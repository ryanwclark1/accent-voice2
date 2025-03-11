# storage.py
# Copyright 2025 Accent Communications

"""Package storage functionality for accent-fetchfw."""

import collections
import json
import logging
import os
from binascii import a2b_hex
from collections.abc import Callable
from configparser import ParsingError, RawConfigParser
from typing import Any

from accent_fetchfw import download, install, util
from accent_fetchfw.download import DownloaderProtocol, RemoteFile
from accent_fetchfw.package import InstallablePackage, InstalledPackage

logger = logging.getLogger(__name__)

class StorageError(util.FetchfwError):
    """Base exception for storage-related errors."""


class ParsingError(StorageError):
    """Raised when parsing a configuration file fails."""


class DefaultRemoteFileBuilder:
    """Builds RemoteFile objects from configuration."""

    def __init__(self, cache_dir: str, downloaders: dict[str, DownloaderProtocol]) -> None:
        """Initialize the remote file builder.

        Args:
            cache_dir: Directory to store downloaded files
            downloaders: Dictionary of available downloaders

        """
        self._cache_dir = cache_dir
        self._downloaders = downloaders

    def build_remote_file(self, config: RawConfigParser, section: str) -> RemoteFile:
        """Build a RemoteFile from a configuration section.

        Args:
            config: Parsed configuration
            section: Section name

        Returns:
            A new RemoteFile instance

        Raises:
            ParsingError: If the configuration is invalid

        """
        url = config.get(section, "url")
        size = config.getint(section, "size")
        sha1sum = a2b_hex(config.get(section, "sha1sum"))
        filename = config.get(section, "filename") if config.has_option(section, "filename") else os.path.basename(url)
        path = os.path.join(self._cache_dir, filename)
        downloader_name = config.get(section, "downloader") if config.has_option(section, "downloader") else "default"
        try:
            downloader = self._downloaders[downloader_name]
        except KeyError:
            raise ParsingError(f"'{downloader_name}' is not a valid downloader name in file definition '{section}'")
        return RemoteFile.new_remote_file(
            path, size, url, downloader, [download.SHA1Hook.create_factory(sha1sum)]
        )

class DefaultFilterBuilder:
    """Builds filter objects from configuration."""

    def _build_unzip(self, args: list[str]) -> install.ZipFilter:
        """Build a ZIP filter.

        Args:
            args: Filter arguments

        Returns:
            A new ZipFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) != 1:
            raise ValueError(f"unzip takes 1 arguments: has {len(args)}")
        return install.ZipFilter(args[0])

    def _build_untar(self, args: list[str]) -> install.TarFilter:
        """Build a TAR filter.

        Args:
            args: Filter arguments

        Returns:
            A new TarFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) != 1:
            raise ValueError(f"untar takes 1 arguments: has {len(args)}")
        return install.TarFilter(args[0])

    def _build_unrar(self, args: list[str]) -> install.RarFilter:
        """Build a RAR filter.

        Args:
            args: Filter arguments

        Returns:
            A new RarFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) != 1:
            raise ValueError(f"unrar takes 1 arguments: has {len(args)}")
        return install.RarFilter(args[0])

    def _build_7z(self, args: list[str]) -> install.Filter7z:
        """Build a 7Z filter.

        Args:
            args: Filter arguments

        Returns:
            A new Filter7z instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) != 1:
            raise ValueError(f"7z takes 1 arguments: has {len(args)}")
        return install.Filter7z(args[0])

    def _build_unsign(self, args: list[str]) -> install.CiscoUnsignFilter:
        """Build a Cisco unsign filter.

        Args:
            args: Filter arguments

        Returns:
            A new CiscoUnsignFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) != 2:
            raise ValueError(f"unsign takes 2 arguments: has {len(args)}")
        return install.CiscoUnsignFilter(args[0], args[1])

    def _build_exclude(self, args: list[str]) -> install.IncludeExcludeFilter:
        """Build an exclude filter.

        Args:
            args: Filter arguments

        Returns:
            A new exclude filter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if not args:
            raise ValueError("exclude takes at least 1 arguments")
        return install.ExcludeFilter(args)

    def _build_include(self, args: list[str]) -> install.IncludeExcludeFilter:
        """Build an include filter.

        Args:
            args: Filter arguments

        Returns:
            A new include filter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if not args:
            raise ValueError("include takes at least 1 arguments")
        return install.IncludeFilter(args)

    def _build_cp(self, args: list[str]) -> install.CopyFilter:
        """Build a copy filter.

        Args:
            args: Filter arguments

        Returns:
            A new CopyFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if len(args) < 2:
            raise ValueError(f"cp takes at least 2 arguments: has {len(args)}")
        return install.CopyFilter(args[:-1], args[-1])

    def _build_null(self, args: list[str]) -> install.NullFilter:
        """Build a null filter.

        Args:
            args: Filter arguments

        Returns:
            A new NullFilter instance

        Raises:
            ValueError: If the arguments are invalid

        """
        if args:
            raise ValueError(f"null takes no arguments: has {len(args)}")
        return install.NullFilter()

    def build_node(self, tokens: list[str]) -> Any:
        """Build a filter node from tokens.

        Args:
            tokens: Token list (first token is the filter type)

        Returns:
            A new filter instance

        Raises:
            ValueError: If the filter type is unknown or arguments are invalid

        """
        type_, args = tokens[0], tokens[1:]
        method_name = "_build_" + type_
        try:
            fun = getattr(self, method_name)
        except AttributeError:
            raise ValueError(f"unknown node type {type_}")
        else:
            return fun(args)

