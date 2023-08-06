from datetime import datetime

from cherre_types import FilePath

from cherre_singer_ingest.value_items.ingest_bookmarks.bookmark_type import BookmarkTypes
from cherre_singer_ingest.value_items.ingest_bookmarks.ingest_bookmark import IngestBookmark
from cherre_singer_ingest.value_items.uri import URI


class FileReadBookmark(IngestBookmark):
    def __init__(
        self,
        file: FilePath,
        local_file_uri: URI,
        remote_file_uri: URI,
        stream_name: str,
        number_records_read: int = None,
        pipeline_name: str = "",
        timestamp: datetime = None,
    ):
        super().__init__(
            title=str(file),
            bookmark_type=BookmarkTypes.FILE_READ,
            stream_name=stream_name,
            pipeline_name=pipeline_name,
            errors=[],
            success=True,
            additional_data={
                "number_records_read": str(number_records_read) if number_records_read else "",
                "remote_file_uri": str(remote_file_uri) if remote_file_uri else "",
                "local_file_uri": str(local_file_uri) if local_file_uri else ""
            },
            timestamp=timestamp,
        )
        self.number_records_read = number_records_read
        self.file = file
        self.remote_file_uri = remote_file_uri

        self.local_file_uri = local_file_uri
