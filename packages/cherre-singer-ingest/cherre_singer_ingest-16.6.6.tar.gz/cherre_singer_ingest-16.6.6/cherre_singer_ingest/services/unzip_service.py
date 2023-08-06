import logging
import subprocess
from typing import Iterable

from cherre_types import FilePath, FolderPath
from cherre_types.services import FileSystem

from cherre_singer_ingest.value_items import (
    FileIsCompressedFileSpecification,
)


class UnzipService:
    def __init__(
        self,
        working_directory: FolderPath = None,
        overwrite_switch: str = "u",
        zip_password="",
        file_system: FileSystem = None,
    ):
        self.working_directory = working_directory

        self.overwrite_switch = overwrite_switch
        self.zip_password = zip_password

        if not file_system:
            file_system = FileSystem()
        self.file_system = file_system

        self.compressed_spec = FileIsCompressedFileSpecification()

    def _unzip_file_interior(self, file: FilePath) -> Iterable[FilePath]:
        if self.compressed_spec.is_satisfied_by(file):
            all_files_found = []
            files = self._unzip_archive(file)
            for unzipped_file in files:
                if self.compressed_spec.is_satisfied_by(unzipped_file):
                    for sub_file in self._unzip_file_interior(unzipped_file):
                        all_files_found.append(sub_file)
                else:
                    all_files_found.append(unzipped_file)
            yield from all_files_found
        else:
            yield file

    def unzip_file(self, file: FilePath) -> Iterable[FilePath]:
        if self.compressed_spec.is_satisfied_by(file):
            yield from self._unzip_file_interior(file)
        else:
            yield file

    def _unzip_archive(self, file: FilePath) -> Iterable[FilePath]:
        working_dir = (
            self.working_directory
            if self.working_directory
            else file.path.add_sub_folder(file.name)
        )
        if self.file_system.folder_exists(working_dir):
            for file in self.file_system.get_files_in_directory(working_dir):
                if not self.compressed_spec.is_satisfied_by(file):
                    self.file_system.delete_file(file)
        else:
            self.file_system.create_folder(working_dir)

        if self.compressed_spec.is_satisfied_by(file):
            logging.info(f"Unzip {str(file)} to the folder: {str(working_dir)}/")

            # Creating the 7z command line to extract the compressed file.
            cmd = ["7z", "x", str(file), "-y", f"-o{str(working_dir)}"]

            if self.overwrite_switch:
                cmd.extend([f"-ao{self.overwrite_switch}"])

            if self.zip_password:
                cmd.extend([f"-p{self.zip_password}"])

            logging.info(f"Executing the command, {cmd}")
            subprocess.check_output(cmd, shell=False)

            yield from self.file_system.get_files_in_directory(working_dir)