class DefaultInstallMgrFactory:
    """Factory for creating installation managers."""

    def __init__(self, config: RawConfigParser, section: str, filter_builder: DefaultFilterBuilder, global_vars: dict[str, Any]) -> None:
        """Initialize the factory.

        Args:
            config: Parsed configuration
            section: Section name
            filter_builder: Filter builder
            global_vars: Global variables

        """
        self._config = config
        self._section = section
        self._filter_builder = filter_builder
        self._global_vars = global_vars

    def new_install_mgr(self, src_node, local_vars: dict[str, Any]) -> install.InstallationManager:
        """Create a new installation manager.

        Args:
            src_node: Source node
            local_vars: Local variables

        Returns:
            A new InstallationManager instance

        Raises:
            ParsingError: If the configuration is invalid

        """
        vars = dict(self._global_vars)
        vars.update(local_vars)
        filters = {}
        graph = {"sources": {"a": src_node}, "filters": filters}
        for name, value in self._config.items(self._section):
            src, dst = self._get_src_and_dst(name, self._section)
            if dst == "a":
                raise ParsingError(f"usage of reserved dst 'a' in install definition '{self._section}'")
            if dst in filters:
                raise ParsingError(f"at least two filter with dst '{dst}' in install definition '{self._section}'")
            raw_tokens = self._tokenize(value, self._section)
            tokens = self._substitute(raw_tokens, vars)
            filter_obj = self._filter_builder.build_node(tokens)
            filters[dst] = (filter_obj, src)
        return install.InstallationManager(graph)


    def _get_src_and_dst(self, name: str, section: str) -> tuple[str, str]:
        """Get source and destination from a key.

        Args:
            name: Key name
            section: Section name

        Returns:
            Tuple of (source, destination)

        Raises:
            ParsingError: If the key is invalid

        """
        try:
            src, dst = name.split("-")
        except ValueError:
            raise ParsingError(
                f"'{name}' is not a valid key in install definition '{section}'"
            )
        else:
            return src, dst

    def _tokenize(self, value: str, section: str) -> list[str]:
        """Split a value into tokens.

        Args:
            value: Value to tokenize
            section: Section name

        Returns:
            List of tokens

        Raises:
            ParsingError: If the value is empty

        """
        tokens = value.split()
        if not tokens:
            raise ParsingError(
                f"'{value}' is not a valid value in install definition '{section}'"
            )
        return tokens

    def _substitute(
        self, raw_tokens: list[str], local_vars: dict[str, Any]
    ) -> list[str]:
        """Substitute variables in tokens.

        Args:
            raw_tokens: Raw tokens
            local_vars: Local variables

        Returns:
            Tokens with variables substituted

        """
        return [util.apply_subs(token, local_vars) for token in raw_tokens]


