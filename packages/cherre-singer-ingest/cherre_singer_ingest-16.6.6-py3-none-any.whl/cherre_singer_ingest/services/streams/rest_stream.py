from typing import Iterable, Optional, Dict, Any
import time
import logging

from singer import Schema
from singer_sdk import RESTStream as MeltanoRestStream
from singer_sdk.authenticators import APIAuthenticatorBase

from cherre_singer_ingest.services.streams.base_tap_stream import Prop, BaseTapStream
from cherre_singer_ingest.services.flatten_object import flatten_object


class RESTStream(BaseTapStream, MeltanoRestStream):
    def __init__(
        self,
        url: str,
        name: str,
        pipeline_name: str = "",
        authenticator: APIAuthenticatorBase = None,
        request_delay: Optional[float] = None,
        raise_on_error: bool = True,
    ):
        super().__init__(
            name=name, pipeline_name=pipeline_name, raise_on_error=raise_on_error
        )

        self.request_delay = request_delay

        self._authenticator = authenticator

        self._url_base = url
        self.path = ""

        self._found_schema_object: Optional[Schema] = None

    @property
    def url_base(self) -> str:
        return self._url_base

    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        if self.request_delay:
            time.sleep(self.request_delay)

        try:
            for row in self.request_records(partition):
                row = self.post_process(row, partition)
                flat = flatten_object(row)
                yield flat
            self.bookmark_service.write_url_read_bookmark(
                self.url_base, success=True, stream_name=self.name
            )
        except Exception as e:
            self.bookmark_service.write_url_read_bookmark(
                url_base=self.url_base,
                success=False,
                exception=e,
                stream_name=self.name,
            )
            logging.error(e)
            raise

    def get_schema(self) -> Schema:
        first = None
        if not self._found_schema_object:
            for rec in self.get_records():
                first = rec
                break

            # translate to a schema
            props = {}
            if first:
                for key in first:
                    if isinstance(first[key], int):
                        props[key] = Prop("integer")
                    else:
                        props[key] = Prop()
            self._found_schema_object = Schema(properties=props)

        return self._found_schema_object

    def post_process(
        self, row: Dict[str, Any], partition: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        row = super().post_process(row)

        res = {}
        for key in row:
            if key[0].isdigit():
                res[f"_{key}"] = row[key]
            else:
                res[key] = row[key]
        return res

    @property
    def authenticator(self) -> Optional[APIAuthenticatorBase]:
        if self._authenticator:
            return self._authenticator
        return super().authenticator

    @authenticator.setter
    def authenticator(self, val: Optional[APIAuthenticatorBase]) -> None:
        self._authenticator = val
