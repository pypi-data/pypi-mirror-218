from typing import Optional, Iterable, Dict, Any

import click
from singer import Schema

from cherre_singer_ingest.services.taps.base_tap import BaseTap, BaseTapStream


class SimpleTestStream(BaseTapStream):
    def __init__(self):
        super().__init__("test")

    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        for i in range(10):
            yield {"value": f"test_{str(i)}"}

    def get_schema(self) -> Schema:
        return Schema(properties={"value": "string"})


class SimpleTestTap(BaseTap):
    """
    Simple test to make one record
    """

    def get_streams(self) -> Iterable[BaseTapStream]:
        yield SimpleTestStream()


def get_simple_test_tap_cmd() -> str:
    return f"python {__file__}"


@click.option("--config")
@click.command()
def main(config: str):
    tap = SimpleTestTap()
    tap.execute()


if __name__ == "__main__":
    main()
