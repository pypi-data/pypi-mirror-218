from abc import abstractmethod, ABC
import sys
import os
from typing import List, Dict, Any
from datetime import datetime, timezone
from logging import Logger, getLogger

from singer import (
    parse_message,
    RecordMessage,
    SchemaMessage,
    load_json,
    StateMessage,
    get_logger,
)
from pandas import isna
from cherre_domain import DbDataTypes

from cherre_singer_ingest.value_items import (
    RecordStream,
    TargetError,
    MissingTargetConfigValueError,
)
from cherre_singer_ingest.repositories import (
    CloudSQLIngestStateRepository,
    BaseIngestStateRepository,
)
from cherre_singer_ingest.factories import BookmarkFactory
from cherre_types import FilePath


class BaseCherreTarget(ABC):
    """
    Defines basic interface to receive results from a tap and move them to somewhere else
    """

    def __init__(
        self,
        ignore_schema: bool = False,
        state_repository: BaseIngestStateRepository = None,
        bookmark_factory: BookmarkFactory = None,
        store_bookmarks: bool = True,
        logger: Logger = None,
        destination_dataset: str = "raw",
        include_stream_name: bool = False,
    ) -> None:
        if not logger:
            logger = get_logger()
            if not logger:
                logger = getLogger()
        self.logger = logger

        self.ignore_schema = ignore_schema
        self.schema_messages: Dict[str, SchemaMessage] = {}

        if not state_repository:
            state_repository = CloudSQLIngestStateRepository()
        self.state_repository = state_repository

        if not bookmark_factory:
            bookmark_factory = BookmarkFactory()
        self.bookmark_factory = bookmark_factory

        self.store_bookmarks = store_bookmarks
        self._destination_dataset = destination_dataset
        self._include_stream_name = include_stream_name

    @abstractmethod
    def write_records(self, records: RecordStream) -> int:
        """
        Given the record generation, deal with the data
        :param records:
        :return: Number of records taken
        """
        raise NotImplementedError()

    @property
    def destination_dataset(self) -> str:
        return self._destination_dataset

    @staticmethod
    def get_delimiter() -> str:
        """
        Defines the delimiter that our DBT process will use to split data rows
        :return:
        """
        return "Ý"

    @staticmethod
    def get_delimiter_replacement() -> str:
        return "#$!CHERRE_DELIMITER_WAS_FOUND!$#"

    @classmethod
    def load_config_file(cls, config_file_loc: str, keys: List[str]) -> Dict[str, Any]:
        config_values = load_json(config_file_loc)

        tap_name = cls.__name__
        for key in keys:
            if key not in config_values:
                raise MissingTargetConfigValueError(key, config_file_loc, tap_name)

        return config_values

    def convert_object_to_data_row(self, record_message: RecordMessage) -> str:
        """
        Translate a single record to the format DBT expects
        :param record_message:
        :return: string for the row
        """
        # if we have a schema, check if what we've been given agrees with that as well
        self.check_record_against_schema(record_message)

        delim = self.get_delimiter()
        val_strings = []
        for val in record_message.record.values():
            if isinstance(val, float) and isna(val):
                val_strings.append("")
            if isinstance(val, bool):
                val = "True" if val else "False"
                val_strings.append(val)
            elif val:
                val_string = str(val)
                if delim in val_string:
                    val_string = val_string.replace(
                        delim, self.get_delimiter_replacement()
                    )
                val_strings.append(val_string)
            else:
                val_strings.append("")

        data = delim.join(val_strings)
        num_delim = data.count(delim)
        expected = len(record_message.record) - 1
        if not num_delim == expected:
            raise RuntimeError(
                f"Error, string produced {num_delim} records but was given {expected} records"
            )

        return data

    def check_record_against_schema(self, record: RecordMessage) -> None:
        record_fields = record.record.keys()
        if not record_fields:
            raise ValueError("No keys were given in the record!")
        if record.stream in self.schema_messages and not self.ignore_schema:
            schema = self.schema_messages[record.stream]
            schema_fields = self.get_expected_fields_from_schema(schema)
            missing_fields = [
                f
                for f in schema_fields
                if f not in record_fields and not f == "cherre_ingest_datetime"
            ]
            if len(missing_fields) > 0:
                raise RuntimeError(
                    f"Record is missing fields {missing_fields}.  Schema is {schema}"
                )
            extra_fields = [
                f
                for f in record_fields
                if f not in schema_fields and not f == "cherre_ingest_datetime"
            ]
            if len(extra_fields) > 0:
                raise RuntimeError(
                    f"Record has fields not in schema {extra_fields}.  Schema is {schema}"
                )

    @staticmethod
    def get_expected_fields_from_schema(schema_message: SchemaMessage) -> List[str]:
        try:
            schema = schema_message.asdict()["schema"]
            return schema["properties"].keys()
        except Exception as e:
            raise ValueError("Schema has no fields!")

    def process(self, source_file: str = None) -> None:
        source = None
        if source_file:
            source = FilePath.parse(source_file)
        record_stream = self.get_records_from_message_stream(source)
        num_written = self.write_records(record_stream)
        if num_written <= 0:
            self.logger.warning("No records were ingested for target!")

    def execute(self, source_file: str = None) -> None:
        """
        Execute the TAP as a Singer stand alone process
        :return:
        """
        self.logger.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))
        try:
            self.process(source_file)
        except Exception as e:
            msg = f"Error in Cherre Target: {str(e)}"
            sys.stderr.write(msg)
            raise TargetError(msg)

    def add_schema(self, message: SchemaMessage):
        if not message.stream:
            raise ValueError("Schema messages must include a stream name!")
        if message.stream in self.schema_messages:
            if not message == self.schema_messages[message.stream]:
                raise ValueError(
                    f"Schema {message.stream} has already been set but new message attempts to redefine it!"
                )
        self.schema_messages[message.stream] = message

    def _open_file(self, source_file: FilePath):
        return open(str(source_file), mode="r")

    def get_records_from_message_stream(
        self, source_file: FilePath = None
    ) -> RecordStream:
        """
        Get records from stdin, remove the Singer formatting and give just the record values
        :return:
        """
        timestamp_string = datetime.now(tz=timezone.utc).isoformat()

        if source_file:
            source = self._open_file(source_file)
        else:
            if os.isatty(sys.stdin.fileno()):  # type: ignore
                raise RuntimeError("No data in stdin is present to read from!")
            source = sys.stdin

        for line in source:
            line = line.rstrip()
            message = parse_message(line)

            try:
                if isinstance(message, RecordMessage):
                    if "cherre_ingest_datetime" not in message.record:
                        message.record["cherre_ingest_datetime"] = timestamp_string

                    # If we need the stream_name to be included in the schema!
                    if self._include_stream_name:
                        if "cherre_stream_name" not in message.record:
                            message.record["cherre_stream_name"] = message.stream

                    yield message
                elif isinstance(message, SchemaMessage):
                    ts_type = DbDataTypes.TIMESTAMP.json_schema_type
                    message.schema["properties"]["cherre_ingest_datetime"] = {
                        "type": ts_type[0],
                        "format": ts_type[1],
                    }

                    if self._include_stream_name:
                        message.schema["properties"]["cherre_stream_name"] = {
                            "type": "string"
                        }

                    self.add_schema(message)
                elif isinstance(message, StateMessage):
                    if self.store_bookmarks:
                        bookmarks = self.bookmark_factory.from_state_message(
                            message=message
                        )
                        for bookmark in bookmarks:
                            self.state_repository.add_bookmark(bookmark=bookmark)
                else:
                    # only throw if it's not a valid singer message type!
                    if not message:
                        raise TargetError(f"Received unknown message of {line}")
            except Exception as e:
                self.logger.error(e)
                raise

        self.state_repository.save()
        try:
            if source_file:
                source.close()
        except Exception as e:
            self.logger.error(f"Error closing source {e}")
        return
