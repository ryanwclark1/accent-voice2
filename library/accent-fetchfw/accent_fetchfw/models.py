# models.py
# Copyright 2025 Accent Communications

"""Pydantic models for the accent-fetchfw package."""


from pydantic import BaseModel, Field


class RemoteFileConfig(BaseModel):
    """Configuration for a remote file.

    Attributes:
        path: Path where the file will be stored
        size: Size of the remote file in bytes
        url: URL to download the file from
        filename: Name of the file (derived from URL if not specified)
        sha1sum: SHA1 checksum of the file for verification
        downloader: Name of the downloader to use

    """

    path: str
    size: int
    url: str
    filename: str | None = None
    sha1sum: bytes
    downloader: str = "default"


class PackageInfo(BaseModel):
    """Information about a package.

    Attributes:
        id: ID of the package
        version: Version of the package
        description: Description of the package
        depends: List of package IDs this package depends on
        files: List of files installed by the package (for installed packages)
        explicit_install: Whether the package was explicitly installed

    """

    id: str
    version: str
    description: str
    depends: list[str] = Field(default_factory=list)
    files: list[str] | None = None
    explicit_install: bool | None = None


class DownloadProgress(BaseModel):
    """Download progress information.

    Attributes:
        filename: Name of the file being downloaded
        size: Total size of the file in bytes
        downloaded: Number of bytes downloaded
        percentage: Percentage of the file downloaded

    """

    filename: str
    size: int
    downloaded: int = 0
    percentage: float = 0.0
