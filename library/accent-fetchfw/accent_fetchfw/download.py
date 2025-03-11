# download.py
# Copyright 2025 Accent Communications

"""Download functionality for fetching remote files."""

import hashlib
import logging
import os
from binascii import b2a_hex
from collections.abc import Callable
from typing import Any, Protocol
from urllib.parse import urlparse

import httpx

from accent_fetchfw.util import FetchfwError

# Configure logging
logger = logging.getLogger(__name__)


class DownloadError(FetchfwError):
    """Base exception for download-related errors."""



class InvalidCredentialsError(DownloadError):
    """Raised when credentials are invalid."""



class CorruptedFileError(DownloadError):
    """Raised when a downloaded file is corrupted."""



class AbortedDownloadError(DownloadError):
    """Raised when a download is explicitly aborted."""



class DownloaderProtocol(Protocol):
    """Protocol defining the interface for downloader objects."""

    def download(self, url: str, timeout: float = 15.0) -> httpx.Response:
        """Download from the specified URL."""
        ...

    async def download_async(self, url: str, timeout: float = 15.0) -> httpx.Response:
        """Download from the specified URL asynchronously."""
        ...


class DefaultDownloader:
    """Default implementation of a downloader using httpx."""

    _TIMEOUT: float = 15.0

    def __init__(self, handlers: list[Any] | None = None) -> None:
        """Initialize the downloader.

        Args:
            handlers: Optional handlers for the downloader

        """
        self._client = httpx.Client(follow_redirects=True)
        self._client.headers.update({"User-agent": "accent-fetchfw/1.0"})

        # Create async client as well
        self._async_client = httpx.AsyncClient(follow_redirects=True)
        self._async_client.headers.update({"User-agent": "accent-fetchfw/1.0"})

        # Initialize any handlers if needed
        if handlers:
            logger.debug("Initializing downloader with %d handlers", len(handlers))

    def download(
        self, url: str | httpx.Request, timeout: float = _TIMEOUT
    ) -> httpx.Response:
        """Open the URL and return a response object.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        Raises:
            InvalidCredentialsError: If authentication fails
            DownloadError: If download fails for other reasons

        """
        try:
            return self._do_download(url, timeout)
        except httpx.HTTPStatusError as e:
            logger.warning(
                "HTTPStatusError while downloading '%s': %s", self._get_url(url), e
            )
            if e.response.status_code == 401:
                raise InvalidCredentialsError(
                    f"unauthorized access to '{self._get_url(url)}'"
                )
            raise DownloadError(str(e))
        except httpx.RequestError as e:
            logger.warning(
                "RequestError while downloading '%s': %s", self._get_url(url), e
            )
            raise DownloadError(str(e))

    async def download_async(
        self, url: str | httpx.Request, timeout: float = _TIMEOUT
    ) -> httpx.Response:
        """Open the URL and return a response object asynchronously.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        Raises:
            InvalidCredentialsError: If authentication fails
            DownloadError: If download fails for other reasons

        """
        try:
            return await self._do_download_async(url, timeout)
        except httpx.HTTPStatusError as e:
            logger.warning(
                "HTTPStatusError while downloading '%s': %s", self._get_url(url), e
            )
            if e.response.status_code == 401:
                raise InvalidCredentialsError(
                    f"unauthorized access to '{self._get_url(url)}'"
                )
            raise DownloadError(str(e))
        except httpx.RequestError as e:
            logger.warning(
                "RequestError while downloading '%s': %s", self._get_url(url), e
            )
            raise DownloadError(str(e))

    def _get_url(self, url: str | httpx.Request) -> str:
        """Return the URL string from either a httpx.Request or string.

        Args:
            url: URL or request object

        Returns:
            URL string

        """
        if isinstance(url, httpx.Request):
            return str(url.url)
        return url

    def _do_download(
        self, url: str | httpx.Request, timeout: float
    ) -> httpx.Response:
        """Perform the actual download.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        """
        return self._client.get(url, timeout=timeout)

    async def _do_download_async(
        self, url: str | httpx.Request, timeout: float
    ) -> httpx.Response:
        """Perform the actual download asynchronously.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        """
        return await self._async_client.get(url, timeout=timeout)

    def __del__(self) -> None:
        """Clean up resources when the downloader is destroyed."""
        self._client.close()
        # We can't await in __del__, but the gc will handle this
        # for the async client


