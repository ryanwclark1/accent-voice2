# install.py
# Copyright 2025 Accent Communications

"""Installation functionality for accent-fetchfw."""

import collections
import contextlib
import glob
import itertools
import logging
import os
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from collections.abc import Callable, Iterable, Iterator
from fnmatch import fnmatch
from typing import (
    Any,
)

from accent_fetchfw.util import FetchfwError

logger = logging.getLogger(__name__)


class InstallationError(FetchfwError):
    """Base exception for installation-related errors."""



class InstallationGraphError(InstallationError):
    """Raised when an installation graph is invalid."""



class _InstallationProcess:
    """Process for installing files from sources through filters."""

    def __init__(
        self,
        sources: dict[str, Any],
        filters: dict[str, tuple[Any, str]],
        dir: str | None = None,
    ) -> None:
        """Initialize the installation process.

        Args:
            sources: Dictionary of source objects
            filters: Dictionary of filter objects and their dependencies
            dir: Directory for temporary files, or None for system default

        """
        self._sources = sources
        self._filters = filters
        self._dir = dir
        self._executed = False
        self._need_cleanup = False
        self._base_dir: str | None = None

    def execute(self) -> str:
        """Execute the installation.

        Returns:
            Directory containing the result of the installation process

        Raises:
            Exception: If the installation process has already been executed

        """
        if self._executed:
            raise Exception("Installation process already executed")
        self._base_dir = tempfile.mkdtemp(dir=self._dir)
        req_map = self._build_requirement_map()

        sources = self._sources
        filters = self._filters
        result_dir, input_dirs, output_dirs = self._create_directories_map(req_map)
        try:
            for node_id in self._create_execution_plan(req_map):
                if node_id in sources:
                    source_obj = sources[node_id]
                    output_dir = output_dirs[node_id]
                    logger.debug("Executing source node %s", node_id)
                    source_obj.pull(output_dir)
                else:
                    assert node_id in filters
                    filter_obj = filters[node_id][0]
                    input_dir = input_dirs[node_id]
                    output_dir = output_dirs[node_id]
                    logger.debug("Executing filter node %s", node_id)
                    filter_obj.apply(input_dir, output_dir)
        except Exception:
            logger.error(
                "Error during execution of installation manager", exc_info=True
            )
            try:
                raise
            finally:
                shutil.rmtree(self._base_dir, True)
        else:
            self._executed = True
            self._need_cleanup = True
            return result_dir

    def _build_requirement_map(self) -> dict[str, list[str]]:
        """Build a map of node dependencies.

        Returns:
            Dictionary mapping node IDs to the IDs of nodes that depend on them

        """
        # Return a 'requirement map', i.e. a dictionary which keys are node id
        # and values are node id that depends on the key
        req_map = {
            node_id: [] for node_id in itertools.chain(self._sources, self._filters)
        }
        for filter_id, (_, filter_dependency) in self._filters.items():
            req_map[filter_dependency].append(filter_id)
        return req_map

    def _create_directories_map(
        self, req_map: dict[str, list[str]]
    ) -> tuple[str, dict[str, str], dict[str, str]]:
        """Create directories for installation.

        Args:
            req_map: Requirement map from _build_requirement_map

        Returns:
            Tuple of (result_dir, input_dirs, output_dirs)

        """
        # note that self._base_dir must have been set
        assert self._base_dir is not None
        result_dir = os.path.join(self._base_dir, "result")
        os.mkdir(result_dir)
        input_dirs: dict[str, str] = {}
        output_dirs: dict[str, str] = {}
        for node_id, requirements in req_map.items():
            if not requirements:
                # terminal node
                output_dirs[node_id] = result_dir
            else:
                # non-terminal node
                cur_dir = os.path.join(self._base_dir, "node_" + node_id)
                os.mkdir(cur_dir)
                output_dirs[node_id] = cur_dir
                for requirement in requirements:
                    input_dirs[requirement] = cur_dir
        return result_dir, input_dirs, output_dirs

    def _create_execution_plan(self, req_map: dict[str, list[str]]) -> Iterator[str]:
        """Create an execution plan for installation.

        Args:
            req_map: Requirement map from _build_requirement_map

        Returns:
            Iterator yielding node IDs in execution order

        """
        # Return a iterator which gives a valid order of execution of nodes
        # The algorithm is correct since each filter has 1 and exactly 1 dependency
        deque: collections.deque = collections.deque(self._sources)
        while deque:
            node_id = deque.popleft()
            yield node_id
            for requirement in req_map[node_id]:
                if requirement not in deque:
                    deque.append(requirement)

    def cleanup(self) -> None:
        """Remove all files and directories created during the installation.

        Note that this includes the files in the result directory.

        It is safe to call this method even if the install process has not
        been executed or to call this method more than once.
        """
        if self._need_cleanup and self._base_dir is not None:
            shutil.rmtree(self._base_dir, True)
            self._need_cleanup = False


