from abc import ABC
from typing import Iterable, List, Union, Dict, Optional
import time
import stat
import random
import re
import logging
from datetime import datetime, timezone

from cherre_types import FilePath, FTPInfo, FolderPath, File
from cherre_types.services import FileSystem
from pathlib import PurePath
import paramiko
from cherre_google_clients import GoogleClientFactory, GoogleSecretManagerClient

from cherre_singer_ingest.services.taps.base_file_parsing_tap import BaseFileParsingTap
from cherre_singer_ingest.services.unzip_service_with_bookmarks import (
    UnzipServiceWithBookmarks,
)
from cherre_singer_ingest.value_items import RemoteFile
from cherre_singer_ingest.factories import RemoteFileURIFactory

# we have to set this for the library, or we will fail on large files
# discussion at https://stackoverflow.com/questions/12486623/paramiko-fails-to-download-large-files-1gb
paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = pow(2, 22)  # 4MB per chunk


def file_download_progress_heartbeat(num_in: int, file_size: int) -> None:
    ratio = num_in / float(file_size)
    logging.debug(f"File download at {ratio * 100} percent")


class BaseFTPFileTap(BaseFileParsingTap, ABC):
    def __init__(
        self,
        ftp_info: FTPInfo,
        project_id: str,
        secret_manager: GoogleSecretManagerClient = None,
        download_directory: FolderPath = None,
        recursive: bool = True,
        file_system: FileSystem = None,
        overwrite_local_files: bool = False,
        unzip_service: UnzipServiceWithBookmarks = None,
        ignore_failed_unzips: bool = False,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        num_workers: int = 1,
        worker_id: int = 0,
        pipeline_name: str = "",
    ):

        self.ftp_info = ftp_info
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            num_workers=num_workers,
            worker_id=worker_id,
            pipeline_name=pipeline_name,
            download_directory=download_directory,
        )

        if not secret_manager:
            secret_manager = GoogleClientFactory().get_secret_manager_client(
                project_id=project_id
            )
        self.secret_manager = secret_manager

        self.remote_start_directory = (
            FolderPath.parse(self.ftp_info.external_folder_path)
            if self.ftp_info.external_folder_path
            else FolderPath(".")
        )

        self.recursive = recursive

        if not file_system:
            file_system = FileSystem()
        self.file_system = file_system
        self.overwrite_local_files = overwrite_local_files

        self.ignore_failed_unzips = ignore_failed_unzips

        if not unzip_service:
            unzip_service = UnzipServiceWithBookmarks(
                pipeline_name=self.pipeline_name,
                ignore_failed_unzips=self.ignore_failed_unzips,
            )
        self.unzip_service = unzip_service

        self.max_retries = 10

        self._transport: paramiko.Transport = None
        self._sftp_client: paramiko.SFTPClient = None
        self.reset_connection()

        self._found_subfolders: List[FolderPath] = []

        self.reg_ex = (
            re.compile(self.ftp_info.regex_file_pattern)
            if self.ftp_info.regex_file_pattern
            else None
        )
        self.remote_file_uri_factory = RemoteFileURIFactory()

    def get_remote_files_locally(self) -> Iterable[RemoteFile]:
        fails = 0
        self._found_subfolders = []

        remote_files = self.get_remote_files_on_server()

        # we need to get the remote file path here, because we'll filter based on what the final name is
        remote_files_and_uris = [
            RemoteFile(
                local_file=f,
                remote_uri=self.remote_file_uri_factory.get_ftp_uri(
                    host=self.ftp_info.host, remote_folder=f.path, file=f.file
                ),
                modified_at=f.modified_at,
            )
            for f in remote_files
        ]
        filtered_remote_files = [
            rf for rf in remote_files_and_uris if self.should_remote_file_be_used(rf)
        ]

        done = len(filtered_remote_files) == 0
        while not done:
            try:
                for remote_file_and_uri in filtered_remote_files:
                    if not remote_file_and_uri.local_file:
                        logging.error(
                            f"Remote file {str(remote_file_and_uri.local_file)} does not have a local file!"
                        )
                        continue
                    self.logger.info(
                        f"Processing remote file {str(remote_file_and_uri.local_file)}"
                    )
                    downloaded_file = self.download_file_from_server(
                        remote_file=remote_file_and_uri.local_file
                    )

                    yield RemoteFile(
                        local_file=downloaded_file,
                        remote_uri=remote_file_and_uri.remote_uri,
                        modified_at=remote_file_and_uri.modified_at,
                    )
                done = True
            except Exception as e:
                fails += 1
                self.logger.error(f"Error in get_files: {str(e)}")
                if fails >= self.max_retries:
                    self.logger.error("Max retries reached, failing")
                    raise
                else:
                    self.logger.info(f"Failed on try {fails}, trying again")
                    self.wait_for_fails(fails)
                    self.reset_connection()

    def get_files(self) -> Iterable[RemoteFile]:
        found_any = False
        for pair in self.get_remote_files_locally():
            try:
                # we unzip and return the files from here
                unzipped_files = self.unzip_service.unzip_file(remote_file=pair)

                for unzipped_rf in unzipped_files:
                    # we check one last time if we don't need to process the files that were unzipped
                    if self.should_local_file_be_used(unzipped_rf.local_file):
                        found_any = True
                        yield RemoteFile(
                            local_file=unzipped_rf.local_file,
                            remote_uri=unzipped_rf.remote_uri,
                            modified_at=pair.modified_at,
                        )
            except Exception as e:
                self.logger.error(e)
                if not self.ignore_failed_unzips:
                    raise
        if not found_any:
            self.logger.info("Tap found no unprocessed files!")
            return []

    def rename_unzipped_file(self, f: FilePath, remote_file) -> FilePath:
        """
        Given a local file, rename it so it contains the folder info of remote
        """
        file_prefix = str(remote_file).replace("/", "_").replace(".", "_")
        dest_file_name = f"{file_prefix}_{f.file.name_with_extension}"
        if dest_file_name.startswith("_"):
            dest_file_name = dest_file_name[1:]

        max_length = 256 - len(str(self.download_directory))
        if len(dest_file_name) > max_length:
            dest_file_name = dest_file_name[-max_length:]

        dest_file = File.parse(dest_file_name)

        dest_file_path = FilePath(path=self.download_directory, file=dest_file)
        if self.file_system.file_exists(dest_file_path):
            self.file_system.delete_file(dest_file_path)
        self.logger.info(f"Renaming {str(f)} to {dest_file}")

        copied = self.file_system.copy_file(
            source=f, destination=self.download_directory
        )
        renamed = self.file_system.rename_file(copied, dest_file)

        if not self.file_system.file_exists(renamed):
            raise RuntimeError(f"File was copied to {str(renamed)} but does not exist")
        self.file_system.delete_file(f)
        return renamed

    def reset_connection(self):
        try:
            if self._sftp_client:
                self._sftp_client.close()
            if self._transport:
                self._transport.close()
        except Exception as e:
            self.logger.error(f"Error while closing FTP: {e}")

        self._transport = None
        self._sftp_client = None

    def make_connection(self, force: bool = False) -> None:
        if force or (not self._transport or not self._sftp_client):
            try:
                if self._transport:
                    self._transport.close()
                if self._sftp_client:
                    self._sftp_client.close()
            except Exception as e:
                self.logger.error(e)
            transport_args = (self.ftp_info.host, self.ftp_info.port)
            self._transport = paramiko.Transport(transport_args)
            self._transport.default_window_size = paramiko.common.MAX_WINDOW_SIZE
            self._transport.packetizer.REKEY_BYTES = pow(
                2, 40
            )  # 1TB max, this is a security degradation!
            self._transport.packetizer.REKEY_PACKETS = pow(
                2, 40
            )  # 1TB max, this is a security degradation!
            self._transport.banner_timeout = 100
            self._transport.connect(
                username=self.ftp_info.user,
                password=self.password,
            )
            self._transport.banner_timeout = 2000
            self._sftp_client = paramiko.SFTPClient.from_transport(self._transport)

    def get_folder_paths_to_bypass(self) -> Iterable[FolderPath]:
        """Method to help us avoid introspecting files in a remote folder.

        This is important for folders we cannot introspect due to permission issues.

        Returns:
            Iterable[FolderPath]: [description]
        """
        return []

    def get_remote_files_on_server(self) -> Iterable[FilePath]:
        good_folder = FolderPath(
            folders=self.ftp_info.external_folder_path,
            force_linux_style=True,
            is_root=self.ftp_info.external_folder_path.startswith("/"),
        )
        return self.get_remote_files_under_folder(directory=good_folder)

    def get_remote_files_under_folder(
        self, directory: FolderPath
    ) -> Iterable[FilePath]:
        fails = 0
        done = False

        directory_str = str(directory)
        if directory_str in self.get_folder_paths_to_bypass():
            done = True

        while not done:
            try:
                self.make_connection()
                self.logger.info(f"Retrieving file list from {directory_str}")
                top_folder_items = list(self._sftp_client.listdir_iter(directory_str))

                for item in top_folder_items:
                    if self._is_remote_file_a_directory(item):
                        if self.recursive:
                            sub_directory = item.filename
                            full_dir = directory.add_sub_folder(sub_directory)

                            if full_dir not in self._found_subfolders:
                                sub = self.get_remote_files_under_folder(
                                    directory=full_dir
                                )
                                for file in sub:
                                    yield file
                            self._found_subfolders.append(full_dir)
                    else:
                        file_names_strings = [item.filename]
                        if self.reg_ex:
                            file_names_strings = [
                                f for f in file_names_strings if self.reg_ex.match(f)
                            ]
                        file_names = [File.parse(f) for f in file_names_strings if f]

                        for f in file_names:
                            modified_date = self._get_modified_date_for_remote_file(
                                item
                            )
                            yield FilePath(
                                file=f, path=directory, modified_at=modified_date
                            )
                done = True
            except Exception as e:
                fails += 1
                self.logger.error(
                    f"Error while retrieving files from {str(directory)}, {str(e)}"
                )
                if fails > self.max_retries:
                    raise
                else:
                    self.logger.info(
                        f"Got error {str(e)} retrieving files, retrying {fails}, {str(e)}"
                    )
                    self.wait_for_fails(fails)

    @staticmethod
    def _get_modified_date_for_remote_file(
        file_info: paramiko.SFTPAttributes,
    ) -> Optional[datetime]:
        if not file_info.st_mtime:
            return None
        try:
            modified_date = datetime.fromtimestamp(file_info.st_mtime)
            modified_date = modified_date.replace(tzinfo=timezone.utc)
            return modified_date
        except TypeError:
            logging.error(f"Invalid timestamp of {file_info.st_mtime}")
            return None

    @staticmethod
    def _is_remote_file_a_directory(file_info: paramiko.SFTPAttributes) -> bool:
        return stat.S_ISDIR(file_info.st_mode)

    def download_file_from_server(self, remote_file: FilePath) -> FilePath:
        if (
            remote_file.path
            and remote_file.path.folder_names
            and remote_file.path.folder_names == [""]
        ):
            directory = self.download_directory
        else:
            directory = self.download_directory.add_sub_folder(str(remote_file.path))
        if not self.file_system.folder_exists(directory):
            self.file_system.create_folder(directory)

        local_file = FilePath(file=remote_file.file, path=directory)

        if self.overwrite_local_files or not self.file_system.file_exists(local_file):
            done = False
            num_fails = 0

            while not done and (num_fails < self.max_retries):
                try:
                    self.make_connection()
                    external_file_name = str(remote_file)
                    self.logger.info(
                        f"Downloading {external_file_name} to {str(local_file)}"
                    )
                    self._sftp_client.get(
                        external_file_name,
                        str(local_file),
                        callback=file_download_progress_heartbeat,
                    )

                    if not self.file_system.file_exists(local_file):
                        raise Exception(f"File {str(local_file)} not found")
                    done = True
                except Exception as e:
                    msg = str(e).lower()
                    num_fails += 1
                    if num_fails >= self.max_retries:
                        self.logger.error(
                            f"Failed to get file {str(remote_file)} after {num_fails},  raising errors"
                        )
                        raise
                    else:
                        self.logger.info(
                            f"Connection failed with {msg}, retrying {num_fails}"
                        )
                        self.wait_for_fails(num_fails)
        else:
            self.logger.info(
                f"File {str(local_file)} was found locally, skipping download"
            )
        return local_file

    def wait_for_fails(self, num_fails: int):
        # wait a semi-random amount of time to try again
        # this is semi-random so multiple workers vary their retry times
        wait_factor = random.randint(1000, 3000) / float(1000)
        time.sleep(wait_factor * num_fails)
        self.reset_connection()
        self.make_connection()

    def _get_password(self) -> str:
        return self.secret_manager.get_secret_value(self.ftp_info.password_secret)

    @property
    def password(self) -> str:
        return self._get_password()