class DefaultInstallMgrFactoryBuilder:
    """Factory for creating DefaultInstallMgrFactory instances."""

    def __init__(
        self, filter_builder: DefaultFilterBuilder, global_vars: dict[str, Any]
    ) -> None:
        """Initialize the builder.

        Args:
            filter_builder: Filter builder
            global_vars: Global variables

        """
        self._filter_builder = filter_builder
        self._global_vars = global_vars

    def build_install_mgr_factory(
        self, config: RawConfigParser, section: str
    ) -> DefaultInstallMgrFactory:
        """Build a new installation manager factory.

        Args:
            config: Parsed configuration
            section: Section name

        Returns:
            A new DefaultInstallMgrFactory instance

        """
        return DefaultInstallMgrFactory(
            config, section, self._filter_builder, self._global_vars
        )


class DefaultPkgBuilder:
    """Builds InstallablePackage objects from configuration."""

    def build_installable_pkg(
        self,
        config: RawConfigParser,
        section: str,
        pkg_id: str,
        remotes_files: dict[str, RemoteFile],
        install_mgr_factories: dict[str, DefaultInstallMgrFactory],
    ) -> InstallablePackage:
        """Build an installable package from configuration.

        Args:
            config: Parsed configuration
            section: Section name
            pkg_id: Package ID
            remotes_files: Available remote files
            install_mgr_factories: Available installation manager factories

        Returns:
            A new InstallablePackage instance

        Raises:
            ParsingError: If the configuration is invalid

        """
        # remote files -- a map where keys are remote file ids and values are remote files
        # install_mgr_factories -- a map where keys are install manager ids and values are
        #   install manager factories
        pkg_info = {"id": pkg_id}
        raw_pkg_info = dict(config.items(section))

        if "id" in raw_pkg_info:
            raise ParsingError(f"found invalid option 'id' in pkg def '{section}'")

        if "depends" in raw_pkg_info:
            pkg_info["depends"] = raw_pkg_info.pop("depends").split()

        pkg_remote_files = []
        if "files" in raw_pkg_info:
            for remote_file_id in raw_pkg_info.pop("files").split():
                try:
                    pkg_remote_files.append(remotes_files[remote_file_id])
                except KeyError:
                    raise ParsingError(
                        f"unknown file '{remote_file_id}' in pkg def '{section}'"
                    )

        if "install" in raw_pkg_info:
            tokens = raw_pkg_info.pop("install").split()
            install_mgr_id = tokens[0]
            install_mgr_args = tokens[1:]
            try:
                install_mgr_factory = install_mgr_factories[install_mgr_id]
            except KeyError:
                raise ParsingError(
                    f"unknown install '{install_mgr_id}' in pkg def '{section}'"
                )
            else:
                src_node = install.NonGlobbingFilesystemLinkSource(
                    f.path for f in pkg_remote_files
                )
                local_vars = {}
                for i, remote_file in enumerate(pkg_remote_files):
                    local_vars[f"FILE{i + 1}"] = remote_file.filename
                for i, arg in enumerate(install_mgr_args):
                    local_vars[f"ARG{i + 1}"] = arg
                pkg_install_mgr = install_mgr_factory.new_install_mgr(
                    src_node, local_vars
                )
        else:
            pkg_install_mgr = None

        pkg_info.update(raw_pkg_info)

        return InstallablePackage(pkg_info, pkg_remote_files, pkg_install_mgr)


