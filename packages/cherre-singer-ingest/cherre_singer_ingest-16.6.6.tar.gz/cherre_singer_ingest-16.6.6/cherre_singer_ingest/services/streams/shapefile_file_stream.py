import os
from typing import List, TextIO
import logging

from cherre_types import FolderPath, FilePath, File

from cherre_singer_ingest.services.common import shp_to_geojson, execute_bash_script
from cherre_singer_ingest.value_items.specifications.folder_is_shapefile_file_specification import (
    FolderIsShapefileFileSpecification,
)
from cherre_singer_ingest.services.streams.csv_file_stream import CSVFileStream
from cherre_singer_ingest.services.unzip_service import UnzipService
from cherre_singer_ingest.value_items import RemoteFile


class ShapefileFileStream(CSVFileStream):
    shapefile_spec = FolderIsShapefileFileSpecification()

    def __init__(
        self,
        remote_file: RemoteFile,
        has_header: bool = True,
        raise_on_error: bool = True,
        pipeline_name: str = "",
    ):
        super().__init__(
            remote_file=remote_file,
            raise_on_error=raise_on_error,
            pipeline_name=pipeline_name,
        )
        self.has_header = has_header

    @staticmethod
    def get_file_extensions(folder: FolderPath) -> List[str]:
        return [File(f).extension for f in os.listdir(str(folder))]

    def get_not_required_file_extensions(self, folder: FolderPath) -> List[str]:
        file_extensions = self.get_file_extensions(folder)
        return list(set(file_extensions) - set(self.shapefile_spec.required_extensions))

    @staticmethod
    def get_shapefile_name(folder: FolderPath) -> File:
        for f in os.listdir(str(folder)):
            file = File(f)
            if file.extension.lower() == "shp":
                return file

    @staticmethod
    def _unzip_file(file: FilePath, unzip_service: UnzipService) -> List[FilePath]:
        return [file for file in unzip_service.unzip_file(file)]

    def get_unzip_folder_path(self, file: FilePath) -> FolderPath:
        unzip_service = UnzipService()
        unzipped_files = [str(f) for f in self._unzip_file(file, unzip_service)]
        logging.info(
            f"The following are the files in the compressed file: {', '.join(unzipped_files)}"
        )

        return unzip_service.working_directory

    def convert_shapefile_to_geojson(self, file_path: FilePath):
        shp_to_geojson_bash_command = shp_to_geojson(file_path)
        execute_bash_script(shp_to_geojson_bash_command)

    def introspect_file_extensions(self, folder: FolderPath) -> None:
        if not self.shapefile_spec.is_satisfied_by(folder):
            raise ValueError(
                "To convert shapefile to GeoJSON, the following extension must be included: .shp, .dbf, and .shx"
            )
        additional_file_exts = self.get_not_required_file_extensions(folder)
        if additional_file_exts:
            logging.info(
                f"The following are additional extensions: {additional_file_exts}"
            )

    def get_and_create_geojson_file_path(self, file: FilePath) -> FilePath:
        unzipped_folder_path = self.get_unzip_folder_path(file)
        self.introspect_file_extensions(unzipped_folder_path)

        shapefile_name = self.get_shapefile_name(unzipped_folder_path)
        self.geojson_file_path = FilePath.parse(
            f"{str(unzipped_folder_path)}/{shapefile_name}.csv"
        )
        self.convert_shapefile_to_geojson(self.geojson_file_path)
        return self.geojson_file_path

    def open_file(self, file: FilePath) -> TextIO:
        return open(
            str(self.get_and_create_geojson_file_path(file)), encoding=self.encoding
        )