class AuthenticatingDownloader(DefaultDownloader):
    """Downloader that handles authentication."""

    def __init__(self, handlers: list[Any] | None = None) -> None:
        """Initialize the authenticating downloader.

        Args:
            handlers: Optional handlers for the downloader

        """
        super().__init__(handlers)
        self._auth_info: dict[str, tuple[str, str]] = {}

    def add_credentials(self, url: str, username: str, password: str) -> None:
        """Add credentials for a specific URL.

        Args:
            url: URL to authenticate with
            username: Username for authentication
            password: Password for authentication

        """
        # Extract the domain from the URL
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Store credentials
        self._auth_info[domain] = (username, password)

        logger.debug("Added credentials for %s", domain)

    def _do_download(
        self, url: str | httpx.Request, timeout: float
    ) -> httpx.Response:
        """Perform the actual download with auth if needed.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        """
        # Try to find matching auth info
        url_str = self._get_url(url)
        parsed_url = urlparse(url_str)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        auth = None
        if domain in self._auth_info:
            auth = httpx.BasicAuth(*self._auth_info[domain])

        # Make the request with auth if available
        return self._client.get(url, auth=auth, timeout=timeout)

    async def _do_download_async(
        self, url: str | httpx.Request, timeout: float
    ) -> httpx.Response:
        """Perform the actual download with auth if needed asynchronously.

        Args:
            url: URL to download from
            timeout: Timeout in seconds

        Returns:
            A response object

        """
        # Try to find matching auth info
        url_str = self._get_url(url)
        parsed_url = urlparse(url_str)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        auth = None
        if domain in self._auth_info:
            auth = httpx.BasicAuth(*self._auth_info[domain])

        # Make the request with auth if available
        return await self._async_client.get(url, auth=auth, timeout=timeout)


class BaseRemoteFile:
    """A remote file that can be downloaded."""

    _BLOCK_SIZE: int = 4096

    def __init__(
        self,
        url: str,
        downloader: DownloaderProtocol,
        hook_factories: list[Callable[[], "DownloadHook"]] | None = None,
    ) -> None:
        """Initialize the remote file.

        Args:
            url: The URL/object to pass to the downloader
            downloader: The file downloader
            hook_factories: A list of callable objects that return download hooks

        """
        self._url = url
        self._downloader = downloader
        self._hook_factories = list(hook_factories) if hook_factories else []

    async def download_async(self, supp_hooks: list["DownloadHook"] = None) -> None:
        """Download the file asynchronously and run it through the hooks.

        Args:
            supp_hooks: Additional hooks to use during download

        Raises:
            DownloadError: If download fails

        """
        if supp_hooks is None:
            supp_hooks = []

        logger.debug("Downloading %s asynchronously", self._url)
        hooks = supp_hooks + [factory() for factory in self._hook_factories]
        last_started_idx = 0

        try:
            # Start all hooks
            for hook in hooks:
                hook.start()
                last_started_idx += 1

            # Download and process the file
            async with self._downloader.download_async(self._url) as response:
                async for data in response.aiter_bytes(chunk_size=self._BLOCK_SIZE):
                    for hook in hooks:
                        hook.update(data)

            # Complete all hooks
            for hook in reversed(hooks):
                hook.complete()

        except Exception as e:
            # Preserve traceback info while handling hook failures
            try:
                raise
            finally:
                hook_idx = last_started_idx
                while hook_idx:
                    hook_idx -= 1
                    try:
                        hooks[hook_idx].fail(e)
                    except Exception:
                        logger.error("hook.fail raised an exception", exc_info=True)
        finally:
            # Always stop all started hooks
            hook_idx = last_started_idx
            while hook_idx:
                hook_idx -= 1
                try:
                    hooks[hook_idx].stop()
                except Exception:
                    logger.error("hook.stop raised an exception", exc_info=True)

    def download(self, supp_hooks: list["DownloadHook"] = None) -> None:
        """Download the file and run it through the hooks.

        Args:
            supp_hooks: Additional hooks to use during download

        Raises:
            DownloadError: If download fails

        """
        if supp_hooks is None:
            supp_hooks = []

        logger.debug("Downloading %s", self._url)
        hooks = supp_hooks + [factory() for factory in self._hook_factories]
        last_started_idx = 0

        try:
            # Start all hooks
            for hook in hooks:
                hook.start()
                last_started_idx += 1

            # Download and process the file
            with self._downloader.download(self._url) as response:
                for data in response.iter_bytes(chunk_size=self._BLOCK_SIZE):
                    for hook in hooks:
                        hook.update(data)

            # Complete all hooks
            for hook in reversed(hooks):
                hook.complete()

        except Exception as e:
            # Preserve traceback info while handling hook failures
            try:
                raise
            finally:
                hook_idx = last_started_idx
                while hook_idx:
                    hook_idx -= 1
                    try:
                        hooks[hook_idx].fail(e)
                    except Exception:
                        logger.error("hook.fail raised an exception", exc_info=True)
        finally:
            # Always stop all started hooks
            hook_idx = last_started_idx
            while hook_idx:
                hook_idx -= 1
                try:
                    hooks[hook_idx].stop()
                except Exception:
                    logger.error("hook.stop raised an exception", exc_info=True)


