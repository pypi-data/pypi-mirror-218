from dataclasses import dataclass


@dataclass(frozen=True, eq=True, repr=True)
class SchemaProperty:
    name: str
    type: str = "string"
