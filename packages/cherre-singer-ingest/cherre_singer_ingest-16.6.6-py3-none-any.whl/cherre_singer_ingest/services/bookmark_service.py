from datetime import datetime, timezone
from typing import Union

from singer import write_state

from cherre_singer_ingest.value_items import (
    IngestBookmark,
    BookmarkTypes,
    FileIsCompressedFileSpecification,
    FileReadBookmark,
    FileUnzippedFailedBookmark,
    FileUnzippedBookmark,
    FileReadFailedBookmark,
    RemoteFile,
    URI,
)
from cherre_singer_ingest.factories import RemoteFileURIFactory


class BookmarkService:
    def __init__(
        self, pipeline_name: str = "", uri_factory: RemoteFileURIFactory = None
    ):
        self.pipeline_name = pipeline_name

        if not uri_factory:
            uri_factory = RemoteFileURIFactory()
        self.uri_factory = uri_factory

    def write_file_unzipped_bookmark(
        self,
        unzipped_file: RemoteFile,
        compressed_file: RemoteFile,
    ):
        if not FileIsCompressedFileSpecification().is_satisfied_by(
            compressed_file.local_file
        ):
            raise ValueError(f"File {str(compressed_file)} is not a compressed file!")

        bookmark = FileUnzippedBookmark(
            unzipped_file=unzipped_file.local_file,
            unzipped_file_local_uri=self.uri_factory.get_file_path_uri(
                unzipped_file.local_file
            ),
            compressed_file=compressed_file.local_file,
            compressed_file_local_uri=self.uri_factory.get_file_path_uri(
                compressed_file.local_file
            ),
            unzipped_file_remote_uri=unzipped_file.remote_uri,
            compressed_file_remote_uri=compressed_file.remote_uri,
            pipeline_name=self.pipeline_name,
            stream_name=unzipped_file.local_file.name,
        )

        self.write_bookmark_to_stream(bookmark=bookmark)
        return bookmark

    def write_file_unzipped_error(
        self,
        compressed_file: RemoteFile,
        exception: Exception,
        stream_name: str = "unzip_errors",
    ) -> IngestBookmark:
        if not FileIsCompressedFileSpecification().is_satisfied_by(
            compressed_file.local_file
        ):
            raise ValueError(f"File {str(compressed_file)} is not a compressed file!")

        bookmark = FileUnzippedFailedBookmark(
            compressed_file=compressed_file.local_file,
            compressed_file_local_uri=self.uri_factory.get_file_path_uri(
                compressed_file.local_file
            ),
            exception=exception,
            pipeline_name=self.pipeline_name,
            compressed_file_remote_uri=compressed_file.remote_uri,
            stream_name=stream_name,
        )

        self.write_bookmark_to_stream(bookmark=bookmark)
        return bookmark

    def write_file_read_bookmark(
        self, remote_file: RemoteFile, stream_name: str, num_records: int
    ) -> IngestBookmark:
        bookmark = FileReadBookmark(
            file=remote_file.local_file,
            local_file_uri=self.uri_factory.get_file_path_uri(remote_file.local_file),
            stream_name=stream_name,
            pipeline_name=self.pipeline_name,
            number_records_read=num_records,
            remote_file_uri=remote_file.remote_uri,
        )

        self.write_bookmark_to_stream(bookmark=bookmark)
        return bookmark

    def write_file_read_error(
        self, remote_file: RemoteFile, stream_name: str, exception: Exception
    ) -> IngestBookmark:
        bookmark = FileReadFailedBookmark(
            file=remote_file.local_file,
            local_file_uri=self.uri_factory.get_file_path_uri(remote_file.local_file),
            stream_name=stream_name,
            exception=exception,
            pipeline_name=self.pipeline_name,
            remote_file_uri=remote_file.remote_uri,
        )
        self.write_bookmark_to_stream(bookmark=bookmark)
        return bookmark

    def write_url_read_bookmark(
        self,
        url_base: Union[str, URI],
        success: bool,
        stream_name: str,
        timestamp: datetime = datetime.now(tz=timezone.utc),
        exception: Exception = None,
    ) -> IngestBookmark:
        bookmark = IngestBookmark(
            title=str(url_base),
            bookmark_type=BookmarkTypes.URI_READ,
            success=success,
            errors=[str(exception)] if exception else [],
            timestamp=timestamp,
            stream_name=stream_name,
            pipeline_name=self.pipeline_name,
        )
        self.write_bookmark_to_stream(bookmark)
        return bookmark

    @staticmethod
    def write_bookmark_to_stream(bookmark: IngestBookmark) -> IngestBookmark:
        state_message = {"bookmarks": bookmark.to_dict()}
        write_state(state_message)
        return bookmark
