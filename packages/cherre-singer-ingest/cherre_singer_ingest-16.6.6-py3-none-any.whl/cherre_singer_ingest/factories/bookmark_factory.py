from typing import Dict, Any, Iterable
from datetime import datetime

from singer import StateMessage
from cherre_types import FilePath

from cherre_singer_ingest.factories.remote_file_uri_factory import RemoteFileURIFactory
from cherre_singer_ingest.value_items import (
    IngestBookmark,
    BookmarkTypes,
    URI,
    FileReadBookmark,
    FileUnzippedFailedBookmark,
    FileReadFailedBookmark,
    FileUnzippedBookmark,
    StateMessageIsCherreBookmarkSpecification
)


class BookmarkFactory:
    def __init__(self):
        self.uri_factory = RemoteFileURIFactory()

    def from_dict(self, bookmark: str, bk: Dict[str, Any]) -> IngestBookmark:
        timestamp = datetime.fromisoformat(bk["timestamp"])

        bookmark_type = BookmarkTypes.from_string(bk["bookmark_type"])
        success = bool(bk["success"]) and (not str(bk["success"]).lower() == "false")

        if bookmark_type == BookmarkTypes.FILE_READ:
            remote_file_uri = (
                URI.parse(bk["additional_data"]["remote_file_uri"])
            )

            file = FilePath.parse(bookmark)
            local_file_uri = (
                URI.parse(bk["additional_data"]["local_file_uri"])
                if "local_file_uri" in bk["additional_data"] else self.uri_factory.get_file_path_uri(file=file)
            )
            if success:
                return FileReadBookmark(
                    file=file,
                    local_file_uri=local_file_uri,
                    stream_name=bk["stream_name"],
                    pipeline_name=bk["pipeline_name"],
                    number_records_read=bk["additional_data"]["number_records_read"]
                    if "number_records_read" in bk["additional_data"]
                    else None,
                    remote_file_uri=remote_file_uri,
                    timestamp=timestamp,
                )
            else:
                return FileReadFailedBookmark(
                    file=file,
                    local_file_uri=local_file_uri,
                    stream_name=bk["stream_name"],
                    pipeline_name=bk["pipeline_name"],
                    exception=Exception(bk["errors"][0]),
                    timestamp=timestamp,
                    remote_file_uri=remote_file_uri,
                )
        elif bookmark_type == BookmarkTypes.FILE_UNZIPPED:
            remote_file_location = URI.parse(bk["additional_data"]["compressed_file_remote_uri"])

            compressed_file = FilePath.parse(bk["additional_data"]["compressed_file"])
            local_compressed_uri = (
                URI.parse(bk["additional_data"]["compressed_file_local_uri"])
                if "compressed_file_local_uri" in bk["additional_data"]
                else self.uri_factory.get_file_path_uri(compressed_file)
            )
            if success:
                unzipped_file = FilePath.parse(bk["additional_data"]["unzipped_file"])
                unzipped_remote_path = URI.parse(bk["additional_data"]["unzipped_file_remote_uri"])
                unzipped_local_uri = URI.parse(bk["additional_data"]["unzipped_file_local_uri"])
                return FileUnzippedBookmark(
                    compressed_file=compressed_file,
                    compressed_file_local_uri=local_compressed_uri,
                    pipeline_name=bk["pipeline_name"],
                    compressed_file_remote_uri=remote_file_location,
                    unzipped_file=unzipped_file,
                    unzipped_file_remote_uri=unzipped_remote_path,
                    unzipped_file_local_uri=unzipped_local_uri,
                    timestamp=timestamp,
                    stream_name=bk["stream_name"],
                )
            else:
                return FileUnzippedFailedBookmark(
                    compressed_file=FilePath.parse(bookmark),
                    pipeline_name=bk["pipeline_name"],
                    exception=Exception(bk["errors"][0]),
                    compressed_file_remote_uri=remote_file_location,
                    compressed_file_local_uri=URI.parse(f"file://{bookmark}"),
                    timestamp=timestamp,
                    stream_name=bk["stream_name"],
                )
        else:
            return IngestBookmark(
                title=bookmark,
                bookmark_type=BookmarkTypes.from_string(bk["bookmark_type"]),
                stream_name=bk["stream_name"],
                success=bk["success"],
                errors=bk["errors"],
                timestamp=timestamp,
                pipeline_name=bk["pipeline_name"],
                additional_data=bk["additional_data"],
            )

    def from_state_message(self, message: StateMessage) -> Iterable[IngestBookmark]:
        # not all state is a bookmark, check!
        spec = StateMessageIsCherreBookmarkSpecification()
        if not spec.is_satisfied_by(message):
            return []

        for bookmark, bk in message.value["bookmarks"].items():
            hydrated = self.from_dict(bookmark=bookmark, bk=bk)
            yield hydrated
