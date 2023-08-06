"""
NOTE: This is deprecated. This target should not be used.

This target is removed from `run_custom_image_tap` in "14.0.0".
If this tap is still in use, please update to `CherreBigQueryExternalDataTarget`.
"""

from datetime import datetime
import logging
from typing import List, Optional

import click

from cherre_types import FilePath, BigQueryTable
from cherre_domain import BucketFactory
from cherre_google_clients import (
    GoogleStorageClient,
    GoogleBigQueryClient,
    GoogleClientFactory,
)

from cherre_singer_ingest.value_items import TargetError, RecordStream
from cherre_singer_ingest.services.stream_writers import (
    AvroStreamWriter,
)
from cherre_singer_ingest.services.targets.base_cherre_target import BaseCherreTarget
from cherre_singer_ingest.repositories import BigQueryIngestStateRepository


class CherreParsedDataLakeTarget(BaseCherreTarget):
    """
    Target which expects the tap to bring column data in, and avoids the ELT parsing need
    Each stream will be taken to its own AVRO file, loaded to an eph schema, then loaded to a table in source

    """

    def __init__(
        self,
        project_id: str,
        data_provider_name: str,
        run_time: datetime = None,
        table_name_override: str = None,  # if set, use this value for the table name instead of the stream
        storage_client: GoogleStorageClient = None,
        big_query_client: GoogleBigQueryClient = None,
        file_writer: AvroStreamWriter = None,
        ignore_schema: bool = False,
        lower_schema_case: bool = False,
        state_repository: BigQueryIngestStateRepository = None,
        store_bookmarks: bool = True,
        destination_dataset: str = "raw",
    ):
        super().__init__(
            ignore_schema=ignore_schema,
            state_repository=state_repository,
            store_bookmarks=store_bookmarks,
            destination_dataset=destination_dataset,
        )

        self.project_id = project_id

        if not storage_client:
            storage_client = GoogleClientFactory().get_storage_client()
        self.storage_client = storage_client

        if not big_query_client:
            big_query_client = GoogleClientFactory().get_big_query_client(
                project_id=project_id
            )
        self.big_query_client = big_query_client

        if not run_time:
            run_time = datetime.now()
        self.run_time = run_time

        bucket_factory = BucketFactory(
            project_id=self.project_id,
            data_provider_name=data_provider_name,
            run_time=self.run_time,
        )
        bucket_folder = bucket_factory.get_converted_bucket_folder()
        self.bucket_folder = bucket_folder

        self.table_name_override = table_name_override

        if not file_writer:
            file_writer = AvroStreamWriter(
                lowercase_schema=lower_schema_case, logger=self.logger
            )
        self.file_writer = file_writer

    def write_records(self, records: RecordStream) -> int:
        per_stream_results, total_num = self.file_writer.write_records_to_file(
            records=records,
            schema_messages=self.schema_messages,
            table_name_override=self.table_name_override,
        )

        for psr in per_stream_results:
            self.upload_file_to_bq(local_file=psr.file, column_names=psr.column_names)

        return total_num

    def upload_file_to_bq(
        self, local_file: FilePath, column_names: Optional[List[str]] = None
    ) -> BigQueryTable:
        uploaded_file = self.storage_client.upload_file_to_bucket_folder(
            source=local_file, destination=self.bucket_folder
        )

        if not self.big_query_client.does_dataset_exist(
            project_id=self.project_id, dataset=self.destination_dataset
        ):
            self.big_query_client.create_dataset(
                project_id=self.project_id, dataset=self.destination_dataset
            )

        table_name = (
            self.table_name_override
            if self.table_name_override
            else local_file.file.name
        )
        table = BigQueryTable(
            project_id=self.project_id,
            dataset=self.destination_dataset,
            table=table_name,
        )

        self.big_query_client.upload_avro_data_to_big_query(
            bucket_file=uploaded_file,
            destination_table=table,
            column_names=column_names,
        )

        return table


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
        config_values = CherreParsedDataLakeTarget.load_config_file(
            config, ["project_id", "data_provider_name"]
        )
        table_name_override = (
            config_values["table_name"] if "table_name" in config_values else None
        )

        lower_schema_case = (
            config_values["lower_schema_case"]
            if "lower_schema_case" in config_values
            else False
        )

        store_bookmarks = False
        if ("store_bookmarks" in config_values) and (
            str(config_values["store_bookmarks"]).lower().strip() == "true"
        ):
            store_bookmarks = True
        destination_dataset = config_values.get("destination_dataset", "raw")

        target = CherreParsedDataLakeTarget(
            project_id=config_values["project_id"],
            data_provider_name=config_values["data_provider_name"],
            table_name_override=table_name_override,
            lower_schema_case=lower_schema_case,
            store_bookmarks=store_bookmarks,
            destination_dataset=destination_dataset,
        )

        target.execute(source_file=source_file)
    except TargetError:
        raise
    except Exception as e:
        logging.error(f"{e}")
        raise TargetError(str(e))


if __name__ == "__main__":
    main()