class InstallationManager:
    """Manager for installation processes."""

    def __init__(self, installation_graph: dict[str, dict[str, Any]]) -> None:
        """Build an InstallationManager.

        Args:
            installation_graph: Dictionary defining the installation graph
                For example:
                {
                    'filters': {
                        'ZipFilter1': (<ZipFilter object>, 'TarFilter1'),
                        'TarFilter1': (<TarFilter object>, 'FilesystemLinkSource'),
                    },
                    'sources': {
                        'FilesystemLinkSource1': <FilesystemLinkSource object>
                    }
                }

        Note:
            Node IDs must match the regex \\w+.
            A filter is an object with an 'apply(src_directory, dst_directory)' method.
            A source is an object with a 'pull(dst_directory)' method.

        Raises:
            InstallationGraphError: If the installation graph is invalid

        """
        self._sources = installation_graph["sources"]
        self._filters = installation_graph["filters"]
        self._check_installation_graph_validity()

    def _check_installation_graph_validity(self) -> None:
        """Check if the installation graph is valid.

        Raises:
            InstallationGraphError: If the installation graph is invalid

        """
        self._check_nodes_id_are_unique()
        self._check_filters_depend_on_valid_node()
        self._check_no_useless_source()
        self._check_is_acyclic()

    def _check_nodes_id_are_unique(self) -> None:
        """Check that node IDs are unique.

        Raises:
            InstallationGraphError: If node IDs are not unique

        """
        common_ids = set(self._sources).intersection(self._filters)
        if common_ids:
            raise InstallationGraphError(
                f"these IDs are shared by both a source and a filter: {common_ids}"
            )

    def _check_filters_depend_on_valid_node(self) -> None:
        """Check that filters depend on valid nodes.

        Raises:
            InstallationGraphError: If a filter depends on an unknown node

        """
        # Check that there's no unknown identifier in the installation graph, i.e. raise an
        # exception if there's a filter such that it depends on an unknown node.
        sources = self._sources
        filters = self._filters
        for filter_id, filter_value in filters.items():
            node_dependency = filter_value[1]
            if node_dependency not in filters and node_dependency not in sources:
                raise InstallationGraphError(
                    f"filter '{filter_id}' depends on unknown filter/source '{node_dependency}'"
                )

    def _check_no_useless_source(self) -> None:
        """Check that all sources are used.

        Raises:
            InstallationGraphError: If there are unused sources

        """
        # Check if every source participates in the installation process, i.e. raise an exception
        # if there's a source such that no other filter depend on it.
        dependencies = (v[1] for v in self._filters.values())
        unused_sources = set(self._sources).difference(dependencies)
        if unused_sources:
            raise InstallationGraphError(
                f"these sources don't participate in the installation: {unused_sources}"
            )

    def _check_is_acyclic(self) -> None:
        """Check that the installation graph is acyclic.

        Raises:
            InstallationGraphError: If the installation graph has a cycle

        """
        # Check that the installation graph is acyclic
        sources = self._sources
        filters = self._filters
        visited: set[str] = set()
        for node_id in filters:
            if node_id not in visited:
                currently_visited: set[str] = {node_id}
                while True:
                    next_node_id = filters[node_id][1]
                    if next_node_id in sources:
                        break
                    if next_node_id in currently_visited:
                        raise InstallationGraphError(
                            "a cycle in the installation graph has been detected"
                        )
                    currently_visited.add(next_node_id)
                    node_id = next_node_id
                visited.update(currently_visited)

    def new_installation_process(
        self, dir: str | None = None
    ) -> _InstallationProcess:
        """Return an installation process instance.

        Args:
            dir: Directory for temporary files, or None for system default

        Returns:
            An installation process instance

        """
        return _InstallationProcess(self._sources, self._filters, dir)


