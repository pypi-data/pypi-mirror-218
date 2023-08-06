from typing import Iterable, Union, List, Dict
from pathlib import PurePath

from cherre_types import (
    BucketFolder,
    File,
    Bucket,
    FolderPath,
    BucketFile,
    FileSystem,
)
from cherre_google_clients import GoogleStorageClient

from cherre_singer_ingest.services.taps.base_google_cloud_bucket_file_tap import (
    BaseGoogleCloudBucketFileTap,
)
from cherre_singer_ingest.services.streams import (
    ShapefileFileStream,
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.value_items import RemoteFile


class GoogleCloudBucketShapefileFileTap(BaseGoogleCloudBucketFileTap):
    """
    Reads a file, producing every line as a record
    """

    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        overwrite: bool = False,
        file_system: FileSystem = None,
        download_directory: FolderPath = None,
        google_storage_client: GoogleStorageClient = None,
        pipeline_name: str = "",
    ):
        if not config:
            raise ValueError()

        config_values = GoogleCloudBucketShapefileFileTap.load_config_file(
            config[0], ["source_file", "table_name"]
        )
        table_name = (
            None
            if config_values["table_name"].lower() == "none"
            else config_values["table_name"]
        )

        source_file = config_values["source_file"]
        bucket_file = BucketFile.parse(source_file)

        bucket_name, folder_in_bucket, file_name = (
            str(bucket_file.bucket_folder.bucket_name),
            str(bucket_file.bucket_folder.folders_in_bucket),
            str(bucket_file.file.name_with_extension),
        )

        self.bucket_folder = BucketFolder(
            bucket=Bucket(bucket_name), folders_in_bucket=FolderPath(folder_in_bucket)
        )
        self.bucket_file = BucketFile(
            file=File(file_name), bucket_folder=self.bucket_folder
        )

        super().__init__(
            config=config,
            state=state,
            catalog=catalog,
            parse_env_config=parse_env_config,
            bucket_file=bucket_file,
            overwrite=overwrite,
            file_system=file_system,
            download_directory=download_directory,
            google_storage_client=google_storage_client,
            pipeline_name=pipeline_name,
        )

        self.stream_name = table_name if table_name else self.bucket_file.file.name
        self.logger.info(
            f"Retrieving records from gs://{bucket_name}/{folder_in_bucket}/{file_name}"
        )

    def get_files(self) -> Iterable[RemoteFile]:
        remote_file = self.download_file_if_doesnt_exist(bucket_file=self.bucket_file)

        # Not unzipping the file because the `ShapefileFileStream` requires the files to be zipped!
        if remote_file:
            yield remote_file

    def get_streams(self) -> Iterable[BaseFileParsingTapStream]:
        for remote_file in self.get_files():
            yield ShapefileFileStream(
                remote_file=remote_file, pipeline_name=self.pipeline_name
            )


if __name__ == "__main__":
    GoogleCloudBucketShapefileFileTap.cli()
