# util.py
# Copyright 2025 Accent Communications

"""Utility functions for accent-fetchfw."""

import errno
import logging
import operator
import os
import re
import shutil
from collections.abc import Iterator
from typing import Any

logger = logging.getLogger(__name__)

class FetchfwError(Exception):
    """Base exception for all fetchfw errors."""

_APPLY_SUBS_REGEX = re.compile(r"(?<!\\)\$(?:{(\w*)}|(\w*))")

def apply_subs(string: str, variables: dict[str, Any]) -> str:
    """Apply variable substitution to a string.

    Args:
        string: String with variables
        variables: Dictionary of variable values

    Returns:
        String with variables substituted

    Raises:
        KeyError: If a variable is not defined
        ValueError: If the substitution string is invalid

    """
    def aux(m):
        var_name = m.group(1)
        if var_name is None:
            var_name = m.group(2)
        if not var_name:
            raise ValueError(f"invalid zero-length variable: {string}")
        try:
            var_value = variables[var_name]
        except KeyError:
            raise KeyError(f"undefined substitution '{var_name}'")
        else:
            # This treats a special case where var_value has the string
            # "\$" in it, we don't want it to get unescaped at the end
            return str(var_value).replace(r"\$", r"\\$")

    interm = _APPLY_SUBS_REGEX.sub(aux, string)
    return interm.replace(r"\$", "$")

def _split_version(raw_version: str) -> tuple[int, list[str], int]:
    """Split a version string into components.

    Args:
        raw_version: Version string

    Returns:
        Tuple of (epoch, version_tokens, release)

    """
    if ":" in raw_version:
        epoch, rest = raw_version.split(":", 1)
        epoch = int(epoch)
    else:
        epoch = 0
        rest = raw_version
    if "-" in rest:
        rest, rel = rest.rsplit("-", 1)
        rel = int(rel)
    else:
        rel = 0
    return epoch, rest.split("."), rel

def cmp(x: Any, y: Any) -> int:
    """Compare two values.

    Args:
        x: First value
        y: Second value

    Returns:
        -1 if x < y, 0 if x == y, 1 if x > y

    """
    return (x > y) - (x < y)

def cmp_version(version1: str, version2: str) -> int:
    """Compare two version strings.

    Args:
        version1: First version
        version2: Second version

    Returns:
        -1 if version1 < version2, 0 if version1 == version2, 1 if version1 > version2

    """
    # Common case optimization
    if version1 == version2:
        return 0
    v1_epoch, v1_tokens, v1_rel = _split_version(version1)
    v2_epoch, v2_tokens, v2_rel = _split_version(version2)
    # Compare epoch
    if v1_epoch != v2_epoch:
        return v1_epoch - v2_epoch
    # Compare version
    for v1_token, v2_token in zip(v1_tokens, v2_tokens, strict=False):
        v1_is_digit = v1_token.isdigit()
        v2_is_digit = v2_token.isdigit()
        if v1_is_digit and v2_is_digit:
            v1_int_token = int(v1_token)
            v2_int_token = int(v2_token)
            if v1_int_token != v2_int_token:
                return v1_int_token - v2_int_token
        elif v1_is_digit:
            assert not v2_is_digit
            return 1
        elif v2_is_digit:
            assert not v1_is_digit
            return -1
        else:
            token_cmp = cmp(v1_token, v2_token)
            if token_cmp:
                return token_cmp
    # Check tokens length
    tokens_len_diff = len(v1_tokens) - len(v2_tokens)
    if tokens_len_diff:
        return tokens_len_diff
    # Compare release
    if v1_rel != v2_rel:
        return v1_rel - v2_rel
    # We reach this if we compare "1.0" with "1.00" for example
    return 0

def _recursive_listdir_tuple(directory: str) -> Iterator[tuple[str, str]]:
    """Recursively list files in a directory.

    Args:
        directory: Directory to list

    Yields:
        Tuples of (absolute_path, relative_path)

    """
    directories_stack = []
    for path in os.listdir(directory):
        abs_path = os.path.join(directory, path)
        if os.path.isdir(abs_path):
            directories_stack.append(path)
        yield abs_path, path
    while directories_stack:
        cur_directory = directories_stack.pop()
        cur_abs_directory = os.path.join(directory, cur_directory)
        for path in os.listdir(cur_abs_directory):
            rel_path = os.path.join(cur_directory, path)
            abs_path = os.path.join(directory, rel_path)
            if os.path.isdir(abs_path):
                directories_stack.append(rel_path)
            yield abs_path, rel_path

def recursive_listdir(directory: str) -> Iterator[str]:
    """Recursively list files in a directory.

    Args:
        directory: Directory to list

    Yields:
        Relative paths of files and directories

    """
    return map(operator.itemgetter(1), _recursive_listdir_tuple(directory))

def list_paths(directory: str) -> Iterator[str]:
    """Recursively list files in a directory, marking directories with a trailing slash.

    Args:
        directory: Directory to list

    Yields:
        Relative paths of files and directories (directories have a trailing slash)

    """
    for abs_path, path in _recursive_listdir_tuple(directory):
        if os.path.isdir(abs_path):
            yield path + "/"
        else:
            yield path

def install_paths(src_directory: str, dst_directory: str) -> Iterator[str]:
    """Copy files from source to destination.

    Args:
        src_directory: Source directory
        dst_directory: Destination directory

    Yields:
        Relative paths of copied files and directories

    Raises:
        OSError: If a file cannot be copied

    """
    for src_abs_path, path in _recursive_listdir_tuple(src_directory):
        dst_abs_path = os.path.join(dst_directory, path)
        if os.path.isdir(src_abs_path):
            try:
                os.mkdir(dst_abs_path)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(dst_abs_path):
                    # dst_abs_path already exists and is a directory
                    pass
                else:
                    raise
            yield path + "/"
        else:
            # Do not use shutil.copy since dst must not be a directory
            shutil.copyfile(src_abs_path, dst_abs_path)
            shutil.copymode(src_abs_path, dst_abs_path)
            yield path

def remove_paths(paths: list[str], directory: str) -> Iterator[str]:
    """Remove files and directories.

    Args:
        paths: List of paths to remove (directories should end with a slash)
        directory: Base directory

    Yields:
        Paths that were (or would have been) removed

    Raises:
        OSError: If a file or directory cannot be removed

    """
    non_empty_directories = []
    for path in sorted(paths, reverse=True):
        abs_path = os.path.join(directory, path)
        if abs_path.endswith("/"):
            # Test if 'os.rmdir' will fail, i.e. if removing a child path that
            # previously failed.
            for non_empty_directory in non_empty_directories:
                if non_empty_directory.startswith(abs_path):
                    logger.debug(
                        "Not trying to remove '%s' since removing '%s' failed",
                        abs_path,
                        non_empty_directory,
                    )
                    break
            else:
                logger.debug("Deleting '%s' as directory", abs_path)
                try:
                    os.rmdir(abs_path)
                except OSError as e:
                    if e.errno == errno.ENOTEMPTY:
                        logger.debug(
                            "Could not delete directory '%s' because it is not empty",
                            path,
                        )
                        non_empty_directories.append(abs_path)
                    elif e.errno == errno.ENOENT:
                        logger.warning(
                            "Could not delete directory '%s' because it does not exist",
                            path,
                        )
                    else:
                        raise
        else:
            logger.debug("Deleting '%s' as file", abs_path)
            try:
                os.remove(abs_path)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    logger.warning(
                        "Could not delete file '%s' because it does not exist", abs_path
                    )
                else:
                    raise
        yield path

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