class RemoteFile:
    """A BaseRemoteFile with additional attributes."""

    def __init__(self, path: str, size: int, base_remote_file: BaseRemoteFile) -> None:
        """Initialize the remote file.

        Args:
            path: The path where the file will be written
            size: The size of the remote file
            base_remote_file: The underlying remote file

        Note:
            You probably want to use the "new_remote_file" method
            instead of directly using this constructor.

        """
        self.path = path
        self.size = size
        self._base_remote_file = base_remote_file

    @property
    def filename(self) -> str:
        """Get the filename of the remote file.

        Returns:
            The filename

        """
        return os.path.basename(self.path)

    def exists(self) -> bool:
        """Check if the file already exists.

        Returns:
            True if the file exists, False otherwise

        """
        return os.path.isfile(self.path)

    def download(self, supp_hooks: list["DownloadHook"] = None) -> None:
        """Download the file.

        Args:
            supp_hooks: Additional hooks to use during download

        Raises:
            DownloadError: If download fails

        """
        if supp_hooks is None:
            supp_hooks = []
        self._base_remote_file.download(supp_hooks)

    async def download_async(self, supp_hooks: list["DownloadHook"] = None) -> None:
        """Download the file asynchronously.

        Args:
            supp_hooks: Additional hooks to use during download

        Raises:
            DownloadError: If download fails

        """
        if supp_hooks is None:
            supp_hooks = []
        await self._base_remote_file.download_async(supp_hooks)

    @classmethod
    def new_remote_file(
        cls,
        path: str,
        size: int,
        url: str,
        downloader: DownloaderProtocol,
        hook_factories: list[Callable[[], "DownloadHook"]] = None,
    ) -> "RemoteFile":
        """Create a new RemoteFile instance.

        Args:
            path: The path where the file will be written
            size: The size of the remote file
            url: The URL to download from
            downloader: The downloader to use
            hook_factories: Factories for creating download hooks

        Returns:
            A new RemoteFile instance

        """
        if hook_factories is None:
            hook_factories = []
        hook_factories = [*hook_factories, WriteToFileHook.create_factory(path)]
        base_remote_file = BaseRemoteFile(url, downloader, hook_factories)
        return cls(path, size, base_remote_file)


class DownloadHook:
    """Base class for download hooks."""

    def start(self) -> None:
        """Called just before the download is started."""

    def update(self, data: bytes) -> None:
        """Called every time a chunk of data is received.

        Args:
            data: The data chunk received

        """

    def complete(self) -> None:
        """Called just after the download has completed."""

    def fail(self, exc_value: Exception) -> None:
        """Called if the download fails.

        Args:
            exc_value: The exception that caused the failure

        Note:
            This method MUST NOT raise an exception.

        """

    def stop(self) -> None:
        """Called just after the download is stopped.

        Note:
            This method MUST NOT raise an exception.

        """


class WriteToFileHook(DownloadHook):
    """Hook that writes download data to a file."""

    def __init__(self, filename: str) -> None:
        """Initialize the hook.

        Args:
            filename: The filename to write to

        """
        super().__init__()
        self._filename = filename
        self._tmp_filename = filename + ".tmp"
        self._fobj = None
        self._renamed = False

    def start(self) -> None:
        """Start the hook by opening the output file."""
        self._fobj = open(self._tmp_filename, "wb")

    def update(self, data: bytes) -> None:
        """Write data to the file.

        Args:
            data: The data to write

        """
        self._fobj.write(data)

    def complete(self) -> None:
        """Complete the download by closing the file and renaming it."""
        self._fobj.close()
        os.rename(self._tmp_filename, self._filename)
        self._renamed = True

    def fail(self, exc_value: Exception) -> None:
        """Handle failure by closing and removing temporary files.

        Args:
            exc_value: The exception that caused the failure

        """
        self._fobj.close()
        try:
            filename = self._filename if self._renamed else self._tmp_filename
            os.remove(filename)
        except OSError as e:
            logger.error("error while removing '%s': %s", filename, e)

    @classmethod
    def create_factory(cls, filename: str) -> Callable[[], "WriteToFileHook"]:
        """Create a factory function for this hook.

        Args:
            filename: The filename to write to

        Returns:
            A factory function that creates WriteToFileHook instances

        """

        def factory() -> WriteToFileHook:
            return cls(filename)

        return factory


