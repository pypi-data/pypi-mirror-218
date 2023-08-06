from typing import Union, Dict, AsyncGenerator, Generator

from singer import RecordMessage

# defines our Record type here so we don't have it everywhere
# any value which can go to a string
ValidRecordValueType = Union[str, int, float, complex, bool]
Record = Dict[str, ValidRecordValueType]
TapOutput = AsyncGenerator[Record, None]
RecordStream = Generator[RecordMessage, None, None]
SingerRecord = Dict[str, Union[str, Record]]

FixedWidthFileDefinition = Dict[str, int]
