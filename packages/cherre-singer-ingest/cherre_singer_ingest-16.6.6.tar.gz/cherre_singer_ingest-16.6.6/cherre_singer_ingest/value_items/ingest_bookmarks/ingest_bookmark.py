from typing import List, Dict
from datetime import datetime, timezone
import json

from cherre_singer_ingest.value_items.ingest_bookmarks.bookmark_type import BookmarkTypes


class IngestBookmark:
    def __init__(
        self,
        title: str,
        bookmark_type: BookmarkTypes,
        stream_name: str,
        success: bool,
        errors: List[str] = None,
        timestamp: datetime = None,
        pipeline_name="",
        additional_data: Dict[str, str] = None,
    ):
        if errors and len(errors) > 0 and success:
            raise ValueError("You cannot have errors on a successful bookmark!")

        self.title = title
        self.bookmark_type = bookmark_type
        self.stream_name = stream_name
        self.errors = errors if errors else []
        self.success = success
        self.timestamp = timestamp if timestamp else datetime.now(tz=timezone.utc)
        self.pipeline_name = pipeline_name
        self.additional_data = additional_data if additional_data else {}

    def to_dict(self):
        return {
            self.title: {
                "bookmark_type": str(self.bookmark_type),
                "success": self.success,
                "errors": self.errors,
                "timestamp": self.timestamp.isoformat(),
                "pipeline_name": self.pipeline_name,
                "stream_name": self.stream_name,
                "additional_data": self.additional_data,
            }
        }

    def to_json(self) -> str:
        dict_ = self.to_dict()
        return json.dumps(dict_)

    def __hash__(self):
        return hash(
            (self.title, str(self.bookmark_type), self.stream_name, self.pipeline_name, self.success, self.timestamp)
        )

    def __eq__(self, other):
        return hash(self) == hash(other)


