from abc import ABC, abstractmethod
import json
from typing import Iterable, Dict, List, Any, Optional
from logging import Logger, getLogger
from datetime import datetime

from cherre_types import FilePath
from cherre_singer_ingest.value_items import IngestBookmark, BookmarkTypes
from singer import get_logger


class BaseIngestStateRepository(ABC):
    col_list = "id, title, stream_name, success, pipeline_name, bookmark_type, errors, timestamp, additional_data"

    def __init__(self, logger: Optional[Logger]) -> None:
        self.logger = logger or get_logger() or getLogger()

    @abstractmethod
    def get_all(self) -> Iterable[IngestBookmark]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_type(self, bookmark_type: BookmarkTypes) -> Iterable[IngestBookmark]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_pipeline(self, pipeline_name: str) -> Iterable[IngestBookmark]:
        raise NotImplementedError()

    @abstractmethod
    def get(self, bookmark_id: int) -> Optional[IngestBookmark]:
        raise NotImplementedError()

    @abstractmethod
    def add_bookmark(self, bookmark: IngestBookmark) -> IngestBookmark:
        raise NotImplementedError()

    @abstractmethod
    def save(self) -> bool:
        # signal the repository all writing is done
        raise NotImplementedError()

    @staticmethod
    def write_states_to_file(output_file: FilePath, states: Iterable[IngestBookmark]):
        full_dict: Dict[str, Dict[str, Any]] = {"bookmarks": {}}

        for bk in states:
            full_dict["bookmarks"][bk.title] = bk.to_dict()[bk.title]
        strings = json.dumps(full_dict)

        with open(str(output_file), "w") as file:
            file.writelines(strings)

    def get_latest_states(self, pipeline_name: str = "") -> Iterable[IngestBookmark]:
        if not pipeline_name:
            items = self.get_all()
        else:
            items = self.get_by_pipeline(pipeline_name=pipeline_name)

        per_streams: Dict[str, List[IngestBookmark]] = {}

        zip_bookmarks: Dict[str, Dict[str, List[IngestBookmark]]] = {}

        for item in items:
            if item.bookmark_type == BookmarkTypes.FILE_UNZIPPED:
                if item.stream_name not in zip_bookmarks:
                    zip_bookmarks[item.stream_name] = {}
                zips_for_title = zip_bookmarks[item.stream_name]
                if item.title not in zips_for_title:
                    zips_for_title[item.title] = []
                zips_for_title[item.title].append(item)
            else:
                if item.stream_name not in per_streams:
                    per_streams[item.stream_name] = []
                per_streams[item.stream_name].append(item)

        for stream in per_streams:
            bookmarks_in_stream = per_streams[stream]
            sorted_by_ts = sorted(
                bookmarks_in_stream, key=lambda bk: bk.timestamp, reverse=True
            )

            if len(sorted_by_ts) > 0:
                yield sorted_by_ts[0]

        # for zips, return the latest for the title, since all are the same stream
        for stream_name in zip_bookmarks:
            zip_for_stream = zip_bookmarks[stream_name]
            for title in zip_for_stream:
                zips_per_title = zip_for_stream[title]
                sorted_by_ts = sorted(
                    zips_per_title, key=lambda bk: bk.timestamp, reverse=True
                )
                if len(sorted_by_ts) > 0:
                    yield sorted_by_ts[0]

    @staticmethod
    def _row_to_object(row) -> IngestBookmark:
        additional_data_in_row = row["additional_data"]
        additional_data = (
            json.loads(additional_data_in_row) if additional_data_in_row else {}
        )

        return IngestBookmark(
            title=row["title"],
            stream_name=row["stream_name"],
            success=bool(row["success"]),
            pipeline_name=row["pipeline_name"],
            bookmark_type=BookmarkTypes.from_string(row["bookmark_type"]),
            errors=[e for e in row["errors"].split(",") if e],
            timestamp=datetime.fromisoformat(str(row["timestamp"])),
            additional_data=additional_data,
        )
