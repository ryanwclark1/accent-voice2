# package.py
# Copyright 2025 Accent Communications

"""Package management functionality for accent-fetchfw."""

import copy
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from accent_fetchfw.models import PackageInfo
from accent_fetchfw.util import FetchfwError, cmp_version, install_paths, remove_paths

logger = logging.getLogger(__name__)

class PackageError(FetchfwError):
    """Base exception for package-related errors."""
    pass

_COMMON_MANDATORY_KEYS = ['id', 'version', 'description']

def _check_pkg_info(pkg_info: Dict[str, Any], mandatory_keys: List[str]) -> None:
    """Check that package info has all mandatory keys.

    Args:
        pkg_info: Package information
        mandatory_keys: List of required keys

    Raises:
        Exception: If a mandatory key is missing
    """
    for key in mandatory_keys:
        if key not in pkg_info:
            raise Exception(f"missing mandatory key {key}")

def _add_pkg_info_defaults(pkg_info: Dict[str, Any]) -> None:
    """Add default values to package info.

    Args:
        pkg_info: Package information to update
    """
    pkg_info.setdefault('depends', [])

class InstallablePackage:
    """A package that can be installed."""

    _MANDATORY_KEYS = _COMMON_MANDATORY_KEYS

    def __init__(self, pkg_info: Dict[str, Any], remote_files: List, install_mgr) -> None:
        """Initialize a new installable package.

        Args:
            pkg_info: Package information
            remote_files: List of remote files
            install_mgr: Installer manager or None

        Raises:
            Exception: If mandatory keys are missing
        """
        _check_pkg_info(pkg_info, self._MANDATORY_KEYS)
        _add_pkg_info_defaults(pkg_info)
        self.pkg_info = pkg_info
        self.remote_files = remote_files
        self.install_mgr = install_mgr

    def clone(self) -> 'InstallablePackage':
        """Create a copy of this package.

        Returns:
            A new package instance with the same properties
        """
        new_pkg_info = copy.deepcopy(self.pkg_info)
        return InstallablePackage(new_pkg_info, self.remote_files, self.install_mgr)

    def new_installed_package(self) -> 'InstalledPackage':
        """Create an installed package from this installable package.

        Returns:
            A new installed package
        """
        new_pkg_info = copy.deepcopy(self.pkg_info)
        return InstalledPackage(new_pkg_info)

    def __str__(self) -> str:
        """Get a string representation of the package.

        Returns:
            String representation
        """
        return f"{self.pkg_info['id']} {self.pkg_info['version']}"

class InstalledPackage:
    """A package that is installed on the system."""

    _MANDATORY_KEYS = [*_COMMON_MANDATORY_KEYS, 'files', 'explicit_install']

    def __init__(self, pkg_info: Dict[str, Any]) -> None:
        """Initialize a new installed package.

        Args:
            pkg_info: Package information

        Raises:
            Exception: If mandatory keys are missing
        """
        _check_pkg_info(pkg_info, self._MANDATORY_KEYS)
        _add_pkg_info_defaults(pkg_info)
        self.pkg_info = pkg_info

    def __str__(self) -> str:
        """Get a string representation of the package.

        Returns:
            String representation
        """
        return f"{self.pkg_info['id']} {self.pkg_info['version']}"

