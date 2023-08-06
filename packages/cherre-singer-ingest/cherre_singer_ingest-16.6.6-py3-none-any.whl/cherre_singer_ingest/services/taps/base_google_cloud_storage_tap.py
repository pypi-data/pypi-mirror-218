from abc import ABC
from typing import List, Union, Dict, Optional
from pathlib import PurePath

from cherre_types import BucketFile, FilePath, FolderPath, FileSystem
from cherre_google_clients import GoogleStorageClient, GoogleClientFactory
from cherre_singer_ingest.services.taps.base_file_parsing_tap import BaseFileParsingTap
from cherre_singer_ingest.factories import RemoteFileURIFactory
from cherre_singer_ingest.value_items import RemoteFile


class BaseGoogleCloudStorageTap(BaseFileParsingTap, ABC):
    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        overwrite: bool = False,
        download_directory: FilePath = None,
        file_system: FileSystem = None,
        google_storage_client: GoogleStorageClient = None,
        pipeline_name: str = "",
        remote_file_uri_factory: RemoteFileURIFactory = None,
        num_workers: int = 1,
        worker_id: int = 0,
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            pipeline_name=pipeline_name,
            num_workers=num_workers,
            worker_id=worker_id,
        )

        self.overwrite = overwrite

        if not download_directory:
            download_directory = FolderPath.parse("./.downloaded")
        self.download_directory = download_directory

        if not file_system:
            file_system = FileSystem()
        self.file_system = file_system

        if not google_storage_client:
            google_storage_client = GoogleClientFactory().get_storage_client()
        self.google_storage_client = google_storage_client

        if not remote_file_uri_factory:
            remote_file_uri_factory = RemoteFileURIFactory()
        self.remote_file_uri_factory = remote_file_uri_factory

    def download_file_if_doesnt_exist(
        self, bucket_file: BucketFile
    ) -> Optional[RemoteFile]:
        local_file = FilePath(file=bucket_file.file, path=self.download_directory)

        if self.overwrite:
            if self.file_system.file_exists(local_file):
                self.file_system.delete_file(local_file)

        remote_uri = self.remote_file_uri_factory.get_google_bucket_file_uri(
            bucket_file
        )
        remote_file = RemoteFile(local_file=local_file, remote_uri=remote_uri)
        if self.should_remote_file_be_used(remote_file=remote_file):
            if not self.file_system.file_exists(local_file):
                self.logger.info(f"Downloading file {bucket_file} to {str(local_file)}")
                local_file = self.google_storage_client.download_bucket_file(
                    source=bucket_file, destination=self.download_directory
                )
            else:
                self.logger.info(
                    f"File {local_file} already exists in the local system, skipping"
                )
            return RemoteFile(remote_uri=remote_uri, local_file=local_file)
        else:
            # Since remote file should not be used, returning None!
            return None
