import click
import logging
from cherre_google_clients import GoogleClientFactory, GoogleStorageClient
from cherre_types import BucketFolder, Bucket, FolderPath

from cherre_singer_ingest.value_items import RecordStream, TargetError
from cherre_singer_ingest.services.targets.base_cherre_target import BaseCherreTarget
from cherre_singer_ingest.services.stream_writers import (
    AvroStreamWriter,
)


class CherreBigQueryExternalDataTarget(BaseCherreTarget):
    def __init__(
        self,
        project_id: str,
        storage_client: GoogleStorageClient = None,
        file_writer: AvroStreamWriter = None,
        store_bookmarks: bool = True,
        destination_dataset: str = "raw",
        include_stream_name: bool = False,
    ):
        super().__init__(
            store_bookmarks=store_bookmarks,
            destination_dataset=destination_dataset,
            include_stream_name=include_stream_name,
        )
        if not storage_client:
            storage_client = GoogleClientFactory().get_storage_client()
        self.storage_client = storage_client

        self.bucket = Bucket(project_id)
        self.base_path = FolderPath(f"bq_external_data/{self.destination_dataset}/")

        if not file_writer:
            file_writer = AvroStreamWriter(logger=self.logger)
        self.file_writer = file_writer

    def write_records(self, records: RecordStream) -> int:
        per_stream_results, num = self.file_writer.write_records_to_file(
            records=records, schema_messages=self.schema_messages
        )

        # upload the files to the correct folder to be picked up
        for per_stream_result in per_stream_results:
            folder = self.base_path
            if per_stream_result.sub_folder:
                folder = folder.add_sub_folder(str(per_stream_result.sub_folder))
            bucket_folder = BucketFolder(bucket=self.bucket, folders_in_bucket=folder)
            self.storage_client.upload_file_to_bucket_folder(
                source=per_stream_result.file,
                destination=bucket_folder,
                base_path=folder,
            )

        return num


@click.option(
    "--source_file",
    required=False,
    default=None,
    help="Tells the target to read from the provided file, instead of STDIN",
)
@click.option("--config", required=True, help="path of the config file")
@click.command()
def main(config: str, source_file: str = None):
    try:
        config_values = CherreBigQueryExternalDataTarget.load_config_file(
            config, ["project_id"]
        )

        store_bookmarks = False
        if ("store_bookmarks" in config_values) and (
            str(config_values["store_bookmarks"]).lower().strip() == "true"
        ):
            store_bookmarks = True
        destination_dataset = config_values.get("destination_dataset", "raw")

        include_stream_name = False
        if ("include_stream_name" in config_values) and (
            str(config_values["include_stream_name"]).lower().strip() == "true"
        ):
            include_stream_name = True

        target = CherreBigQueryExternalDataTarget(
            project_id=config_values["project_id"],
            store_bookmarks=store_bookmarks,
            destination_dataset=destination_dataset,
            include_stream_name=include_stream_name,
        )

        target.execute(source_file=source_file)
    except TargetError:
        raise
    except Exception as e:
        logging.error(f"{e}")
        raise TargetError(str(e))


if __name__ == "__main__":
    main()