class PackageManager:
    """Manager for package installation, removal, and upgrades."""

    def __init__(self, installable_pkg_sto, installed_pkg_sto) -> None:
        """Initialize the package manager.

        Args:
            installable_pkg_sto: Storage for installable packages
            installed_pkg_sto: Storage for installed packages
        """
        self.installable_pkg_sto = installable_pkg_sto
        self.installed_pkg_sto = installed_pkg_sto

    def _remove_installed_paths(self, installed_paths: List[str], root_dir: str) -> None:
        """Remove installed paths, logging any errors.

        Args:
            installed_paths: List of paths to remove
            root_dir: Root directory
        """
        removed_paths = []
        try:
            # This relies on the fact that remove_paths is a generator
            for removed_path in remove_paths(installed_paths, root_dir):
                removed_paths.append(removed_path)
        except Exception as e:
            # Error while removing files we were successful at installing
            non_removed_paths = list(set(installed_paths).difference(removed_paths))
            logger.warning(f'Error while removing already installed files: {e}', exc_info=True)
            logger.warning(f'The following files have been left in {root_dir}: {non_removed_paths}')

    def _install_pkg_from_install_mgr(self, install_mgr, root_dir: str, pkg_id: str) -> List[str]:
        """Install a package using an installation manager.

        Args:
            install_mgr: Installation manager
            root_dir: Root directory
            pkg_id: Package ID

        Returns:
            List of installed paths

        Raises:
            Exception: If installation fails
        """
        install_process = install_mgr.new_installation_process()
        result_dir = install_process.execute()

        installed_paths = []
        # This relies on the fact that install_paths is a generator
        try:
            for installed_path in install_paths(result_dir, root_dir):
                installed_paths.append(installed_path)
        except Exception as e:
            logger.error(f'Error during installation of pkg {pkg_id} in {root_dir}: {e}')
            # Preserve stack trace while removing installed files
            try:
                raise
            finally:
                self._remove_installed_paths(installed_paths, root_dir)
        else:
            return installed_paths
        finally:
            install_process.cleanup()

    def _install_pkg(self, installable_pkg: InstallablePackage, root_dir: str) -> Optional[InstalledPackage]:
        """Install a package.

        Args:
            installable_pkg: Package to install
            root_dir: Root directory

        Returns:
            Installed package or None if installation fails

        Raises:
            Exception: If installation fails
        """
        pkg_id = installable_pkg.pkg_info['id']

        # Install files
        install_mgr = installable_pkg.install_mgr
        if install_mgr is None:
            logger.debug(f"No install mgr for pkg {pkg_id}")
            files = []
        else:
            files = self._install_pkg_from_install_mgr(install_mgr, root_dir, pkg_id)

        # Commit to installed database
        try:
            installable_pkg.pkg_info['files'] = files
            installed_pkg = installable_pkg.new_installed_package()

            self.installed_pkg_sto.upsert_pkg(installed_pkg)
        except Exception as e:
            logger.error(f"Error while committing pkg {pkg_id} to storage: {e}")
            # Preserve stack trace while removing installed files
            try:
                raise
            finally:
                self._remove_installed_paths(files, root_dir)
        else:
            return installed_pkg

    async def _install_pkg_async(self, installable_pkg: InstallablePackage, root_dir: str) -> Optional[InstalledPackage]:
        """Install a package asynchronously.

        Args:
            installable_pkg: Package to install
            root_dir: Root directory

        Returns:
            Installed package or None if installation fails

        Raises:
            Exception: If installation fails
        """
        # This is a placeholder - implementing fully async installation would require
        # more extensive changes to the installation process
        return self._install_pkg(installable_pkg, root_dir)

    def install(self, raw_pkg_ids: List[str], root_dir: str, installer_ctrl_factory: Callable) -> None:
        """Install packages.

        Args:
            raw_pkg_ids: List of package IDs to install
            root_dir: Root directory
            installer_ctrl_factory: Factory for creating installer controller

        Raises:
            Exception: If installation fails
        """
        # 1. Do some preparation
        installable_pkg_sto = self.installable_pkg_sto
        installed_pkg_sto = self.installed_pkg_sto
        # 1.1. Instantiate an installer controller
        installer_ctrl = installer_ctrl_factory(installable_pkg_sto, installed_pkg_sto)
        installer_ctrl.pre_installation()

        try:
            # 2. Preprocessing
            # 2.1. Get the list of package ids to install
            pkg_ids = installer_ctrl.preprocess_raw_pkg_ids(raw_pkg_ids)

            # 2.2. Get the list of packages to install
            # Next line raises an error if one of pkg id is invalid, which is what we want
            raw_pkgs = [installable_pkg_sto[pkg_id].clone() for pkg_id in pkg_ids]
            pkgs = installer_ctrl.preprocess_raw_pkgs(raw_pkgs)

            # 2.3. Get the list of remote files to download
            # This is a quick way to get the list of unique remote files
            raw_remote_files = list(
                {remote_file.path: remote_file for pkg in pkgs for remote_file in pkg.remote_files}.values()
            )
            remote_files = installer_ctrl.preprocess_raw_remote_files(raw_remote_files)

            # 3. Download remote files
            installer_ctrl.pre_download(remote_files)
            for remote_file in remote_files:
                installer_ctrl.download_file(remote_file)
            installer_ctrl.post_download(remote_files)

            # 4. Install package
            installer_ctrl.pre_install(pkgs)
            for pkg in pkgs:
                installer_ctrl.pre_install_pkg(pkg)
                requisite_ids = self._installed_pkg_sto.get_requisites(candidate_id)
                if not requisite_ids.issubset(augm_candidate1_ids):
                    dependency_ids = self._installed_pkg_sto.get_dependencies(candidate_id, ignore_missing=True)
                    candidate2_ids.discard(candidate_id)
                    candidate2_ids.difference_update(dependency_ids)
            for candidate_id in candidate2_ids:
                installed_pkgs.append(self._installed_pkg_sto[candidate_id])
        return installed_pkgs

