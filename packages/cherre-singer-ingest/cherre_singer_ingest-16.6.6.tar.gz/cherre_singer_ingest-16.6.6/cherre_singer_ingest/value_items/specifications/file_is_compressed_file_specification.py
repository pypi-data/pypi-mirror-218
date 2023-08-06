from cherre_types import BaseSpecification, FilePath

from cherre_singer_ingest.value_items.remote_file import RemoteFile


class FileIsCompressedFileSpecification(BaseSpecification):
    # There are more compressed files, these are just some of the most common compressed files.
    possible_extensions = ("zip", "gzip", "tar", "7z", "gz", "xz")

    def is_satisfied_by(self, candidate: FilePath) -> bool:
        if not candidate.extension:
            return False

        if candidate.extension.lower() in self.possible_extensions:
            return True
        return False


class RemoteFileIsCompressedFileSpecification(BaseSpecification):
    # There are more compressed files, these are just some of the most common compressed files.
    possible_extensions = ("zip", "gzip", "tar", "7z", "gz", "xz")

    def is_satisfied_by(self, candidate: RemoteFile) -> bool:
        for ext in self.possible_extensions:
            if candidate.remote_uri.value.endswith(f".{ext}"):
                return True
        return False
