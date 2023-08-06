from datetime import datetime

from cherre_types import FilePath

from cherre_singer_ingest.value_items.ingest_bookmarks.ingest_bookmark import IngestBookmark
from cherre_singer_ingest.value_items.ingest_bookmarks.bookmark_type import BookmarkTypes
from cherre_singer_ingest.value_items.uri import URI


class FileUnzippedFailedBookmark(IngestBookmark):
    def __init__(
        self,
        compressed_file: FilePath,
        compressed_file_local_uri: URI,
        stream_name: str,
        exception: Exception,
        compressed_file_remote_uri: URI = None,
        pipeline_name: str = "",
        timestamp: datetime = None,
    ):
        additional_data = {
            "compressed_file": str(compressed_file),
            "compressed_file_remote_uri": str(compressed_file_remote_uri) if compressed_file_remote_uri else "",
            "compressed_file_local_uri": str(compressed_file_local_uri)
        }
        title = f"unzip:{str(compressed_file)}"
        super().__init__(
            title=title,
            bookmark_type=BookmarkTypes.FILE_UNZIPPED,
            stream_name=stream_name,
            pipeline_name=pipeline_name,
            additional_data=additional_data,
            success=False,
            errors=[str(exception)],
            timestamp=timestamp,
        )

        self.compressed_file = compressed_file
        self.compressed_file_local_uri = compressed_file_local_uri
        self.compressed_file_remote_uri = compressed_file_remote_uri
