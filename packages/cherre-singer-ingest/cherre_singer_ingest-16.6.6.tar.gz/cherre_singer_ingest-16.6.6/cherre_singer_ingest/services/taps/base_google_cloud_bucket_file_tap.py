from abc import ABC
from typing import Iterable, List, Union, Dict

from cherre_types import BucketFile
from pathlib import PurePath
from cherre_types import FileSystem, FolderPath
from cherre_google_clients import GoogleStorageClient, GoogleClientFactory

from cherre_singer_ingest.services.taps.base_google_cloud_storage_tap import (
    BaseGoogleCloudStorageTap,
)
from cherre_singer_ingest.services.unzip_service_with_bookmarks import (
    UnzipServiceWithBookmarks,
)
from cherre_singer_ingest.value_items import RemoteFile
from cherre_singer_ingest.factories import RemoteFileURIFactory


class BaseGoogleCloudBucketFileTap(BaseGoogleCloudStorageTap, ABC):
    """
    Reads a file, producing every line as a record
    """

    def __init__(
        self,
        bucket_file: BucketFile,
        google_storage_client: GoogleStorageClient = None,
        unzip_service: UnzipServiceWithBookmarks = None,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        overwrite: bool = False,
        file_system: FileSystem = None,
        download_directory: FolderPath = None,
        pipeline_name: str = "",
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            file_system=file_system,
            download_directory=download_directory,
            google_storage_client=google_storage_client,
            overwrite=overwrite,
            pipeline_name=pipeline_name,
        )

        self.bucket_file = bucket_file

        if not unzip_service:
            unzip_service = UnzipServiceWithBookmarks(pipeline_name=self.pipeline_name)
        self.unzip_service = unzip_service

        if not file_system:
            file_system = FileSystem()
        self.file_system = file_system

        if not google_storage_client:
            google_storage_client = GoogleClientFactory().get_storage_client()
        self.google_storage_client = google_storage_client

        self.uri_factory = RemoteFileURIFactory()

    def get_files(self) -> Iterable[RemoteFile]:
        remote_file = self.download_file_if_doesnt_exist(bucket_file=self.bucket_file)

        if remote_file:
            self.logger.info(f"Unzipping {str(remote_file.local_file)}")
            unzipped = self.unzip_service.unzip_file(remote_file=remote_file)

            for file in unzipped:
                self.logger.info(f"Found unzipped file of {str(file)}")
                yield file