class _GlobHelper:
    """Helper for applying glob patterns to arbitrary directories.

    The python glob module works only with the notion of the current directory.
    This class is used to facilitate the application of one or more glob patterns
    inside arbitrary directories.
    """

    def __init__(
        self, pathnames: str | Iterable[str], error_on_no_matches: bool = True
    ) -> None:
        """Initialize the glob helper.

        Args:
            pathnames: Single path name or iterable of path names
            error_on_no_matches: Whether to raise an error if no matches are found

        Raises:
            ValueError: If a path name is absolute or references a parent directory

        """
        if isinstance(pathnames, str):
            self._pathnames = [os.path.normpath(pathnames)]
        else:
            self._pathnames = [os.path.normpath(pathname) for pathname in pathnames]
        for pathname in self._pathnames:
            if os.path.isabs(pathname):
                raise ValueError(f"path name '{pathname}' is an absolute path")
            if pathname.startswith(os.pardir):
                raise ValueError(
                    f"path name '{pathname}' makes reference to the parent directory"
                )
        self._error_on_no_matches = error_on_no_matches

    def glob_in_dir(self, src_directory: str) -> list[str]:
        """Apply glob patterns in a directory.

        Args:
            src_directory: Directory to search in

        Returns:
            List of matched file paths

        Raises:
            InstallationError: If no matches are found and error_on_no_matches is True

        """
        return list(self.iglob_in_dir(src_directory))

    def iglob_in_dir(self, src_directory: str) -> Iterator[str]:
        """Apply glob patterns in a directory.

        Args:
            src_directory: Directory to search in

        Yields:
            Matched file paths

        Raises:
            InstallationError: If no matches are found and error_on_no_matches is True

        """
        no_matches = True
        for rel_pathname in self._pathnames:
            abs_pathname = os.path.join(src_directory, rel_pathname)
            for globbed_abs_pathname in glob.iglob(abs_pathname):
                no_matches = False
                yield globbed_abs_pathname
        if no_matches and self._error_on_no_matches:
            raise InstallationError(
                f"the glob patterns {self._pathnames} did not match anything in directory '{src_directory}'"
            )


class FilesystemLinkSource:
    """A source which creates symlinks of existing files to the destination directory.

    Warning:
        Be careful when using this source with directories, as you might encounter
        issues if creating links to parent directories of the destination directory.

    """

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the source.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        if isinstance(pathnames, str):
            self._pathnames = [pathnames]
        else:
            self._pathnames = list(pathnames)

    def pull(self, dst_directory: str) -> None:
        """Create symlinks in the destination directory.

        Args:
            dst_directory: Destination directory

        """
        for pathname in self._pathnames:
            for globbed_pathname in glob.iglob(pathname):
                os.symlink(
                    globbed_pathname,
                    os.path.join(dst_directory, os.path.basename(globbed_pathname)),
                )