class UpgraderController:
    """Base controller for package upgrades."""

    def __init__(self, installable_pkg_sto, installed_pkg_sto) -> None:
        """Initialize the controller.

        Args:
            installable_pkg_sto: Storage for installable packages
            installed_pkg_sto: Storage for installed packages
        """
        pass

    def pre_upgradation(self) -> None:
        """Called before upgrade begins."""
        pass

    def preprocess_raw_upgrade_list(self, raw_upgrade_list: List[Tuple[InstalledPackage, InstallablePackage]]) -> List[Tuple[InstalledPackage, InstallablePackage]]:
        """Process raw upgrade list.

        Args:
            raw_upgrade_list: List of (installed_pkg, installable_pkg) tuples

        Returns:
            Processed list of (installed_pkg, installable_pkg) tuples
        """
        return raw_upgrade_list

    def preprocess_upgrade_list(self, upgrade_list: List[Tuple[InstalledPackage, InstallablePackage]]) -> List[Tuple[InstalledPackage, InstallablePackage, List[InstallablePackage], List[InstalledPackage]]]:
        """Process upgrade list.

        Args:
            upgrade_list: List of (installed_pkg, installable_pkg) tuples

        Returns:
            List of (installed_pkg, installable_pkg, [additional_installable_pkg], [additional_uninstallable_pkg]) tuples
        """
        return [(ed_pkg, able_pkg, [], []) for (ed_pkg, able_pkg) in upgrade_list]

    def preprocess_raw_remote_files(self, raw_remote_files: List) -> List:
        """Process raw remote files.

        Args:
            raw_remote_files: List of remote files to process

        Returns:
            Processed list of remote files
        """
        return [xfile for xfile in raw_remote_files if not xfile.exists()]

    def pre_download(self, remote_files: List) -> None:
        """Called before any files are downloaded.

        Args:
            remote_files: List of files to be downloaded
        """
        pass

    def download_file(self, remote_file) -> None:
        """Download a file.

        Args:
            remote_file: The file to download
        """
        remote_file.download()

    def post_download(self, remote_files: List) -> None:
        """Called after all files have been downloaded.

        Args:
            remote_files: List of downloaded files
        """
        pass

    def pre_upgrade(self, upgrade_specs: List[Tuple[InstalledPackage, InstallablePackage, List[InstallablePackage], List[InstalledPackage]]]) -> None:
        """Called before any packages are upgraded.

        Args:
            upgrade_specs: List of upgrade specifications
        """
        pass

    def pre_upgrade_uninstall_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Called before a package is uninstalled during upgrade.

        Args:
            installed_pkg: The package to uninstall
        """
        pass

    def post_upgrade_uninstall_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Called after a package is uninstalled during upgrade.

        Args:
            installed_pkg: The uninstalled package
        """
        pass

    def pre_upgrade_install_pkg(self, installable_pkg: InstallablePackage) -> None:
        """Called before a package is installed during upgrade.

        Args:
            installable_pkg: The package to install
        """
        pass

    def post_upgrade_install_pkg(self, installable_pkg: InstallablePackage) -> None:
        """Called after a package is installed during upgrade.

        Args:
            installable_pkg: The installed package
        """
        pass

    def pre_upgrade_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Called before a package is upgraded.

        Args:
            installed_pkg: The package to upgrade
        """
        pass

    def post_upgrade_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Called after a package is upgraded.

        Args:
            installed_pkg: The upgraded package
        """
        pass

    def post_upgrade(self, upgrade_specs: List[Tuple[InstalledPackage, InstallablePackage, List[InstallablePackage], List[InstalledPackage]]]) -> None:
        """Called after all packages are upgraded.

        Args:
            upgrade_specs: List of upgrade specifications
        """
        pass

    def post_upgradation(self, exc_value: Optional[Exception]) -> None:
        """Called after upgrade completes or fails.

        Args:
            exc_value: Exception if upgrade failed, or None if successful
        """
        pass

    @classmethod
    def new_factory(cls, *args, **kwargs) -> Callable:
        """Create a new factory function for this controller.

        Args:
            *args: Positional arguments for the controller
            **kwargs: Keyword arguments for the controller

        Returns:
            Factory function that creates controller instances
        """
        def factory(installable_pkg_sto, installed_pkg_sto):
            return cls(installable_pkg_sto, installed_pkg_sto, *args, **kwargs)
        return factory

