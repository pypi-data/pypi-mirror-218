import logging
from decimal import Decimal, localcontext
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from fastavro import writer, parse_schema
from cherre_types.services.file_system import FileSystem
from cherre_types import FilePath, FolderPath


PRECISION = 9


class AvroFileStreamTarget:
    """
    Represents a single table that we're writing to an avro file for upload to the data lake
    """

    def __init__(
        self,
        stream_name: str,
        output_file: FilePath,
        schema: Dict[str, Any],
        column_names: Optional[List[str]] = None,
        sub_folder: Optional[FolderPath] = None,
        chunk_size: int = 10000,
    ):
        self.stream_name = stream_name
        self.output_file = output_file
        self.sub_folder = sub_folder
        self.column_names = column_names

        self.schema = schema
        self.chunk_size = chunk_size
        self.current_chunk: List[Dict[str, str]] = []
        self.file_started = False

        # get the fields which need numeric processing from the schema
        self.float_fields = [
            f["name"] for f in self.schema["fields"] if f["type"] == "float"
        ]

        self.epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

        logical_type_fields = [
            f
            for f in self.schema["fields"]
            if "type" in f
            and len(f["type"]) > 1
            and "type" in f["type"][1]
            and "logicalType" in f["type"][1]
        ]
        self.decimal_fields = [
            f["name"]
            for f in logical_type_fields
            if f["type"][1]["type"] == "bytes"
            and f["type"][1]["logicalType"] == "decimal"
        ]
        self.integer_fields = [
            f["name"] for f in self.schema["fields"] if f["type"][1] == "int"
        ]
        self.bool_fields = [
            f["name"] for f in self.schema["fields"] if f["type"][1] == "boolean"
        ]
        self.date_fields = [
            f["name"]
            for f in logical_type_fields
            if f["type"][1]["type"] == "int" and f["type"][1]["logicalType"] == "date"
        ]
        self.timestamp_fields = [
            f["name"]
            for f in logical_type_fields
            if f["type"][1]["logicalType"] == "timestamp-millis"
        ]

    def _is_null(self, value: Any) -> bool:
        if value == 0:
            return False
        if not value:
            return True
        if str(value).lower() == "null":
            return True
        return False

    def _clean_value(self, value: Any, field_name: str):
        if self._is_null(value):
            return None

        try:
            if field_name in self.float_fields:
                logging.debug(f"Converting {value} to float for {field_name}")
                return float(value)
            elif field_name in self.decimal_fields:
                logging.debug(f"Converting {value} to decimal for {field_name}")
                str_val = str(value)
                with localcontext() as deccontext:
                    deccontext.prec = 38
                    dec = round(Decimal(str_val), PRECISION)
                    return dec
            elif field_name in self.date_fields:
                logging.debug(f"Converting {value} to date for {field_name}")
                this_date = datetime.fromisoformat(value)
                if not this_date.tzinfo:
                    this_date = this_date.replace(tzinfo=timezone.utc)
                delta = this_date - self.epoch
                return delta.days
            elif field_name in self.timestamp_fields:
                logging.debug(f"Converting {value} to timestamp for {field_name}")
                this_date = datetime.fromisoformat(value)
                if not this_date.tzinfo:
                    this_date = this_date.replace(tzinfo=timezone.utc)
                delta = this_date - self.epoch
                return int(delta.total_seconds() * 1000)
            elif field_name in self.integer_fields:
                logging.debug(f"Converting {value} to integer for {field_name}")
                return int(value)
            elif field_name in self.bool_fields:
                logging.debug(f"Converting {value} to boolean for {field_name}")
                return bool(value)
            else:
                logging.debug(f"Converting {value} to string for {field_name}")
                return str(value)
        except Exception as e:
            logging.error(
                f"Error while converting {value} for field {field_name}: {str(e)}"
            )
            raise

    def _start_file(self) -> None:
        fs = FileSystem()
        if fs.file_exists(self.output_file):
            raise RuntimeError(
                f"File {str(self.output_file)} exists, cannot write to it!"
            )

    def _write_chunk_to_file(self):
        with open(str(self.output_file), "a+b") as open_file:
            parsed_schema = parse_schema(self.schema)
            writer(
                open_file,
                parsed_schema,
                self.current_chunk,
                codec="snappy",
                codec_compression_level=6,
            )
            logging.debug(f"Writing records to {str(self.output_file)}")
        self.current_chunk = []

    def write_record(self, record: Dict[str, Any]) -> None:
        if not self.file_started:
            self._start_file()
            self.file_started = True

        new_rec: Dict[str, Any] = {}

        new_rec = {key: self._clean_value(value, key) for key, value in record.items()}

        self.current_chunk.append(new_rec)
        if len(self.current_chunk) > self.chunk_size:
            self._write_chunk_to_file()

    def flush(self) -> None:
        if len(self.current_chunk) > 0:
            self._write_chunk_to_file()

    def close(self) -> None:
        self.flush()
