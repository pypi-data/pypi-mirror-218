from abc import ABC, abstractmethod
from typing import Iterable, List, Union, Dict
from pathlib import PurePath
from urllib.error import HTTPError
import logging

from cherre_singer_ingest.services.taps.base_file_parsing_tap import BaseFileParsingTap
from cherre_singer_ingest.services.common import download_from_http
from cherre_singer_ingest.services.streams import BaseFileParsingTapStream
from cherre_singer_ingest.value_items import URI, RemoteFile
from cherre_singer_ingest.factories import RemoteFileURIFactory
from cherre_types.services import FileSystem
from cherre_types import FilePath


class WebPageTap(BaseFileParsingTap, ABC):
    """
    Tap for reading files over HTTP/S
    """

    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        num_workers: int = 1,
        worker_id: int = 0,
        file_system: FileSystem = None,
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            num_workers=num_workers,
            worker_id=worker_id,
        )

        self.remote_file_uri_factory = RemoteFileURIFactory()

        if not file_system:
            file_system = FileSystem()
        self.file_system = file_system

    @abstractmethod
    def get_file_names(self) -> Iterable[URI]:
        """
        HTTP protocol does not provide a way to list contents in the same way an FTP server would. Each tap
        implementation will need to specify a list of file names to get.
        """
        raise NotImplementedError

    @staticmethod
    def _download_file(remote_uri, local_file):
        try:
            download_from_http(str(remote_uri), str(local_file))
        except HTTPError as e:
            logging.error(f"Error when downloading from {str(remote_uri)}: {str(e)}")
            raise

    def get_files(self) -> Iterable[RemoteFile]:

        remote_files = []

        for remote_uri in self.get_file_names():
            parse_result = remote_uri.to_parse_result()  # tokenize URI
            local_file = self.download_directory + parse_result.path
            remote_file = RemoteFile(FilePath.parse(str(local_file)), remote_uri)

            if not self.should_remote_file_be_used(remote_file):
                continue

            # if the directory doesn't exist, create it
            directory = self.download_directory.add_sub_folder(
                parse_result.path.rsplit("/", 1)[0]
            )
            if not self.file_system.folder_exists(directory):
                self.file_system.create_folder(directory)

            try:
                self._download_file(remote_uri, local_file)
            except HTTPError as e:
                if e.code == 404:
                    # Sometimes the file will be missing remotely. Ideally this would be addressed in get_file_names
                    # but HTTP does not offer a way to get a directory listing and sometimes expected files are missing
                    continue
                raise

            remote_files.append(remote_file)

        return remote_files

    @abstractmethod
    def get_streams(self) -> Iterable[BaseFileParsingTapStream]:
        raise NotImplementedError
