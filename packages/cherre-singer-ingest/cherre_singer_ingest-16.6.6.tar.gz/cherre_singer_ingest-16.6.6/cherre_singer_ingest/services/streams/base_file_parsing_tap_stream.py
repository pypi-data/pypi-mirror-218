from typing import Optional, Iterable, Dict, Any, Generator, IO
from abc import abstractmethod
import logging

from singer.schema import Schema
from cherre_types import FilePath

from cherre_singer_ingest.value_items import TapError, Record, RemoteFile
from cherre_singer_ingest.services.streams.base_tap_stream import BaseTapStream, Prop
from cherre_singer_ingest.services.bookmark_service import BookmarkService


class BaseFileParsingTapStream(BaseTapStream):
    def __init__(
        self,
        remote_file: RemoteFile,
        encoding: str = "",
        pipeline_name: str = "",
        raise_on_error: bool = True,
        bookmark_service: BookmarkService = None,
        stream_name_override: str = "",
    ):
        super().__init__(
            name=stream_name_override
            if stream_name_override
            else remote_file.local_file.name,
            pipeline_name=pipeline_name,
            raise_on_error=raise_on_error,
            bookmark_service=bookmark_service,
        )
        self.remote_file = remote_file
        self._encoding = encoding

    @abstractmethod
    def parse_file(self) -> Generator[Record, None, None]:
        raise NotImplementedError()

    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        try:
            num_records = 0
            for rec in self.parse_file():
                yield rec
                num_records += 1

            self.bookmark_service.write_file_read_bookmark(
                remote_file=self.remote_file,
                stream_name=self.name,
                num_records=num_records,
            )
            self.logger.info(f"Read {num_records} records in stream {self.name}")
        except Exception as e:
            self.bookmark_service.write_file_read_error(
                remote_file=self.remote_file, stream_name=self.name, exception=e
            )

            logging.error(e)
            raise

    @property
    def encoding(self) -> str:
        if self._encoding:
            return self._encoding
        return "utf-8"

    def open_file(self, file: FilePath) -> IO:
        return open(str(file), encoding=self.encoding)

    def get_schema(self) -> Schema:
        for rec in self.parse_file():
            keys = rec.keys()
            props = {k: Prop() for k in keys}
            schema = Schema(
                properties=props,
                additionalProperties=[],
            )
            return schema
        raise TapError("No records found, cannot determine schema!")
