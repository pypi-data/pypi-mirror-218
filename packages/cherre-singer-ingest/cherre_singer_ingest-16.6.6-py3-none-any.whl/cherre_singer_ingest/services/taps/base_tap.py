from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional, Any, List, Dict, Iterable, Union
import hashlib

from pathlib import PurePath
from singer import load_json, SchemaMessage
from singer.schema import Schema
from singer_sdk import Tap, Stream
from singer_sdk.helpers._classproperty import classproperty

from cherre_singer_ingest.value_items import (
    TapError,
    MissingTapConfigValueError,
    SchemaProperty,
)
from cherre_singer_ingest.services.streams import BaseTapStream
from cherre_types import get_env


class BaseTap(Tap, ABC):
    """
    Defines a tap in Singer terms
    Delivers JSON data from a source to a writer
    """

    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        pipeline_name: str = "",
        num_workers: int = 1,
        worker_id: int = 0,
    ):
        # meltano cannot handle a config dictionary in a list, so pass just the dict
        if isinstance(config, list) and len(config) == 1:
            if isinstance(config[0], dict):
                config_to_super = config[0]
                super().__init__(
                    config=config_to_super,
                    catalog=catalog,
                    state=state,
                    parse_env_config=parse_env_config,
                )
            elif isinstance(config[0], str):
                config_to_super = config
                super().__init__(
                    config=config_to_super,
                    catalog=catalog,
                    state=state,
                    parse_env_config=parse_env_config,
                )
            else:
                super().__init__(
                    config=config,
                    catalog=catalog,
                    state=state,
                    parse_env_config=parse_env_config,
                )
        else:
            super().__init__(
                config=config,
                catalog=catalog,
                state=state,
                parse_env_config=parse_env_config,
            )

        log_level = get_env("LOG_LEVEL", "INFO")
        self.logger.setLevel(level=log_level)

        self.pipeline_name = pipeline_name

        if worker_id >= num_workers:
            raise ValueError("worker_id must be lower than the number of workers!")

        if num_workers < 1:
            raise ValueError("num_workers must be >= to 1")

        if worker_id < 0:
            raise ValueError("worker_id must be >= to 0")

        self.num_workers = num_workers
        self.worker_id = worker_id

        self._found_streams: Dict[str, BaseTapStream] = {}

    @abstractmethod
    def get_streams(self) -> Iterable[BaseTapStream]:
        raise NotImplementedError()

    @classproperty
    def name(self) -> str:
        return str(type(self))

    @property
    def _streams(self):
        if not self._found_streams:
            self._found_streams = {s.name: s for s in self.get_streams()}
        return self._found_streams

    @_streams.setter
    def _streams(self, val):
        pass

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return list(self.get_streams())

    @classmethod
    def load_config_file(
        cls, config_file_loc: Union[Dict[str, str], PurePath], keys: List[str]
    ) -> Dict[str, Any]:
        if isinstance(config_file_loc, dict):
            return config_file_loc

        try:
            config_values = load_json(config_file_loc)
        except Exception as e:
            raise TapError(str(e))

        tap_name = cls.__name__
        for key in keys:
            if key not in config_values:
                raise MissingTapConfigValueError(key, str(config_file_loc), tap_name)

        return config_values

    @classmethod
    def get_config_value(
        cls, config: List[Union[Dict[str, str], PurePath]], key: str, default_value=None
    ) -> str:
        if not config:
            raise TapError("No config file given!")

        if isinstance(config[0], dict):
            config_values = config[0]
        else:
            config_values = cls.load_config_file(config_file_loc=config[0], keys=[])

        if key not in config_values:
            if default_value is not None:
                return default_value
            else:
                raise MissingTapConfigValueError(key, file=str(config[0]), tap_name="")
        return str(config_values[key])

    @property
    def time_extracted(self) -> Optional[datetime]:
        return None

    @staticmethod
    def make_schema_from_props_list(schema_properties: List[SchemaProperty]) -> Schema:
        props = {sp.name: {"type": sp.type.lower()} for sp in schema_properties}
        schema = Schema(properties=props)
        return schema

    @staticmethod
    def get_elt_schema() -> Schema:
        """
        Convenience method for OLD etl style ingests, which use a single column
        Returns:

        """
        sole_prop = SchemaProperty("data")
        return BaseTap.make_schema_from_props_list([sole_prop])

    @staticmethod
    def _wrap_schema_message(stream: BaseTapStream) -> SchemaMessage:
        """
        Given a stream, make a schema message for this that can be written as JSON by Meltano
        """
        schema = stream.get_schema().__dict__

        # unwrap here, we need to balance the bad meltano and our serialization needs
        for prop in schema["properties"]:
            if hasattr(schema["properties"][prop], "to_dict"):
                schema["properties"][prop] = schema["properties"][prop].to_dict()

        return SchemaMessage(
            stream=stream.name, schema=schema, key_properties=stream.key_properties
        )

    async def produce_singer_records(self) -> None:
        """
        Writes Singer Records to the stdin
        :return:
        """
        start = datetime.now()
        self.logger.debug(f"Starting record production at {start.isoformat()}")

        for stream in self.get_streams():
            try:
                schema_message = self._wrap_schema_message(stream)
                self.write_schema(stream_name=stream.name, schema=schema_message)

                for record in stream.get_records(partition=None):
                    self.write_record(stream_name=stream.name, record=record)
            except Exception as e:
                self.logger.error(f"Error in tap: {str(e)}")
                if stream.raise_on_error:
                    raise

        finished = datetime.now()
        self.logger.debug(f"Finished record production at {finished.isoformat()}")
        self.logger.info(f"Tap finished in {str(finished - start)}")

    def does_string_belong_to_this_worker(self, string: str) -> bool:
        if self.num_workers == 1:
            return True

        # shards items between worker pods based on a string
        int_hash = int(hashlib.sha1(string.encode()).hexdigest(), 16)
        in_worker = int_hash % self.num_workers == self.worker_id
        if in_worker:
            self.logger.info(f"{string} belongs to this worker")
        return in_worker
