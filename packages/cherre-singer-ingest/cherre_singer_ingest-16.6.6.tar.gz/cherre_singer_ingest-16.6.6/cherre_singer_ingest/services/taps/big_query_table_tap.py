from typing import Any, Dict, Iterable, List, Union
from pathlib import PurePath

from singer import Schema
from cherre_types import BigQueryTable
from cherre_google_clients import GoogleClientFactory, GoogleBigQueryClient
from google.cloud.bigquery import SchemaField

from cherre_singer_ingest.services.taps.base_tap import BaseTap
from cherre_singer_ingest.services.streams import BaseTapStream


def convert_schema_field(schema_field: SchemaField) -> Dict[str, Any]:
    ret: Dict[str, Any] = {}
    # FIXME for date times, we need to change this to string and a format (see JSON Schema docs)

    field_type = schema_field.field_type.lower()
    if field_type == "date":
        ret["format"] = "date"
        field_type = "string"
    elif field_type == "datetime":
        ret["format"] = "datetime"
        field_type = "string"
    elif field_type == "time":
        ret["format"] = "time"
        field_type = "string"
    else:
        field_type = schema_field.field_type.lower()

    if schema_field.is_nullable:
        ret["type"] = [field_type, "null"]
    else:
        ret["type"] = [field_type]

    return ret


class BigQueryTableTap(BaseTap):
    def __init__(
        self,
        bq_client: GoogleBigQueryClient = None,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        pipeline_name: str = "",
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            pipeline_name=pipeline_name,
        )

        if config and len(config) > 0:
            config_values = BigQueryTableTap.load_config_file(
                config[0], ["source_table"]
            )
            source_table = config_values["source_table"]
            table = BigQueryTable.parse(source_table)

            self.batch_size = (
                int(config_values["batch_size"])
                if "batch_size" in config_values
                else 100000
            )
            self.source_table = table
            self.bq_client = bq_client

    def get_streams(self) -> Iterable[BaseTapStream]:
        yield BigQueryTableTapStream(
            source_table=self.source_table,
            batch_size=self.batch_size,
            bq_client=self.bq_client,
            pipeline_name=self.pipeline_name,
        )


class BigQueryTableTapStream(BaseTapStream):
    def __init__(
        self,
        source_table: BigQueryTable,
        batch_size: int = 100000,
        bq_client: GoogleBigQueryClient = None,
        pipeline_name: str = "",
    ):
        super().__init__(source_table.table)
        self.source_table = source_table
        if not bq_client:
            client_factory = GoogleClientFactory()
            bq_client = client_factory.get_big_query_client(source_table.project_id)
        self.bq_client = bq_client
        self.batch_size = batch_size

    def get_records(self, partition=None):
        # FIXME we need to cycle through the max size of results, until we get nothing
        running = True
        num_returned = 0
        while running:
            self.logger.debug(
                f"Getting rows from {num_returned} to {num_returned + self.batch_size}"
            )
            query = f"SELECT * FROM {self.source_table.get_sql_string()} LIMIT {self.batch_size} OFFSET {num_returned}"
            job = self.bq_client.google_bq_client.query(query=query)

            results = job.result()
            running = False
            for row in results:
                running = True
                num_returned += 1
                results = {}
                for field in row._xxx_field_to_index:
                    results[field] = str(row[field])
                yield results

    def get_schema(self) -> Schema:
        table = self.bq_client.google_bq_client.get_table(str(self.source_table))
        props = {}

        for schema_field in table.schema:
            props[schema_field.name] = convert_schema_field(schema_field)

        return Schema(properties=props)


if __name__ == "__main__":
    BigQueryTableTap.cli()
