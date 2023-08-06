from typing import Iterable
from logging import Logger, getLogger

from singer import get_logger
from cherre_types import FolderPath, FileSystem

from cherre_singer_ingest.services.unzip_service import UnzipService
from cherre_singer_ingest.services.bookmark_service import BookmarkService
from cherre_singer_ingest.factories import RemoteFileURIFactory
from cherre_singer_ingest.value_items import (
    FileIsCompressedFileSpecification,
    RemoteFile,
)


class UnzipServiceWithBookmarks:
    def __init__(
        self,
        working_directory: FolderPath = None,
        overwrite_switch: str = "u",
        zip_password="",
        file_system: FileSystem = None,
        bookmark_service: BookmarkService = None,
        logger: Logger = None,
        remote_file_uri_factory: RemoteFileURIFactory = None,
        unzip_service: UnzipService = None,
        pipeline_name: str = "",
        ignore_failed_unzips: bool = False,
    ):
        if not bookmark_service:
            bookmark_service = BookmarkService(pipeline_name=pipeline_name)
        self.bookmark_service = bookmark_service

        if not logger:
            logger = get_logger()
            if not logger:
                logger = getLogger()
        self.logger = logger

        if not remote_file_uri_factory:
            remote_file_uri_factory = RemoteFileURIFactory()
        self.remote_file_uri_factory = remote_file_uri_factory

        if not unzip_service:
            unzip_service = UnzipService(
                working_directory=working_directory,
                overwrite_switch=overwrite_switch,
                zip_password=zip_password,
                file_system=file_system,
            )
        self.unzip_service = unzip_service
        self.ignore_failed_unzips = ignore_failed_unzips

        self.compressed_spec = FileIsCompressedFileSpecification()

    def unzip_file(self, remote_file: RemoteFile) -> Iterable[RemoteFile]:
        if not self.compressed_spec.is_satisfied_by(remote_file.local_file):
            yield remote_file
        else:
            try:
                for file in self.unzip_service.unzip_file(remote_file.local_file):
                    unzipped_remote_uri = (
                        self.remote_file_uri_factory.get_unzipped_file_path(
                            archive_remote_path=remote_file.remote_uri, file=file
                        )
                    )
                    unzipped_remote_file = RemoteFile(
                        local_file=file, remote_uri=unzipped_remote_uri
                    )

                    # only if we ignore failed zip files, we will store it in ingest_state, so we can use it when we re-ingest
                    if self.ignore_failed_unzips:
                        self.bookmark_service.write_file_unzipped_bookmark(
                            unzipped_file=unzipped_remote_file,
                            compressed_file=remote_file,
                        )

                    yield RemoteFile(local_file=file, remote_uri=unzipped_remote_uri)

            except Exception as e:
                self.logger.error(e)

                # only if we ignore failed zip files, we will store it in ingest_state, so we can use it when we re-ingest
                if self.ignore_failed_unzips:
                    self.bookmark_service.write_file_unzipped_error(
                        compressed_file=remote_file,
                        exception=e,
                    )
                raise