class NonGlobbingFilesystemLinkSource:
    """A source which creates symlinks without globbing patterns."""

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the source.

        Args:
            pathnames: Single pathname or iterable of pathnames

        """
        if isinstance(pathnames, str):
            self._pathnames = [pathnames]
        else:
            self._pathnames = list(pathnames)

    def pull(self, dst_directory: str) -> None:
        """Create symlinks in the destination directory.

        Args:
            dst_directory: Destination directory

        Raises:
            InstallationError: If a path does not exist

        """
        for pathname in self._pathnames:
            # Note that we check if pathname really exists so we can easily
            # detect human error, that said it's still possible that the file
            # be removed during execution
            if not os.path.exists(pathname):
                raise InstallationError(f"path doesn't exist: {pathname}")
            os.symlink(
                pathname, os.path.join(dst_directory, os.path.basename(pathname))
            )


class FilesystemCopySource:
    """A source which copies files to the destination directory."""

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the source.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        if isinstance(pathnames, str):
            self._pathnames = [pathnames]
        else:
            self._pathnames = list(pathnames)

    def pull(self, dst_directory: str) -> None:
        """Copy files to the destination directory.

        Args:
            dst_directory: Destination directory

        """
        for pathname in self._pathnames:
            for globbed_pathname in glob.iglob(pathname):
                dst_pathname = os.path.join(
                    dst_directory, os.path.basename(globbed_pathname)
                )
                if os.path.isdir(globbed_pathname):
                    shutil.copytree(globbed_pathname, dst_pathname)
                else:
                    shutil.copy(globbed_pathname, dst_pathname)


class NullSource:
    """A source that adds nothing to the destination directory.

    Mostly useful for testing purposes.
    """

    def pull(self, dst_directory: str) -> None:
        """Do nothing.

        Args:
            dst_directory: Destination directory

        """


class ZipFilter:
    """A filter that extracts ZIP files."""

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the filter.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        self._glob_helper = _GlobHelper(pathnames)

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Extract ZIP files from the source directory to the destination directory.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        """
        for pathname in self._glob_helper.iglob_in_dir(src_directory):
            with contextlib.closing(zipfile.ZipFile(pathname, "r")) as zf:
                zf.extractall(dst_directory)


class TarFilter:
    """A filter that extracts TAR files."""

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the filter.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        self._glob_helper = _GlobHelper(pathnames)

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Extract TAR files from the source directory to the destination directory.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        """
        for pathname in self._glob_helper.iglob_in_dir(src_directory):
            with contextlib.closing(tarfile.open(pathname)) as tf:
                tf.extractall(dst_directory)


class RarFilter:
    """A filter that extracts RAR files.

    Note:
        Requires the "unrar" executable to be installed on the system.

    """

    _CMD_PREFIX = ["unrar", "e", "-idq", "-y"]

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the filter.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        self._glob_helper = _GlobHelper(pathnames)

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Extract RAR files from the source directory to the destination directory.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        Raises:
            InstallationError: If the unrar command fails

        """
        for pathname in self._glob_helper.iglob_in_dir(src_directory):
            cmd = [*self._CMD_PREFIX, pathname, dst_directory]
            logger.debug("Executing external command: %s", cmd)
            retcode = subprocess.call(cmd)
            if retcode:
                raise InstallationError(f"unrar returned status code {retcode}")


