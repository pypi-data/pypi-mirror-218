from abc import ABC
from typing import Iterable, Union, List, Dict

from pathlib import PurePath
from cherre_types import BucketFolder, FolderPath, FileSystem
from cherre_google_clients import GoogleStorageClient

from cherre_singer_ingest.services.taps.base_google_cloud_storage_tap import (
    BaseGoogleCloudStorageTap,
)
from cherre_singer_ingest.services.unzip_service_with_bookmarks import (
    UnzipServiceWithBookmarks,
)
from cherre_singer_ingest.services.common import file_name_match_regex
from cherre_singer_ingest.value_items import RemoteFile
from cherre_singer_ingest.factories import RemoteFileURIFactory


class BaseGoogleCloudBucketFolderTap(BaseGoogleCloudStorageTap, ABC):
    """
    For every file in a bucket folder, get it and present it into a stream
    """

    def __init__(
        self,
        bucket_folder: BucketFolder,
        google_storage_client: GoogleStorageClient = None,
        unzip_service: UnzipServiceWithBookmarks = None,
        filter_regex: str = "",
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        download_directory: FolderPath = None,
        file_system: FileSystem = None,
        overwrite: bool = False,
        pipeline_name: str = "",
        remote_uri_factory: RemoteFileURIFactory = None,
        num_workers: int = 1,
        worker_id: int = 0,
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            download_directory=download_directory,
            file_system=file_system,
            google_storage_client=google_storage_client,
            overwrite=overwrite,
            pipeline_name=pipeline_name,
            num_workers=num_workers,
            worker_id=worker_id,
        )

        self.bucket_folder = bucket_folder
        self._downloaded_file = None

        if not unzip_service:
            unzip_service = UnzipServiceWithBookmarks(pipeline_name=self.pipeline_name)
        self.unzip_service = unzip_service

        self.filter_regex = filter_regex

        if not remote_uri_factory:
            remote_uri_factory = RemoteFileURIFactory()
        self.remote_file_uri_factory = remote_uri_factory

    def get_files(self) -> Iterable[RemoteFile]:
        bucket_files = self.google_storage_client.list_files_in_bucket_folder(
            self.bucket_folder
        )

        for bf in bucket_files:
            if not self.filter_regex or file_name_match_regex(
                file_pattern=self.filter_regex, file_name=str(bf.file)
            ):
                remote_file = self.download_file_if_doesnt_exist(bucket_file=bf)
                if remote_file:
                    unzipped = self.unzip_service.unzip_file(remote_file=remote_file)
                    yield from unzipped
