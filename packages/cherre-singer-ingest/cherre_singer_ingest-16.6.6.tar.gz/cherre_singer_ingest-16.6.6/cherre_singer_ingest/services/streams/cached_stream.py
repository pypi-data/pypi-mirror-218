from typing import Optional, Iterable, Dict, Any, List

from cherre_singer_ingest.services.streams.base_tap_stream import BaseTapStream
from singer import Schema


class CachedStream(BaseTapStream):
    """
    Stream which allows us to cache results of another stream - used when we want to pull the records and return a stream

    """

    def __init__(self, source: BaseTapStream, max_records: int = 100000):
        super().__init__(name=source.name)
        self.source = source
        self.cached_records: List[Dict[str, Any]] = []
        self.found_schema = None
        self.max_records = max_records
        self._over_limit = False

    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        if not self.cached_records:
            temp = []
            for rec in self.source.get_records():
                if not self._over_limit:
                    temp.append(rec)

                    if len(temp) > self.max_records:
                        for c in temp:
                            yield c
                            self._over_limit = True
                            self.cached_records = []
                else:
                    yield rec
            if not self._over_limit:
                self.cached_records = temp
        for rec in self.cached_records:
            yield rec

    def get_schema(self) -> Schema:
        if not self.found_schema:
            self.found_schema = self.source.get_schema()
        return self.found_schema
