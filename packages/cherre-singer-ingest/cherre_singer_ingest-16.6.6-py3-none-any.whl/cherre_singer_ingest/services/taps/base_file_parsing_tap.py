from abc import ABC, abstractmethod
from typing import Iterable, List, Union, Set, Dict

from cherre_types import FilePath, FolderPath
from pathlib import PurePath
from cherre_singer_ingest.factories.remote_file_uri_factory import RemoteFileURIFactory

from cherre_singer_ingest.services.taps.base_tap import BaseTap
from cherre_singer_ingest.services.streams import BaseFileParsingTapStream
from cherre_singer_ingest.factories import BookmarkFactory
from cherre_singer_ingest.value_items import (
    FileIsCompressedFileSpecification,
    RemoteFileIsCompressedFileSpecification,
    FileUnzippedBookmark,
    FileUnzippedFailedBookmark,
    FileReadFailedBookmark,
    FileReadBookmark,
    RemoteFile,
    URI,
    UriBookmark,
)


class BaseFileParsingTap(BaseTap, ABC):
    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        num_workers: int = 1,
        worker_id: int = 0,
        pipeline_name: str = "",
        download_directory: FolderPath = None,
        bookmark_factory: BookmarkFactory = None,
        uri_factory: RemoteFileURIFactory = None,
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            pipeline_name=pipeline_name,
            worker_id=worker_id,
            num_workers=num_workers,
        )
        if not download_directory:
            download_directory = FolderPath.parse("./downloaded")
        self.download_directory = download_directory

        self._is_compressed_file_remote = RemoteFileIsCompressedFileSpecification()
        self._is_compressed_file = FileIsCompressedFileSpecification()

        if not bookmark_factory:
            bookmark_factory = BookmarkFactory()
        self.bookmark_factory = bookmark_factory

        if not uri_factory:
            uri_factory = RemoteFileURIFactory()
        self.uri_factory = uri_factory

        self.local_files_read: Set[URI] = set()
        self.remote_files_read: Set[URI] = set()
        self.local_zip_files_processed: Set[URI] = set()
        self.remote_zip_files_processed: Set[URI] = set()

        self.local_file_bookmarks: Dict[URI, UriBookmark] = {}
        self.local_zip_file_bookmarks: Dict[URI, UriBookmark] = {}
        self.remote_file_bookmarks: Dict[URI, UriBookmark] = {}
        self.remote_zip_file_bookmarks: Dict[URI, UriBookmark] = {}

        self.get_successfully_processed_files_from_state()

    @abstractmethod
    def get_files(self) -> Iterable[RemoteFile]:
        raise NotImplementedError()

    @abstractmethod
    def get_streams(self) -> Iterable[BaseFileParsingTapStream]:
        raise NotImplementedError()

    def get_successfully_processed_files_from_state(self) -> None:
        all_bookmark_objects = []
        if self.state and "bookmarks" in self.state:
            self.logger.info("Processing previous bookmarks to get skip list . . . .")

            all_bookmarks = self.state["bookmarks"]
            for bookmark_name in all_bookmarks:
                bookmark = self.bookmark_factory.from_dict(
                    bookmark=bookmark_name, bk=all_bookmarks[bookmark_name]
                )
                if not self.pipeline_name or (
                    self.pipeline_name == bookmark.pipeline_name
                ):
                    all_bookmark_objects.append(bookmark)

        files_read = {
            bm for bm in all_bookmark_objects if isinstance(bm, FileReadBookmark)
        }
        files_unzipped = {
            bm for bm in all_bookmark_objects if isinstance(bm, FileUnzippedBookmark)
        }

        failed_file_reads = {
            bm for bm in all_bookmark_objects if isinstance(bm, FileReadFailedBookmark)
        }
        failed_unzipped = {
            bm
            for bm in all_bookmark_objects
            if isinstance(bm, FileUnzippedFailedBookmark)
        }

        failed_file_read_uris = {
            bm.remote_file_uri for bm in failed_file_reads if bm.remote_file_uri
        }
        failed_local_files = {
            bm.local_file_uri for bm in failed_file_reads if bm.local_file_uri
        }
        successful_file_bookmarks = {
            bm
            for bm in files_read
            if bm.remote_file_uri not in failed_file_read_uris
            and bm.file not in failed_local_files
        }

        self.local_file_bookmarks = {
            bm.local_file_uri: UriBookmark(
                uri=bm.local_file_uri,
                timestamp=bm.timestamp,
                stream_name=bm.stream_name,
            )
            for bm in successful_file_bookmarks
        }
        self.local_files_read = {ubm.uri for ubm in self.local_file_bookmarks.values()}
        self.logger.debug(
            f"Calculated list of {len(self.local_files_read)} local files to skip"
        )

        self.remote_file_bookmarks = {
            bm.remote_file_uri: UriBookmark(
                uri=bm.remote_file_uri,
                timestamp=bm.timestamp,
                stream_name=bm.stream_name,
            )
            for bm in successful_file_bookmarks
        }
        self.remote_files_read = {
            ubm.uri for ubm in self.remote_file_bookmarks.values()
        }
        self.logger.debug(
            f"Calculated list of {len(self.remote_files_read)} remote files to skip"
        )

        failed_remote_zip_uris = {
            bm.compressed_file_remote_uri
            for bm in failed_unzipped
            if bm.compressed_file_remote_uri
        }
        failed_local_zip_files = {
            bm.compressed_file_local_uri for bm in failed_unzipped if bm.compressed_file
        }
        successful_unzip_bookmarks = {
            bm
            for bm in files_unzipped
            if bm.compressed_file_remote_uri not in failed_remote_zip_uris
            and bm.compressed_file_local_uri not in failed_local_zip_files
        }

        # we now need to filter out any zip bookmarks that didn't process the local files!
        zip_bms_not_missing_remote_files = {
            bm
            for bm in successful_unzip_bookmarks
            if (not bm.unzipped_file_remote_uri)
            or (
                bm.unzipped_file_remote_uri
                and bm.unzipped_file_remote_uri in self.remote_files_read
            )
        }
        zip_bms_not_missing_any = {
            bm
            for bm in zip_bms_not_missing_remote_files
            if bm.unzipped_file_local_uri in self.local_files_read
        }

        self.local_zip_file_bookmarks = {
            bm.compressed_file_local_uri: UriBookmark(
                uri=bm.compressed_file_local_uri,
                timestamp=bm.timestamp,
                stream_name=bm.stream_name,
            )
            for bm in zip_bms_not_missing_any
        }
        self.local_zip_files_processed = {
            bm.uri for bm in self.local_zip_file_bookmarks.values()
        }
        self.logger.debug(
            f"Calculated list of {len(self.local_zip_files_processed)} local archives to skip"
        )

        self.remote_zip_file_bookmarks = {
            bm.compressed_file_remote_uri: UriBookmark(
                uri=bm.compressed_file_remote_uri,
                timestamp=bm.timestamp,
                stream_name=bm.stream_name,
            )
            for bm in zip_bms_not_missing_any
        }
        self.remote_zip_files_processed = {
            bm.uri for bm in self.remote_zip_file_bookmarks.values()
        }
        self.logger.debug(
            f"Calculated list of {len(self.remote_zip_files_processed)} remote archives to skip"
        )

        self.logger.info("State loaded for tap")

    def should_remote_file_be_used(self, remote_file: RemoteFile) -> bool:
        """
        Determine whether the current worker should be responsible for the file with
        the given name.
        """
        if self._is_compressed_file_remote.is_satisfied_by(remote_file):
            uri_collection = self.remote_zip_files_processed
            bookmarks_collection = self.remote_zip_file_bookmarks
        else:
            uri_collection = self.remote_files_read
            bookmarks_collection = self.remote_file_bookmarks

        if remote_file.remote_uri in uri_collection:
            if remote_file.modified_at:
                full_bookmark = bookmarks_collection[remote_file.remote_uri]

                if remote_file.modified_at < full_bookmark.timestamp:
                    return False
                else:
                    self.logger.info(
                        f"File {str(remote_file.remote_uri)} has been modified after last ingest record"
                    )
            else:
                self.logger.info(
                    f"File {str(remote_file.remote_uri)} has already been processed, skipping!"
                )
                return False

        # this determines if we need to do this in parallelized workflows
        filename = str(remote_file.local_file)
        return self.does_string_belong_to_this_worker(filename)

    def should_local_file_be_used(self, local_file: FilePath):
        local_uri = self.uri_factory.get_file_path_uri(local_file)
        if self._is_compressed_file.is_satisfied_by(local_file):
            if local_uri in self.local_zip_files_processed:
                self.logger.info(
                    f"All files in local zip file {str(local_file)} have been processed, skipping"
                )
                return False
        else:
            if local_uri in self.local_files_read:
                self.logger.info(
                    f"Local file {str(local_file)} has been processed, skipping"
                )
                return False

        return True
