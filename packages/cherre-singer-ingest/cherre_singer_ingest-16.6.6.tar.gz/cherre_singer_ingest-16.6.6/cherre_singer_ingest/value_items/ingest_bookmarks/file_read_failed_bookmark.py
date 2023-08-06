from datetime import datetime

from cherre_types import FilePath

from cherre_singer_ingest.value_items.ingest_bookmarks.ingest_bookmark import IngestBookmark
from cherre_singer_ingest.value_items.ingest_bookmarks.bookmark_type import BookmarkTypes
from cherre_singer_ingest.value_items.uri import URI


class FileReadFailedBookmark(IngestBookmark):
    def __init__(
        self,
        file: FilePath,
        local_file_uri: URI,
        stream_name: str,
        exception: Exception,
        pipeline_name: str = "",
        timestamp: datetime = None,
        remote_file_uri: URI = None,
    ):
        super().__init__(
            title=str(file),
            bookmark_type=BookmarkTypes.FILE_READ,
            stream_name=stream_name,
            pipeline_name=pipeline_name,
            errors=[str(exception)],
            success=False,
            timestamp=timestamp,
            additional_data={
                "remote_file_uri": str(remote_file_uri) if remote_file_uri else "",
                "local_file_uri": str(local_file_uri) if local_file_uri else ""
            },
        )
        self.file = file
        self.remote_file_uri = remote_file_uri
        self.local_file_uri = local_file_uri