class BasePkgStorage:
    """Base class for package storage classes."""

    def __getitem__(self, key: str) -> Any:
        """Get a package by ID.

        Args:
            key: Package ID

        Returns:
            The package

        Raises:
            KeyError: If the package is not found

        """
        return self._pkgs[key]

    def __len__(self) -> int:
        """Get the number of packages.

        Returns:
            Number of packages

        """
        return len(self._pkgs)

    def __iter__(self) -> Any:
        """Get an iterator over package IDs.

        Returns:
            Iterator over package IDs

        """
        return iter(self._pkgs)

    def __contains__(self, item: str) -> bool:
        """Check if a package ID exists.

        Args:
            item: Package ID

        Returns:
            True if the package exists, False otherwise

        """
        return item in self._pkgs

    def get(self, key: str, *args) -> Any:
        """Get a package by ID with a default value.

        Args:
            key: Package ID
            *args: Default value if not found

        Returns:
            The package or default value

        """
        return self._pkgs.get(key, *args)

    def items(self) -> list[tuple[str, Any]]:
        """Get all packages.

        Returns:
            List of (id, package) tuples

        """
        return list(self._pkgs.items())

    def keys(self) -> list[str]:
        """Get all package IDs.

        Returns:
            List of package IDs

        """
        return list(self._pkgs.keys())

    def values(self) -> list[Any]:
        """Get all packages.

        Returns:
            List of packages

        """
        return list(self._pkgs.values())

    def get_dependencies(
        self,
        pkg_id: str,
        maxdepth: int = -1,
        filter_fun: Callable[[str], bool] | None = None,
        ignore_missing: bool = False,
    ) -> set[str]:
        """Get dependencies of a package.

        Args:
            pkg_id: Package ID
            maxdepth: Maximum depth (-1 for all, 0 for none)
            filter_fun: Filter function for dependencies
            ignore_missing: Whether to ignore missing dependencies

        Returns:
            Set of dependency package IDs

        Raises:
            KeyError: If the package is not found and ignore_missing is False

        """
        return self.get_dependencies_many(
            [pkg_id], maxdepth, filter_fun, ignore_missing
        )

    def get_dependencies_many(
        self,
        pkg_ids: list[str],
        maxdepth: int = -1,
        filter_fun: Callable[[str], bool] | None = None,
        ignore_missing: bool = False,
    ) -> set[str]:
        """Get dependencies of multiple packages.

        Args:
            pkg_ids: List of package IDs
            maxdepth: Maximum depth (-1 for all, 0 for none)
            filter_fun: Filter function for dependencies
            ignore_missing: Whether to ignore missing dependencies

        Returns:
            Set of dependency package IDs

        Raises:
            KeyError: If a package is not found and ignore_missing is False

        """
        # Return immediately if maxdepth is 0, this simplify the implementation
        if maxdepth == 0:
            return set()
        stack = [(pkg_id, maxdepth) for pkg_id in pkg_ids]
        dependencies = set()
        # Dictionary of pkg_id -> maxdepth to prevent infinite loop
        visited = {}
        while stack:
            # Note that depth is not a real depth value
            pkg_id, depth = stack.pop()
            try:
                pkg = self._pkgs[pkg_id]
            except KeyError:
                if not ignore_missing:
                    raise
            else:
                next_depth = depth - 1
                for dep_pkg_id in pkg.pkg_info["depends"]:
                    if dep_pkg_id in visited:
                        visit_depth = visited[dep_pkg_id]
                        if visit_depth >= next_depth:
                            continue
                    visited[dep_pkg_id] = next_depth
                    if filter_fun is None or filter_fun(dep_pkg_id):
                        dependencies.add(dep_pkg_id)
                        if next_depth:
                            stack.append((dep_pkg_id, next_depth))
        return dependencies


