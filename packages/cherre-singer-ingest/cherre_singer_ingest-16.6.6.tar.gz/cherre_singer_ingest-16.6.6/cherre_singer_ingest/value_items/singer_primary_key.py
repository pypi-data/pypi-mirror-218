from dataclasses import dataclass
from typing import List

from cherre_singer_ingest.services.clean_column_name import clean_column_name


@dataclass(frozen=True, eq=True, repr=True)
class SingerPrimaryKey:
    """
    There are three different scenarios when dealing with Primary Keys, specifically in Taps & Targets.
    Using Singer's key_properties field, we either:
        - Have one value in key_properties indicating one primary key.
        - Have multiple values in key_properties indicating a composite primary key.
        - Have no values in key_properties indicating we need to generate one.
    """

    key_properties: List[str]
    stream_name: str

    @property
    def primary_key_name(self) -> str:
        if self.is_cherre_generated_primary_key():
            clean_stream_name = clean_column_name(self.stream_name)
            return f"cherre_{clean_stream_name}_pk"
        elif self.is_composite_primary_key():
            return clean_column_name("_".join(self.key_properties))
        return self.key_properties[0]

    @property
    def primary_key_type(self) -> str:
        if not self.key_properties:
            return "CHERRE_GENERATED_PRIMARY_KEY"
        elif len(self.key_properties) > 1:
            return "COMPOSITE_PRIMARY_KEY"
        return "SINGLE_PRIMARY_KEY"

    def is_single_column_primary_key(self) -> bool:
        if self.primary_key_type == "SINGLE_PRIMARY_KEY":
            return True
        return False

    def is_composite_primary_key(self) -> bool:
        if self.primary_key_type == "COMPOSITE_PRIMARY_KEY":
            return True
        return False

    def is_cherre_generated_primary_key(self) -> bool:
        if self.primary_key_type == "CHERRE_GENERATED_PRIMARY_KEY":
            return True
        return False