class Filter7z:
    """A filter that extracts 7z files.

    Note:
        Requires the "7zr" executable to be installed on the system.

    """

    _CMD_PREFIX = ["7zr", "e", "-bd"]

    def __init__(self, pathnames: str | Iterable[str]) -> None:
        """Initialize the filter.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns

        """
        self._glob_helper = _GlobHelper(pathnames)

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Extract 7z files from the source directory to the destination directory.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        Raises:
            InstallationError: If the 7zr command fails

        """
        for pathname in self._glob_helper.iglob_in_dir(src_directory):
            cmd = [*self._CMD_PREFIX, f"-o{dst_directory}", pathname]
            # there's no "quiet" option for 7zr, so we redirect stdout to /dev/null
            with open(os.devnull, "wb") as devnull_fobj:
                logger.debug("Executing external command: %s", cmd)
                retcode = subprocess.call(cmd, stdout=devnull_fobj)
            if retcode:
                raise InstallationError(f"7zr returned status code {retcode}")


class CiscoUnsignFilter:
    """A filter that extracts the gzipped file from a Cisco-signed file."""

    _BUF_SIZE = 512
    _GZIP_MAGIC_NUMBER = (
        b"\x1f\x8b"  # see http://www.gzip.org/zlib/rfc-gzip.html#file-format
    )

    def __init__(self, signed_pathname: str, unsigned_pathname: str) -> None:
        """Initialize the filter.

        Args:
            signed_pathname: Path to the signed file (can be a glob pattern)
            unsigned_pathname: Path to write the unsigned file

        Raises:
            ValueError: If unsigned_pathname is an absolute path or references a parent directory

        """
        self._glob_helper = _GlobHelper(signed_pathname)
        self._unsigned_pathname = os.path.normpath(unsigned_pathname)
        if os.path.isabs(self._unsigned_pathname):
            raise ValueError(
                f"unsigned path name '{self._unsigned_pathname}' is an absolute path"
            )
        if self._unsigned_pathname.startswith(os.pardir):
            raise ValueError(
                f"unsigned path name '{self._unsigned_pathname}' makes reference to the parent directory"
            )

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Extract the gzipped file from a Cisco-signed file.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        Raises:
            InstallationError: If multiple files match the pattern or the gzip magic number is not found

        """
        signed_pathnames = self._glob_helper.glob_in_dir(src_directory)
        if len(signed_pathnames) > 1:
            raise InstallationError(
                f"glob pattern matched {len(signed_pathnames)} files"
            )
        signed_pathname = signed_pathnames[0]
        with open(signed_pathname, "rb") as sf:
            buf = sf.read(CiscoUnsignFilter._BUF_SIZE)
            index = buf.find(CiscoUnsignFilter._GZIP_MAGIC_NUMBER)
            if index == -1:
                raise InstallationError(
                    "Couldn't find gzip magic number in the signed file."
                )
            unsigned_filename = os.path.join(dst_directory, self._unsigned_pathname)
            with open(unsigned_filename, "wb") as f:
                f.write(buf[index:])
                shutil.copyfileobj(sf, f)


