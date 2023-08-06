from logging import Logger, getLogger
from typing import Dict, Iterable, List, Optional, Tuple, Any, Sequence

from cherre_types import FolderPath, FilePath, File
from cherre_domain import DbDataTypes
from singer import SchemaMessage, RecordMessage, get_logger

from cherre_singer_ingest.services.stream_writers.stream_target import (
    AvroFileStreamTarget,
)
from cherre_singer_ingest.services.stream_writers.per_stream_writer_results import (
    PerStreamWriterResults,
)
from cherre_singer_ingest.services.clean_column_name import (
    clean_column_name,
)
from cherre_singer_ingest.value_items import RecordStream


class AvroStreamWriter:
    """
    Target which writes records given to avro file(s) (one per stream received)
    """

    def __init__(
        self,
        output_directory: FolderPath = None,
        lowercase_schema: bool = False,
        logger: Logger = None,
    ):
        if not output_directory:
            output_directory = FolderPath(".")
        self.output_directory = output_directory
        self.stream_targets: Dict[str, AvroFileStreamTarget] = {}
        self.lowercase_schema = lowercase_schema

        if not logger:
            logger = get_logger()
            if not logger:
                logger = getLogger()
        self.logger = logger

        self.lowercase_schema = lowercase_schema

        self.field_defs: List[Dict[str, Sequence[Any]]] = []

    @staticmethod
    def get_output_extension() -> str:
        return "avro"

    def _create_stream_data_writer(
        self,
        stream_name: str,
        schema_messages: Dict[str, SchemaMessage],
    ) -> AvroFileStreamTarget:
        if stream_name not in schema_messages:
            raise RuntimeError(f"Stream name {stream_name} has not provided a schema!")
        schema = schema_messages[stream_name]

        self.field_defs = self.get_field_defs(
            schema, lowercase_schema=self.lowercase_schema
        )

        schema_def = {
            "namespace": "cherre",
            "type": "record",
            "name": "source",
            "fields": self.field_defs,
        }
        output_file, sub_folder = self._make_file_path_for_stream(
            stream_name=stream_name
        )

        return AvroFileStreamTarget(
            stream_name=stream_name,
            column_names=[str(field_def["name"]) for field_def in self.field_defs],
            sub_folder=sub_folder,
            output_file=output_file,
            schema=schema_def,
        )

    @staticmethod
    def get_field_defs(
        schema: SchemaMessage, lowercase_schema: bool = False
    ) -> List[Dict[str, Sequence[Any]]]:
        if not schema:
            raise ValueError("Schema message has not been set!")

        schema = schema.asdict()["schema"]

        if isinstance(schema, dict):
            json_fields = schema["properties"]
        else:
            json_fields = schema.__dict__["properties"]

        field_defs = []
        for prop_name in json_fields:
            clean_name = clean_column_name(prop_name, lowercase_schema=lowercase_schema)
            prop_type = json_fields[prop_name]["type"]
            prop_format = (
                json_fields[prop_name]["format"]
                if "format" in json_fields[prop_name]
                else None
            )
            cherre_type = DbDataTypes.from_json_schema(
                json_type=prop_type, type_format=prop_format
            )

            # allow our domain to substitute in preferred types here
            standard_cherre_type = cherre_type.standard_type
            field_defs.append(
                {
                    "name": clean_name,
                    "type": ["null", standard_cherre_type.avro_type],
                }
            )
        return field_defs

    def write_records_to_file(
        self,
        records: RecordStream,
        schema_messages: Dict[str, SchemaMessage],
        table_name_override: str = None,
    ) -> Tuple[Iterable[PerStreamWriterResults], int]:
        local_files_created = []

        num_processed = 0
        old_stream_target = None
        # write each different stream to an avro file
        for record in records:
            stream_target = self._get_stream_target(
                record, schema_messages, table_name_override
            )

            # Initialize `old_stream_target` and flush() whenever the stream changes
            if num_processed == 0:
                old_stream_target = stream_target
            else:
                if (
                    num_processed > 0
                    and old_stream_target
                    and old_stream_target.stream_name != stream_target.stream_name
                ):
                    old_stream_target.flush()

            try:
                avro_record = self._clean_record(record)
                stream_target.write_record(avro_record)
                num_processed += 1
            except TypeError as e:
                self.logger.error(f"No new data can be iterated - {e}")
                raise

            old_stream_target = stream_target

        # finish writing out all files
        self.logger.info(f"{num_processed} records were processed")
        self.logger.info("All streams are done, writing targets to files")
        for stream in self.stream_targets:
            stream_target = self.stream_targets[stream]
            stream_target.close()

            res = PerStreamWriterResults(
                file=stream_target.output_file,
                column_names=stream_target.column_names,
                sub_folder=stream_target.sub_folder,
            )
            local_files_created.append(res)

        return local_files_created, num_processed

    def _get_file_name_from_stream_name(
        self, stream_name
    ) -> Tuple[File, Optional[FolderPath]]:
        extension = self.get_output_extension()
        if "/" in stream_name:
            parts = stream_name.split("/")
            last_part = parts[-1]
            others = "/".join(parts[:-1])
            return File.parse(f"{last_part}.{extension}"), FolderPath.parse(others)
        return File.parse(f"{stream_name}.{extension}"), None

    @staticmethod
    def _get_schema(schema_message: SchemaMessage) -> Dict[str, Any]:
        if not schema_message:
            raise ValueError("Schema message has not been set!")
        return schema_message.asdict()["schema"]

    def _clean_record(self, message: RecordMessage):
        res = {}
        for key in message.record:
            col_name = clean_column_name(key, lowercase_schema=self.lowercase_schema)
            val = message.record[key]
            res[col_name] = val
        return res

    def _make_file_path_for_stream(
        self, stream_name: str
    ) -> Tuple[FilePath, FolderPath]:
        # TODO add run_times to every file?
        file, folder_path = self._get_file_name_from_stream_name(
            stream_name=stream_name
        )
        return FilePath.from_file_in_folder(self.output_directory, file), folder_path

    def _get_stream_target(
        self,
        record: RecordMessage,
        schema_messages: Dict[str, SchemaMessage],
        table_name_override: str = None,
    ) -> AvroFileStreamTarget:
        if record.stream not in self.stream_targets:
            self.logger.info(
                f"Found new stream of {record.stream}, creating new writer . . ."
            )
            stream_name = table_name_override if table_name_override else record.stream
            self.stream_targets[record.stream] = self._create_stream_data_writer(
                stream_name=stream_name,
                schema_messages=schema_messages,
            )
        return self.stream_targets[record.stream]
