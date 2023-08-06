import json
import logging
from typing import Generator, Dict, Any, Iterable, IO

from cherre_singer_ingest.services.streams.base_file_parsing_tap_stream import (
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.value_items import Record, RemoteFile
from cherre_singer_ingest.services.flatten_object import flatten_object


class JSONFileStream(BaseFileParsingTapStream):
    """
    File stream to parsed JSON files and yield a flatten JSON object by key/value properties.
    """

    def __init__(
        self,
        remote_file: RemoteFile,
        pipeline_name: str = "",
        raise_on_error: bool = True,
        encoding: str = "",
    ):
        super().__init__(
            remote_file=remote_file,
            pipeline_name=pipeline_name,
            raise_on_error=raise_on_error,
            encoding=encoding,
        )

    @staticmethod
    def _get_flatten_json(file_content: IO) -> Dict[str, Any]:
        data = json.load(file_content)
        return flatten_object(data)

    def get_fields(self) -> Iterable[str]:
        logging.info(f"Parsing JSON Record from {str(self.remote_file.local_file)}")
        with self.open_file(self.remote_file.local_file) as f:
            data_flatten = self._get_flatten_json(f)

        return [self.clean_key(key) for key in data_flatten.keys()]

    def parse_file(self) -> Generator[Record, None, None]:
        with self.open_file(self.remote_file.local_file) as f:
            data_flatten = self._get_flatten_json(f)
            for key, value in data_flatten.items():
                yield {self.clean_key(key): value}
        return
