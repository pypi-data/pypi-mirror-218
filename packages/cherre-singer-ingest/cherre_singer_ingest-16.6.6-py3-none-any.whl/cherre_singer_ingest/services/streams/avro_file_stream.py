import fastavro
import logging
from typing import Generator, Iterable
from cherre_types import FilePath
from typing import BinaryIO

from cherre_singer_ingest.services.streams.base_file_parsing_tap_stream import (
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.value_items import Record, RemoteFile


class AVROFileStream(BaseFileParsingTapStream):
    """
    File stream to parsed AVRO files and yield a flatten JSON object by key/value properties.
    """

    def __init__(
        self,
        remote_file: RemoteFile,
        pipeline_name: str = "",
        raise_on_error: bool = True,
    ):
        super().__init__(
            remote_file=remote_file,
            pipeline_name=pipeline_name,
            raise_on_error=raise_on_error,
        )

    def open_file(self, file: FilePath) -> BinaryIO:
        return open(str(file), "rb")

    def get_fields(self) -> Iterable[str]:
        logging.info(f"Parsing AVRO Record from {str(self.remote_file.local_file)}")
        with self.open_file(self.remote_file.local_file) as f:
            avro_reader = fastavro.reader(f)
            record = next(avro_reader)

        return [self.clean_key(key) for key in record.keys()]

    def parse_file(self) -> Generator[Record, None, None]:
        with self.open_file(self.remote_file.local_file) as f:
            avro_reader = fastavro.reader(f)
            for record in avro_reader:
                yield {self.clean_key(key): val for key, val in record.items()}
        return
