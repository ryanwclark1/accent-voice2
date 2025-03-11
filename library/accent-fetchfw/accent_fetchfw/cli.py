# cli.py
# Copyright 2025 Accent Communications

"""Command Line Interface tools for accent-fetchfw."""

import logging

import progressbar

from accent_fetchfw.download import ProgressBarHook
from accent_fetchfw.package import (
    DefaultInstallerController,
    DefaultUninstallerController,
    DefaultUpgraderController,
    InstallablePackage,
    InstalledPackage,
    PackageError,
)

logger = logging.getLogger(__name__)


class UserCancellationError(PackageError):
    """Raised when the user cancels an operation.

    This is not an error per se, but is raised when the user
    doesn't want to proceed with an operation.
    """


class CliInstallerController(DefaultInstallerController):
    """Command-line interface for package installation."""

    def preprocess_raw_pkgs(
        self, raw_installable_pkgs: list[InstallablePackage]
    ) -> list[InstallablePackage]:
        """Process the raw packages to be installed.

        Args:
            raw_installable_pkgs: List of packages to process

        Returns:
            Processed list of packages

        Raises:
            UserCancellationError: If the user cancels the installation

        """
        if not self._nodeps:
            print("resolving dependencies...")
        installable_pkgs = super().preprocess_raw_pkgs(raw_installable_pkgs)
        print(f"Targets ({len(installable_pkgs)}):")
        for pkg in installable_pkgs:
            print("    ", pkg)
        print()
        return installable_pkgs

    def pre_download(self, remote_files: list) -> None:
        """Perform pre-download actions.

        Args:
            remote_files: List of files to be downloaded

        Raises:
            UserCancellationError: If the user cancels the installation

        """
        total_dl_size = sum(remote_file.size for remote_file in remote_files)
        print(f"Total Download Size:    {float(total_dl_size) / 1000**2:.2f} MB")
        print()
        rep = input("Proceed with installation? [Y/n] ")
        if rep and rep.lower() != "y":
            raise UserCancellationError

    def download_file(self, remote_file) -> None:
        """Download a file with progress indication.

        Args:
            remote_file: The file to download

        """
        widgets = [
            remote_file.filename,
            ":    ",
            progressbar.FileTransferSpeed(),
            " ",
            progressbar.ETA(),
            " ",
            progressbar.Bar(),
            " ",
            progressbar.Percentage(),
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=remote_file.size)
        remote_file.download([ProgressBarHook(pbar)])

    async def download_file_async(self, remote_file) -> None:
        """Download a file asynchronously with progress indication.

        Args:
            remote_file: The file to download

        """
        widgets = [
            remote_file.filename,
            ":    ",
            progressbar.FileTransferSpeed(),
            " ",
            progressbar.ETA(),
            " ",
            progressbar.Bar(),
            " ",
            progressbar.Percentage(),
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=remote_file.size)
        await remote_file.download_async([ProgressBarHook(pbar)])

    def pre_install_pkg(self, installable_pkg: InstallablePackage) -> None:
        """Perform pre-installation actions for a package.

        Args:
            installable_pkg: The package to install

        """
        print(f"Installing {installable_pkg.pkg_info['id']}...")


class CliUninstallerController(DefaultUninstallerController):
    """Command-line interface for package uninstallation."""

    def pre_uninstall(self, installed_pkgs: list[InstalledPackage]) -> None:
        """Perform pre-uninstallation actions.

        Args:
            installed_pkgs: The packages to uninstall

        Raises:
            UserCancellationError: If the user cancels the uninstallation

        """
        print(f"Remove ({len(installed_pkgs)}):")
        for pkg in installed_pkgs:
            print("    ", pkg)
        print()
        rep = input("Do you want to remove these packages? [Y/n] ")
        if rep and rep.lower() != "y":
            raise UserCancellationError

    def pre_uninstall_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Perform pre-uninstallation actions for a package.

        Args:
            installed_pkg: The package to uninstall

        """
        print(f"Removing {installed_pkg.pkg_info['id']}...")


class CliUpgraderController(DefaultUpgraderController):
    """Command-line interface for package upgrades."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the upgrader controller.

        Args:
            *args: Positional arguments for the parent class
            **kwargs: Keyword arguments for the parent class

        """
        super().__init__(*args, **kwargs)
        self._nothing_to_do = False

    # cli.py (continued)
    def preprocess_upgrade_list(self, upgrade_list: list) -> list:
        """Process the list of packages to upgrade.

        Args:
            upgrade_list: List of packages to upgrade

        Returns:
            Processed list of packages

        """
        if not self._nodeps:
            print("resolving dependencies...")
        installed_specs = super().preprocess_upgrade_list(upgrade_list)
        if not installed_specs:
            print(" there is nothing to do")
            self._nothing_to_do = True
        else:
            installable_pkgs = []
            for installed_spec in installed_specs:
                installable_pkgs.append(installed_spec[1])
                installable_pkgs.extend(installed_spec[2])
            print(f"Targets ({len(installable_pkgs)}):")
            for pkg in installable_pkgs:
                print("    ", pkg)
            print()
        return installed_specs

    def pre_download(self, remote_files: list) -> None:
        """Perform pre-download actions.

        Args:
            remote_files: List of files to be downloaded

        Raises:
            UserCancellationError: If the user cancels the upgrade

        """
        if self._nothing_to_do:
            return

        total_dl_size = sum(remote_file.size for remote_file in remote_files)
        print(f"Total Download Size:    {float(total_dl_size) / 1000**2:.2f} MB")
        print()
        rep = input("Proceed with upgrade? [Y/n] ")
        if rep and rep.lower() != "y":
            raise UserCancellationError

    def download_file(self, remote_file) -> None:
        """Download a file with progress indication.

        Args:
            remote_file: The file to download

        """
        widgets = [
            remote_file.filename,
            ":    ",
            progressbar.FileTransferSpeed(),
            " ",
            progressbar.ETA(),
            " ",
            progressbar.Bar(),
            " ",
            progressbar.Percentage(),
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=remote_file.size)
        remote_file.download([ProgressBarHook(pbar)])

    async def download_file_async(self, remote_file) -> None:
        """Download a file asynchronously with progress indication.

        Args:
            remote_file: The file to download

        """
        widgets = [
            remote_file.filename,
            ":    ",
            progressbar.FileTransferSpeed(),
            " ",
            progressbar.ETA(),
            " ",
            progressbar.Bar(),
            " ",
            progressbar.Percentage(),
        ]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=remote_file.size)
        await remote_file.download_async([ProgressBarHook(pbar)])

    def pre_upgrade_uninstall_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Perform pre-uninstallation actions for a package during upgrade.

        Args:
            installed_pkg: The package to uninstall

        """
        print(f"Removing {installed_pkg.pkg_info['id']}...")

    def pre_upgrade_install_pkg(self, installable_pkg: InstallablePackage) -> None:
        """Perform pre-installation actions for a package during upgrade.

        Args:
            installable_pkg: The package to install

        """
        print(f"Installing {installable_pkg.pkg_info['id']}...")

    def pre_upgrade_pkg(self, installed_pkg: InstalledPackage) -> None:
        """Perform pre-upgrade actions for a package.

        Args:
            installed_pkg: The package to upgrade

        """
        print(f"Upgrading {installed_pkg.pkg_info['id']}...")