class DefaultInstallablePkgStorage(BasePkgStorage):
    """Storage for installable packages."""

    def __init__(
        self,
        db_dir: str,
        remote_file_builder: DefaultRemoteFileBuilder,
        install_mgr_factory_builder: DefaultInstallMgrFactoryBuilder,
        pkg_builder: DefaultPkgBuilder,
    ) -> None:
        """Initialize the storage.

        Args:
            db_dir: Database directory
            remote_file_builder: Remote file builder
            install_mgr_factory_builder: Installation manager factory builder
            pkg_builder: Package builder

        """
        self._db_dir = db_dir
        self._remote_file_builder = remote_file_builder
        self._install_mgr_factory_builder = install_mgr_factory_builder
        self._pkg_builder = pkg_builder
        self._pkgs: dict[str, InstallablePackage] = {}
        self._load_pkgs()

    def _load_pkgs(self) -> None:
        """Load packages from the database directory."""
        config = self._read_db_files()
        pkg_sections, file_sections, install_sections = self._split_sections(config)
        remote_files = self._create_remote_files(config, file_sections)
        install_mgr_factories = self._create_install_mgr_factories(
            config, install_sections
        )
        self._pkgs = self._create_pkg(
            config, pkg_sections, remote_files, install_mgr_factories
        )

    def _read_db_files(self) -> RawConfigParser:
        """Read database files.

        Returns:
            Parsed configuration

        Raises:
            StorageError: If a file cannot be read or parsed

        """
        db_dir = self._db_dir
        config = RawConfigParser()
        try:
            for rel_path in os.listdir(db_dir):
                if not rel_path.startswith("."):
                    path = os.path.join(db_dir, rel_path)
                    with open(path) as f:
                        config.read_file(f)
        except OSError as e:
            raise StorageError(f"could not open/read file '{path}': {e}")
        except ParsingError as e:
            raise StorageError(f"could not parse file '{path}': {e}")
        return config

    def _split_sections(
        self, config: RawConfigParser
    ) -> tuple[list[str], list[str], list[str]]:
        """Split configuration sections.

        Args:
            config: Parsed configuration

        Returns:
            Tuple of (package sections, file sections, install sections)

        Raises:
            ParsingError: If a section is invalid

        """
        pkg_sections = []
        file_sections = []
        install_sections = []
        for section in config.sections():
            if section.startswith("pkg_"):
                pkg_sections.append(section)
            elif section.startswith("file_"):
                file_sections.append(section)
            elif section.startswith("install_"):
                install_sections.append(section)
            else:
                raise ParsingError(f"invalid section '{section}'")
        return pkg_sections, file_sections, install_sections

    def _create_remote_files(
        self, config: RawConfigParser, sections: list[str]
    ) -> dict[str, RemoteFile]:
        """Create remote files from configuration.

        Args:
            config: Parsed configuration
            sections: File sections

        Returns:
            Dictionary of remote files

        Raises:
            ParsingError: If a remote file is invalid

        """
        remote_files = {}
        remote_file_paths = set()
        for section in sections:
            assert section.startswith("file_")
            remote_file_id = section[5:]
            remote_file = self._remote_file_builder.build_remote_file(config, section)
            if remote_file.path in remote_file_paths:
                raise ParsingError(
                    f"two remote files use the same path: {remote_file.path}"
                )
            remote_file_paths.add(remote_file.path)
            remote_files[remote_file_id] = remote_file
        return remote_files

    def _create_install_mgr_factories(
        self, config: RawConfigParser, sections: list[str]
    ) -> dict[str, DefaultInstallMgrFactory]:
        """Create installation manager factories from configuration.

        Args:
            config: Parsed configuration
            sections: Install sections

        Returns:
            Dictionary of installation manager factories

        """
        install_mgr_factories = {}
        for section in sections:
            assert section.startswith("install_")
            install_mgr_factory_id = section[8:]
            install_mgr_factory = (
                self._install_mgr_factory_builder.build_install_mgr_factory(
                    config, section
                )
            )
            install_mgr_factories[install_mgr_factory_id] = install_mgr_factory
        return install_mgr_factories

    def _create_pkg(
        self,
        config: RawConfigParser,
        sections: list[str],
        remote_files: dict[str, RemoteFile],
        install_mgr_factories: dict[str, DefaultInstallMgrFactory],
    ) -> dict[str, InstallablePackage]:
        """Create packages from configuration.

        Args:
            config: Parsed configuration
            sections: Package sections
            remote_files: Available remote files
            install_mgr_factories: Available installation manager factories

        Returns:
            Dictionary of packages

        """
        pkgs = {}
        for section in sections:
            assert section.startswith("pkg_")
            pkg_id = section[4:]
            pkg = self._pkg_builder.build_installable_pkg(
                config, section, pkg_id, remote_files, install_mgr_factories
            )
            pkgs[pkg_id] = pkg
        return pkgs

    def reload(self) -> None:
        """Reload packages from the database directory."""
        self._load_pkgs()


