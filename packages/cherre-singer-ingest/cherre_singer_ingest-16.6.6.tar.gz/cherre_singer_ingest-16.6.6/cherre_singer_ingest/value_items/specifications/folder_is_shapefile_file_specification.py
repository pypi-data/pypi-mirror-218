import os

from cherre_types import BaseSpecification, FolderPath, File


class FolderIsShapefileFileSpecification(BaseSpecification):
    required_extensions = ("shp", "dbf", "shx")

    def is_satisfied_by(self, candidate: FolderPath) -> bool:
        file_extensions = [
            File.parse(f).extension.lower() for f in os.listdir(str(candidate))
        ]
        if set(self.required_extensions).issubset(set(file_extensions)):
            return True
        return False
