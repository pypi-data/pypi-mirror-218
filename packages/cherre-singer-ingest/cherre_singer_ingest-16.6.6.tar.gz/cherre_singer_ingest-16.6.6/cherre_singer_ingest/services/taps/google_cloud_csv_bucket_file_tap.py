from typing import Optional, Iterable, List, Union, Dict
import logging

from cherre_types import BucketFolder, Bucket, FolderPath, BucketFile, File
from cherre_google_clients import GoogleStorageClient
from pathlib import PurePath

from cherre_singer_ingest.services.taps.base_google_cloud_bucket_file_tap import (
    BaseGoogleCloudBucketFileTap,
)
from cherre_singer_ingest.services.streams import (
    CSVFileStream,
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.services.unzip_service_with_bookmarks import (
    UnzipServiceWithBookmarks,
)
from cherre_singer_ingest.value_items.exceptions import TapError


class GoogleCloudCSVBucketFileTap(BaseGoogleCloudBucketFileTap):
    def __init__(
        self,
        google_storage_client: Optional[GoogleStorageClient] = None,
        unzip_service: UnzipServiceWithBookmarks = None,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        pipeline_name: str = "",
    ):
        if config:
            self.delimiter = self.get_config_value(config, "delimiter", ",")
            self.escape_with_quotes = (
                self.get_config_value(config, "escape_with_quotes", "true").lower()
                == "true"
            )

            bucket_name = self.get_config_value(config, "bucket_name")
            folder_in_bucket = self.get_config_value(config, "folder_in_bucket")
            file_name = self.get_config_value(config, "file_name")

            logging.info(
                f"Retrieving records from gs://{bucket_name}/{folder_in_bucket}/{file_name}"
            )
            bucket_folder = BucketFolder(
                bucket=Bucket(bucket_name),
                folders_in_bucket=FolderPath(folder_in_bucket),
            )
            bucket_file = BucketFile(
                file=File.parse(file_name), bucket_folder=bucket_folder
            )

            super().__init__(
                bucket_file=bucket_file,
                google_storage_client=google_storage_client,
                unzip_service=unzip_service,
                catalog=catalog,
                config=config,
                state=state,
                parse_env_config=parse_env_config,
                pipeline_name=pipeline_name,
            )

            self.quote_char = self.get_config_value(config, "quote_char", '"')
            self.encoding = self.get_config_value(config, "encoding", "")
        else:
            raise TapError("No config set for tap")

    def get_streams(self) -> Iterable[BaseFileParsingTapStream]:
        for remote_file in self.get_files():
            yield CSVFileStream(
                remote_file=remote_file,
                delimiter=self.delimiter if self.delimiter else ",",
                quote_char=self.quote_char,
                escape_with_quotes=self.escape_with_quotes,
                encoding=self.encoding,
                pipeline_name=self.pipeline_name,
            )


if __name__ == "__main__":
    GoogleCloudCSVBucketFileTap.cli()
