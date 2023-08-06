from dataclasses import dataclass
from datetime import datetime

from cherre_singer_ingest.value_items.uri import URI


@dataclass(frozen=True, eq=True)
class UriBookmark:
    uri: URI
    timestamp: datetime
    stream_name: str = ""