class IncludeExcludeFilter:
    """A filter that selectively includes or excludes files."""

    def __init__(self, filter_fun: Callable[[str, str], bool]) -> None:
        """Initialize the filter.

        Args:
            filter_fun: Function that takes the relative path and absolute path of a file
                and returns True to include it or False to exclude it

        """
        self._filter_fun = filter_fun

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Apply the filter.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        """
        rel_dir_stack = [os.curdir]
        while rel_dir_stack:
            rel_current_dir = rel_dir_stack.pop()
            abs_current_dir = os.path.join(src_directory, rel_current_dir)
            for file in os.listdir(abs_current_dir):
                rel_file = (
                    file
                    if rel_current_dir == os.curdir
                    else os.path.join(rel_current_dir, file)
                )
                src_abs_file = os.path.join(src_directory, rel_file)
                if self._filter_fun(rel_file, src_abs_file):
                    dst_abs_file = os.path.join(dst_directory, rel_file)
                    if os.path.isdir(src_abs_file):
                        os.mkdir(dst_abs_file)
                        rel_dir_stack.append(rel_file)
                    else:
                        shutil.copy(src_abs_file, dst_abs_file)


def ExcludeFilter(pathnames: str | Iterable[str]) -> IncludeExcludeFilter:
    """Create a filter that excludes files matching patterns.

    Args:
        pathnames: Single glob pattern or iterable of glob patterns

    Returns:
        An IncludeExcludeFilter instance

    """
    pathnames = [pathnames] if isinstance(pathnames, str) else list(pathnames)

    def filter_fun(rel_file: str, abs_file: str) -> bool:
        return all(not fnmatch(rel_file, pathname) for pathname in pathnames)

    return IncludeExcludeFilter(filter_fun)


def IncludeFilter(pathnames: str | Iterable[str]) -> IncludeExcludeFilter:
    """Create a filter that includes only files matching patterns.

    Args:
        pathnames: Single glob pattern or iterable of glob patterns

    Returns:
        An IncludeExcludeFilter instance

    """
    pathnames = [pathnames] if isinstance(pathnames, str) else list(pathnames)

    included_dirs: set[str] = set()

    def filter_fun(rel_file: str, abs_file: str) -> bool:
        # Include rel_file if it's a child of an already included directory
        rel_dirname = os.path.dirname(rel_file)
        if rel_dirname in included_dirs:
            if os.path.isdir(abs_file):
                included_dirs.add(rel_file)
            return True
        for pathname in pathnames:
            if fnmatch(rel_file, pathname):
                if os.path.isdir(abs_file):
                    included_dirs.add(rel_file)
                return True
        return False

    return IncludeExcludeFilter(filter_fun)


class CopyFilter:
    """A filter that copies files to a specific path."""

    def __init__(self, pathnames: str | Iterable[str], dst: str) -> None:
        """Initialize the filter.

        Args:
            pathnames: Single glob pattern or iterable of glob patterns
            dst: Destination path (directory if it ends with /, file otherwise)

        """
        self._glob_helper = _GlobHelper(pathnames)
        self._dst = dst

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Apply the filter.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        Raises:
            InstallationError: If the destination exists but is the wrong type
            OSError: If file operations fail

        """
        dst_is_dir = self._dst.endswith("/")
        abs_dst = os.path.join(dst_directory, self._dst)
        try:
            if os.path.exists(abs_dst):
                if os.path.isdir(abs_dst) != dst_is_dir:
                    if dst_is_dir:
                        raise InstallationError(
                            "destination exists and is a file but should be a directory"
                        )
                    raise InstallationError(
                        "destination exists and is a directory but should be a file"
                    )
            else:
                dirname = os.path.dirname(abs_dst)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            if dst_is_dir:
                self._apply_dir(src_directory, abs_dst)
            else:
                self._apply_file(src_directory, abs_dst)
        except OSError as e:
            logger.error("Error during execution of copy filter", exc_info=True)
            raise InstallationError(str(e))

    def _apply_dir(self, src_directory: str, abs_dst: str) -> None:
        """Copy files to a directory.

        Args:
            src_directory: Source directory
            abs_dst: Absolute path to destination directory

        """
        for pathname in self._glob_helper.iglob_in_dir(src_directory):
            if os.path.isdir(pathname):
                src_dir_name = os.path.basename(pathname)
                shutil.copytree(pathname, os.path.join(abs_dst, src_dir_name), True)
            else:
                shutil.copy(pathname, abs_dst)

    def _apply_file(self, src_directory: str, abs_dst: str) -> None:
        """Copy a file to a specific path.

        Args:
            src_directory: Source directory
            abs_dst: Absolute path to destination file

        Raises:
            InstallationError: If multiple files match the pattern

        """
        pathnames = self._glob_helper.glob_in_dir(src_directory)
        if len(pathnames) > 1:
            raise InstallationError(f"glob pattern matched {len(pathnames)} files")
        pathname = pathnames[0]
        shutil.copy(pathname, abs_dst)


class NullFilter:
    """A filter that does nothing.

    Mostly useful for testing purposes.
    """

    def apply(self, src_directory: str, dst_directory: str) -> None:
        """Do nothing.

        Args:
            src_directory: Source directory
            dst_directory: Destination directory

        """
