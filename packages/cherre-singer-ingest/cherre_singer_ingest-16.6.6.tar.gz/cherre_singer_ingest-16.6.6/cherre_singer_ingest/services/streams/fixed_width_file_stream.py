from typing import Dict, Generator
import logging

from cherre_singer_ingest.services.streams.base_file_parsing_tap_stream import (
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.value_items import Record, RemoteFile


class FixedWidthFileStream(BaseFileParsingTapStream):
    def __init__(
        self,
        remote_file: RemoteFile,
        file_definition: Dict[str, int],
        encoding: str = "",
        raise_on_error: bool = True,
    ):
        super().__init__(
            encoding=encoding, remote_file=remote_file, raise_on_error=raise_on_error
        )

        if not file_definition:
            raise ValueError("File Definition must be set for FixedWidth parsing!")
        self.file_definition = file_definition

    def parse_file(self) -> Generator[Record, None, None]:
        logging.info(
            f"Reading fixed width records from {str(self.remote_file.local_file)}"
        )
        with self.open_file(self.remote_file.local_file) as fixed_width_file:
            for line in fixed_width_file:
                line_pos = 0
                res: Record = {}
                for col, width in self.file_definition.items():
                    val = line[line_pos : line_pos + width]
                    res[col] = val.strip()
                    line_pos += width
                yield res
