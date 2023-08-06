from enum import Enum


class BookmarkTypes(Enum):
    FILE_READ = "file_read"
    FILE_UNZIPPED = "file_unzipped"
    URI_READ = "uri_read"

    @staticmethod
    def from_string(string: str) -> "BookmarkTypes":
        if not string:
            raise ValueError("No value given")
        val = string.lower()
        if val == "file_read":
            return BookmarkTypes.FILE_READ
        elif val == "file_unzipped":
            return BookmarkTypes.FILE_UNZIPPED
        elif val == "uri_read" or val == "url_read":
            return BookmarkTypes.URI_READ
        else:
            raise ValueError(f"Unknown BookmarkType of {val}")

    def __str__(self) -> str:
        return self.value.lower()