class DefaultUpgraderController(UpgraderController):
    """Default implementation of upgrader controller."""

    def __init__(self, installable_pkg_sto, installed_pkg_sto, ignore: Optional[List[str]] = None, nodeps: bool = False) -> None:
        """Initialize the controller.

        Args:
            installable_pkg_sto: Storage for installable packages
            installed_pkg_sto: Storage for installed packages
            ignore: List of package IDs to ignore
            nodeps: Whether to ignore dependencies
        """
        self._installable_pkg_sto = installable_pkg_sto
        self._installed_pkg_sto = installed_pkg_sto
        self._ignore = [] if ignore is None else ignore
        self._nodeps = nodeps

    def _upgrade_list_filter_function(self, pkgs: Tuple[InstalledPackage, InstallablePackage]) -> bool:
        """Filter function for upgrade list.

        Args:
            pkgs: Tuple of (installed_pkg, installable_pkg)

        Returns:
            True if the package should be upgraded, False otherwise
        """
        (installed_pkg, installable_pkg) = pkgs
        pkg_id = installed_pkg.pkg_info['id']
        if pkg_id in self._ignore:
            return False

        installed_version = installed_pkg.pkg_info['version']
        installable_version = installable_pkg.pkg_info['version']
        return cmp_version(installable_version, installed_version) > 0

    def preprocess_raw_upgrade_list(self, raw_upgrade_list: List[Tuple[InstalledPackage, InstallablePackage]]) -> List[Tuple[InstalledPackage, InstallablePackage]]:
        """Process raw upgrade list.

        Args:
            raw_upgrade_list: List of (installed_pkg, installable_pkg) tuples

        Returns:
            Filtered list of (installed_pkg, installable_pkg) tuples
        """
        return list(filter(self._upgrade_list_filter_function, raw_upgrade_list))

    def preprocess_upgrade_list(self, upgrade_list: List[Tuple[InstalledPackage, InstallablePackage]]) -> List[Tuple[InstalledPackage, InstallablePackage, List[InstallablePackage], List[InstalledPackage]]]:
        """Process upgrade list.

        Args:
            upgrade_list: List of (installed_pkg, installable_pkg) tuples

        Returns:
            List of (installed_pkg, installable_pkg, [additional_installable_pkg], [additional_uninstallable_pkg]) tuples
        """
        installed_specs = []
        scheduled_pkg_ids = {elem[0].pkg_info['id'] for elem in upgrade_list}
        for installed_pkg, installable_pkg in upgrade_list:
            install_list = []
            if not self._nodeps:
                pkg_id = installed_pkg.pkg_info['id']

                def filter_fun(dep_pkg_id: str) -> bool:
                    return dep_pkg_id not in self._installed_pkg_sto and dep_pkg_id not in scheduled_pkg_ids

                dependencies = self._installable_pkg_sto.get_dependencies(pkg_id, filter_fun=filter_fun)
                for dep_pkg_id in dependencies:
                    scheduled_pkg_ids.add(dep_pkg_id)
                    dep_pkg = self._installable_pkg_sto[dep_pkg_id].clone()
                    dep_pkg.pkg_info['explicit_install'] = False
                    install_list.append(dep_pkg)
            installed_specs.append((installed_pkg, installable_pkg, install_list, []))
        return installed_specs
