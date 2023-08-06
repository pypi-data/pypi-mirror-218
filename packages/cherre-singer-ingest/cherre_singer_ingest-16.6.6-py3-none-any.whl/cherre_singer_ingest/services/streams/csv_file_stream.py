import csv
import logging
import os
import sys
from typing import Iterable, Generator, Iterator, List
import collections
from itertools import islice

from cherre_singer_ingest.services.streams.base_file_parsing_tap_stream import (
    BaseFileParsingTapStream,
)
from cherre_singer_ingest.services.streams.base_tap_stream import Prop
from cherre_singer_ingest.value_items import Record, TapError, RemoteFile
from singer.schema import Schema

# Set csv field size to the max size Python can handle.
# note this current method does not work on Windows!
if not os.name == "nt":
    csv.field_size_limit(sys.maxsize)


class CSVFileStream(BaseFileParsingTapStream):
    def __init__(
        self,
        remote_file: RemoteFile,
        delimiter: str = ",",
        quote_char: str = '"',
        escape_with_quotes: bool = True,
        encoding: str = "",
        pipeline_name: str = "",
        raise_on_error: bool = True,
        stream_name_override: str = "",
        drop_null_bytes: bool = False,
        header_override: List[str] = None,
        skip_lines: int = 0,
    ):
        super().__init__(
            encoding=encoding,
            remote_file=remote_file,
            pipeline_name=pipeline_name,
            raise_on_error=raise_on_error,
            stream_name_override=stream_name_override,
        )
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.escape_with_quotes = escape_with_quotes
        self.drop_null_bytes = drop_null_bytes
        self.header_override = header_override
        self.skip_lines = skip_lines

    @property
    def _csv_quoting_level(self) -> int:
        return csv.QUOTE_MINIMAL if self.escape_with_quotes else csv.QUOTE_NONE

    @staticmethod
    def _consume(iterator: Iterator, n: int = None):
        """Advance the iterator n-steps ahead. If n is None, consume entirely. This is taken from:
        https://docs.python.org/3.7/library/itertools.html#itertools-recipes"""
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            collections.deque(iterator, maxlen=0)
        else:
            # advance to the empty slice starting at position n
            next(islice(iterator, n, n), None)

    def get_fields(self) -> Iterable[str]:
        logging.info(f"Parsing CSV records from {str(self.remote_file.local_file)}")
        if self.header_override:
            return self.header_override
        else:
            with self.open_file(self.remote_file.local_file) as f:
                reader = csv.reader(
                    f,
                    delimiter=self.delimiter,
                    quotechar=self.quote_char,
                    quoting=self._csv_quoting_level,
                )
                if self.skip_lines:
                    self._consume(
                        reader, self.skip_lines
                    )  # skip ahead self.skip_lines lines

                header = next(reader)

            return [self.clean_key(h) for h in header]

    def get_schema(self) -> Schema:
        """
        We override this method in order to allow for the header override to inform the Schema creation instead of
        allowing a call to parse_file to create the Schema option.
        """
        if self.header_override:
            props = {k: Prop() for k in self.header_override}
            schema = Schema(
                properties=props,
                additionalProperties=[],
            )
            return schema
        return super().get_schema()

    def parse_file(self) -> Generator[Record, None, None]:
        with self.open_file(self.remote_file.local_file) as f:
            file_lines = (x.replace("\0", "") for x in f) if self.drop_null_bytes else f
            reader = csv.reader(
                file_lines,
                delimiter=self.delimiter,
                quotechar=self.quote_char,
                quoting=self._csv_quoting_level,
            )

            if self.skip_lines:
                self._consume(
                    reader, self.skip_lines
                )  # skip ahead self.skip_lines lines

            header = self.header_override or next(reader)
            for line in reader:
                if len(line) != len(header):
                    msg = f"Invalid data shape in file {str(self.remote_file.local_file)}, "
                    msg += f"\n\nHeader has {len(header)} values, but row has {len(line)} values.  Row: {line}"
                    raise TapError(message=msg)

                # NOTE: we enforce lowercase column naming convention here
                yield {self.clean_key(key): val for key, val in zip(header, line)}
        return