class SHA1Hook(DownloadHook):
    """Hook that verifies the SHA1 checksum of downloaded data."""

    def __init__(self, sha1sum: bytes) -> None:
        """Initialize the hook.

        Args:
            sha1sum: The expected SHA1 checksum (raw bytes, not hex)

        """
        super().__init__()
        self._sha1sum = sha1sum
        self._hash = None

    def start(self) -> None:
        """Start the hook by initializing the hash object."""
        self._hash = hashlib.sha1()

    def update(self, data: bytes) -> None:
        """Update the hash with received data.

        Args:
            data: The data to hash

        """
        self._hash.update(data)

    def complete(self) -> None:
        """Verify the hash matches the expected value.

        Raises:
            CorruptedFileError: If the checksums don't match

        """
        sha1sum = self._hash.digest()
        if sha1sum != self._sha1sum:
            raise CorruptedFileError(
                f"sha1sum mismatch: {b2a_hex(sha1sum)} instead of {b2a_hex(self._sha1sum)}"
            )

    @classmethod
    def create_factory(cls, sha1sum: bytes) -> Callable[[], "SHA1Hook"]:
        """Create a factory function for this hook.

        Args:
            sha1sum: The expected SHA1 checksum

        Returns:
            A factory function that creates SHA1Hook instances

        """

        def factory() -> SHA1Hook:
            return cls(sha1sum)

        return factory


class ProgressBarHook(DownloadHook):
    """Hook that updates a progress bar during download."""

    def __init__(self, pbar: Any) -> None:
        """Initialize the hook.

        Args:
            pbar: The progress bar to update

        """
        super().__init__()
        self._pbar = pbar
        self._size = 0

    def start(self) -> None:
        """Start the progress bar."""
        self._pbar.start()

    def update(self, data: bytes) -> None:
        """Update the progress bar with the received data.

        Args:
            data: The received data

        """
        self._size += len(data)
        self._pbar.update(self._size)

    def complete(self) -> None:
        """Mark the progress bar as complete."""
        self._pbar.finish()


class AbortHook(DownloadHook):
    """Hook that can be used to abort a download."""

    def __init__(self) -> None:
        """Initialize the hook."""
        super().__init__()
        self._abort = False

    def update(self, data: bytes) -> None:
        """Check if the download should be aborted.

        Args:
            data: The received data

        Raises:
            AbortedDownloadError: If the download should be aborted

        """
        if self._abort:
            logger.info("explicitly aborting download")
            raise AbortedDownloadError

    def abort_download(self) -> None:
        """Schedule the download to be aborted."""
        logger.info("scheduling download abortion")
        self._abort = True


def new_httpx_client(
    proxies: dict[str, str] | None = None, auth: httpx.Auth | None = None
) -> httpx.Client:
    """Create a new httpx client with the specified configuration.

    Args:
        proxies: Optional proxy configuration
        auth: Optional authentication information

    Returns:
        A configured httpx client

    """
    # Configure client with proxies if provided
    client_kwargs = {}
    if proxies:
        client_kwargs["proxies"] = proxies

    # Configure authentication if provided
    if auth:
        client_kwargs["auth"] = auth

    return httpx.Client(**client_kwargs)


def new_async_httpx_client(
    proxies: dict[str, str] | None = None, auth: httpx.Auth | None = None
) -> httpx.AsyncClient:
    """Create a new async httpx client with the specified configuration.

    Args:
        proxies: Optional proxy configuration
        auth: Optional authentication information

    Returns:
        A configured async httpx client

    """
    # Configure client with proxies if provided
    client_kwargs = {}
    if proxies:
        client_kwargs["proxies"] = proxies

    # Configure authentication if provided
    if auth:
        client_kwargs["auth"] = auth

    return httpx.AsyncClient(**client_kwargs)


def new_downloaders(
    proxies: dict[str, str] | None = None,
) -> dict[str, DownloaderProtocol]:
    """Create standard downloaders with the specified proxy configuration.

    Args:
        proxies: Optional proxy configuration

    Returns:
        A dictionary of downloaders

    """
    auth = AuthenticatingDownloader()
    default = DefaultDownloader()
    return {"auth": auth, "default": default}
