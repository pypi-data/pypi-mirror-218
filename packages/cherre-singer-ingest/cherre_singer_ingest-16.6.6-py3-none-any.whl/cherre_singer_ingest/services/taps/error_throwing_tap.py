from typing import Iterable, Optional, Dict, Any

import click
from cherre_types import FilePath
from singer.schema import Schema

from cherre_singer_ingest import BaseTapStream
from cherre_singer_ingest.value_items import RunSingerPythonTapCommand, RunSingerCommand
from cherre_singer_ingest.services import BaseTap


class ErrorStream(BaseTapStream):
    def __init__(self):
        super().__init__("error")

    def get_schema(self) -> Schema:
        return Schema(properties={"data": "string"})

    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        yield {"first": "fine"}
        raise RuntimeError("Error in tap!")


class ErrorThrowingTap(BaseTap):
    def get_streams(self) -> Iterable[BaseTapStream]:
        yield ErrorStream()

    def __init__(self):
        super().__init__()


def get_error_throwing_tap_cmd() -> RunSingerCommand:
    return RunSingerPythonTapCommand(file=FilePath.parse(__file__).file, config={})


@click.option("--config")
@click.command()
def main(config: str):
    tap = ErrorThrowingTap()
    tap.execute()


if __name__ == "__main__":
    main()
