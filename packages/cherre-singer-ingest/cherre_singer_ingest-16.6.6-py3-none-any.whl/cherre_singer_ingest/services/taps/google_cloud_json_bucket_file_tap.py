import logging
from typing import Iterable, List, Union, Dict
from pathlib import PurePath

from cherre_types import BucketFolder, File, Bucket, FolderPath, BucketFile

from cherre_singer_ingest.services.taps.base_google_cloud_bucket_file_tap import (
    BaseGoogleCloudBucketFileTap,
)
from cherre_singer_ingest.services.streams.json_file_stream import JSONFileStream
from cherre_singer_ingest.services.streams import BaseFileParsingTapStream


class GoogleCloudBucketJSONFileTap(BaseGoogleCloudBucketFileTap):
    """
    Reads a file, producing every line as a record
    """

    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        pipeline_name: str = "",
    ):
        if not config:
            raise ValueError()

        config_values = GoogleCloudBucketJSONFileTap.load_config_file(
            config[0], ["source_file", "table_name"]
        )
        table_name = (
            None
            if config_values["table_name"].lower() == "none"
            else config_values["table_name"]
        )

        source_file = config_values["source_file"]

        encoding = config_values["encoding"] if "encoding" in config_values else ""

        bucket_file = BucketFile.parse(source_file)

        bucket_name, folder_in_bucket, file_name = (
            str(bucket_file.bucket_folder.bucket_name),
            str(bucket_file.bucket_folder.folders_in_bucket),
            str(bucket_file.file.name_with_extension),
        )

        logging.info(
            f"Retrieving records from gs://{bucket_name}/{folder_in_bucket}/{file_name}"
        )

        bucket_folder = BucketFolder(
            bucket=Bucket(bucket_name), folders_in_bucket=FolderPath(folder_in_bucket)
        )
        bucket_file = BucketFile(file=File(file_name), bucket_folder=bucket_folder)

        super().__init__(
            bucket_file=bucket_file,
            config=config,
            state=state,
            catalog=catalog,
            parse_env_config=parse_env_config,
            pipeline_name=pipeline_name,
        )
        self.stream_name = table_name if table_name else self.bucket_file.file.name
        self.encoding = encoding

    def get_streams(self) -> Iterable[BaseFileParsingTapStream]:
        for remote_file in self.get_files():
            yield JSONFileStream(
                remote_file=remote_file,
                encoding=self.encoding,
                pipeline_name=self.pipeline_name,
            )


if __name__ == "__main__":
    GoogleCloudBucketJSONFileTap.cli()
