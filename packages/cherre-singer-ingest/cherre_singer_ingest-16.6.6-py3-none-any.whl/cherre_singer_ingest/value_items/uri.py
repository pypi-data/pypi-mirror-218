from urllib.parse import ParseResult, urlparse

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class URI:
    value: str

    # can include zip files, example ftp://cherreinc/folder/subfolder/a.zip/b.csv
    def __post_init__(self):
        if "://" not in self.value:
            raise ValueError("Must include protocol in value!")

    @staticmethod
    def parse(value: str) -> "URI":
        return URI(value=value)

    def to_parse_result(self) -> ParseResult:
        """Make use of parsing already present in urllib to tokenize a RemoteFileURI"""
        return urlparse(self.value)

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def protocol(self) -> str:
        parts = self.value.split("://")
        return parts[0]
