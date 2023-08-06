from abc import ABC, abstractmethod
from typing import Optional, Iterable, Dict, Any, List
from dataclasses import dataclass

import pendulum
from singer.schema import Schema
from singer import RecordMessage, write_message
from singer_sdk import Stream
from singer_sdk.plugin_base import PluginBase
from singer_sdk.streams.core import conform_record_data_types
from cherre_types import get_env

from cherre_singer_ingest.services.bookmark_service import BookmarkService


class CherreMeltanoPlugin(PluginBase):

    name = "cherre-meltano-plugin"

    def __init__(self):
        super().__init__(config={}, parse_env_config=False)

    @property
    def state(self) -> dict:
        return {}


@dataclass(frozen=True)
class Prop:
    type: str = "string"

    def to_dict(self):
        return {"type": self.type}


class BaseTapStream(Stream, ABC):
    """
    Base class to get us in line with the Meltano classes.  Will eventually be replaced by
    the signer_sdk.streams.stream class
    """

    def __init__(
        self,
        name: str,
        pipeline_name: str = "",
        raise_on_error: bool = True,
        bookmark_service: BookmarkService = None,
    ):
        plugin_base = CherreMeltanoPlugin()
        super().__init__(name=name, tap=plugin_base)
        self.pipeline_name = pipeline_name
        if not self.pipeline_name:
            self.pipeline_name = get_env("PIPELINE_NAME", "")
        self.raise_on_error = raise_on_error

        if not bookmark_service:
            bookmark_service = BookmarkService(pipeline_name=self.pipeline_name)
        self.bookmark_service = bookmark_service

        self._found_schema: Optional[Dict[str, Any]] = None

    @abstractmethod
    def get_records(self, partition: Optional[dict] = None) -> Iterable[Dict[str, Any]]:
        """Abstract row generator function. Must be overridden by the child class.

        Each row emitted should be a dictionary of property names to their values.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_schema(self) -> Schema:
        raise NotImplementedError()

    @property
    def _schema(self) -> Dict[str, Any]:
        """
        Injects our schema generation into the base object to meld them
        """
        if not self._found_schema:
            schema_obj = self.get_schema()

            for prop in schema_obj.properties:
                if not hasattr(schema_obj.properties[prop], "to_dict"):
                    schema_obj.properties[prop] = Prop(
                        schema_obj.properties[prop]["type"]
                    )
            self._found_schema = schema_obj.to_dict()

        if self._found_schema:
            return self._found_schema
        raise RuntimeError("Couldn't find schema")

    @_schema.setter
    def _schema(self, val: Schema) -> None:
        if val:
            raise ValueError("Attempted to set schema with a value!")

    @property
    def key_properties(self) -> Optional[List[str]]:
        return []

    @staticmethod
    def clean_key(key: str) -> str:
        return key.lower().replace("-", "_").replace(",", "_")

    def _write_record_message(self, record: dict) -> None:
        """Override Meltano's version to avoid very expensive catalog checking"""
        """Write out a RECORD message."""
        record = conform_record_data_types(
            stream_name=self.name,
            row=record,
            schema=self.schema,
            logger=self.logger,
        )
        record_message = RecordMessage(
            stream=self.name,
            record=record,
            version=None,
            time_extracted=pendulum.now(),
        )
        write_message(record_message)