class DefaultInstalledPkgStorage(BasePkgStorage):
    """Storage for installed packages."""

    def __init__(self, db_dir: str, pretty_printing: bool = False) -> None:
        """Initialize the storage.

        Args:
            db_dir: Database directory
            pretty_printing: Whether to format JSON output

        """
        self._db_dir = db_dir
        self._json_indent = 4 if pretty_printing else None
        self._pkgs: dict[str, InstalledPackage] = {}
        self._requirement_map: dict[str, set[str]] = collections.defaultdict(set)
        self._load_pkgs()

    def _add_requirements(self, pkg: InstalledPackage, pkg_id: str) -> None:
        """Add requirements of a package.

        Args:
            pkg: Package
            pkg_id: Package ID

        """
        for dep_pkg_id in pkg.pkg_info["depends"]:
            self._requirement_map[dep_pkg_id].add(pkg_id)

    def _remove_requirements(self, pkg: InstalledPackage, pkg_id: str) -> None:
        """Remove requirements of a package.

        Args:
            pkg: Package
            pkg_id: Package ID

        """
        for dep_pkg_id in pkg.pkg_info["depends"]:
            self._requirement_map[dep_pkg_id].discard(pkg_id)

    def _load_pkgs(self) -> None:
        """Load packages from the database directory."""
        pkgs = {}
        self._requirement_map = collections.defaultdict(set)
        for pkg_id in os.listdir(self._db_dir):
            if not pkg_id.startswith("."):
                pkg = InstalledPackage(self._load_pkg_info(pkg_id))
                self._add_requirements(pkg, pkg_id)
                pkgs[pkg_id] = pkg
        self._pkgs = pkgs

    def _load_pkg_info(self, pkg_id: str) -> dict[str, Any]:
        """Load package information from a file.

        Args:
            pkg_id: Package ID

        Returns:
            Package information

        """
        filename = os.path.join(self._db_dir, pkg_id)
        with open(filename) as fobj:
            pkg_info = json.load(fobj)
            return pkg_info

    def insert_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Insert a new package.

        Args:
            installed_pkg: Package to insert

        Raises:
            ValueError: If the package already exists

        """
        pkg_info = installed_pkg.pkg_info
        pkg_id = pkg_info["id"]
        if pkg_id in self._pkgs:
            raise ValueError(f"package is already installed: {pkg_id}")
        self._write_pkg_info(pkg_id, pkg_info)
        self._add_requirements(installed_pkg, pkg_id)
        self._pkgs[pkg_id] = installed_pkg

    def update_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Update an existing package.

        Args:
            installed_pkg: Package to update

        Raises:
            ValueError: If the package does not exist

        """
        pkg_info = installed_pkg.pkg_info
        pkg_id = pkg_info["id"]
        if pkg_id not in self._pkgs:
            raise ValueError(f"package is not installed: {pkg_id}")
        self._remove_requirements(installed_pkg, pkg_id)
        self._write_pkg_info(pkg_id, pkg_info)
        self._add_requirements(installed_pkg, pkg_id)
        self._pkgs[pkg_id] = installed_pkg

    def upsert_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Insert or update a package.

        Args:
            installed_pkg: Package to insert or update

        """
        pkg_info = installed_pkg.pkg_info
        pkg_id = pkg_info["id"]
        if pkg_id in self._pkgs:
            self._remove_requirements(installed_pkg, pkg_id)
        self._write_pkg_info(pkg_id, pkg_info)
        self._add_requirements(installed_pkg, pkg_id)
        self._pkgs[pkg_id] = installed_pkg

    def _write_pkg_info(self, pkg_id: str, pkg_info: dict[str, Any]) -> None:
        """Write package information to a file.

        Args:
            pkg_id: Package ID
            pkg_info: Package information

        Raises:
            ValueError: If the package ID is invalid

        """
        if os.sep in pkg_id:
            raise ValueError(f"invalid pkg id: {pkg_id}")
        filename = os.path.join(self._db_dir, pkg_id)
        with open(filename, "w") as fobj:
            json.dump(pkg_info, fobj, indent=self._json_indent)

    def delete_pkg(self, pkg_id: str) -> None:
        """Delete a package.

        Args:
            pkg_id: Package ID

        Raises:
            ValueError: If the package does not exist

        """
        if pkg_id not in self._pkgs:
            raise ValueError(f"package is not installed: {pkg_id}")
        self._remove_requirements(self._pkgs[pkg_id], pkg_id)
        filename = os.path.join(self._db_dir, pkg_id)
        os.remove(filename)
        del self._pkgs[pkg_id]

    def reload(self) -> None:
        """Reload packages from the database directory."""
        self._load_pkgs()

    def get_requisites(self, pkg_id: str) -> set[str]:
        """Get packages that require a package.

        Args:
            pkg_id: Package ID

        Returns:
            Set of package IDs that require the package

        Raises:
            ValueError: If the package does not exist

        """
        if pkg_id not in self._pkgs:
            raise ValueError(f"package is not installed: {pkg_id}")
        return set(self._requirement_map[pkg_id])


def new_installable_pkg_storage(
    db_dir: str,
    cache_dir: str,
    downloaders: dict[str, DownloaderProtocol],
    global_vars: dict[str, Any],
) -> DefaultInstallablePkgStorage:
    """Create a new installable package storage.

    Args:
        db_dir: Database directory
        cache_dir: Cache directory
        downloaders: Available downloaders
        global_vars: Global variables

    Returns:
        A new DefaultInstallablePkgStorage instance

    """
    remote_file_builder = DefaultRemoteFileBuilder(cache_dir, downloaders)
    filter_builder = DefaultFilterBuilder()
    install_mgr_factory_builder = DefaultInstallMgrFactoryBuilder(
        filter_builder, global_vars
    )
    pkg_builder = DefaultPkgBuilder()
    return DefaultInstallablePkgStorage(
        db_dir, remote_file_builder, install_mgr_factory_builder, pkg_builder
    )


def new_installed_pkg_storage(db_dir: str) -> DefaultInstalledPkgStorage:
    """Create a new installed package storage.

    Args:
        db_dir: Database directory

    Returns:
        A new DefaultInstalledPkgStorage instance

    """
    return DefaultInstalledPkgStorage(db_dir)


def new_pkg_storages(
    base_db_dir: str,
    cache_dir: str,
    downloaders: dict[str, DownloaderProtocol],
    global_vars: dict[str, Any],
) -> tuple[DefaultInstallablePkgStorage, DefaultInstalledPkgStorage]:
    """Create new package storages.

    Args:
        base_db_dir: Base database directory
        cache_dir: Cache directory
        downloaders: Available downloaders
        global_vars: Global variables

    Returns:
        Tuple of (installable_pkg_storage, installed_pkg_storage)

    """
    able_db_dir = os.path.join(base_db_dir, "installable")
    ed_db_dir = os.path.join(base_db_dir, "installed")
    for dir in [able_db_dir, ed_db_dir]:
        if not os.path.isdir(dir):
            os.makedirs(dir)
    able_storage = new_installable_pkg_storage(
        able_db_dir, cache_dir, downloaders, global_vars
    )
    ed_storage = new_installed_pkg_storage(ed_db_dir)
    return able_storage, ed_storage
