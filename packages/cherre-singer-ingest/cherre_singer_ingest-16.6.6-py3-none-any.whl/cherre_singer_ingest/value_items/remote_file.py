from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

from cherre_types import FilePath

from cherre_singer_ingest.value_items.uri import URI


@dataclass(frozen=True, eq=True)
class RemoteFile:
    local_file: FilePath
    remote_uri: URI
    modified_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        res = {"local_file": str(self.local_file), "remote_uri": str(self.remote_uri)}
        if self.modified_at:
            res["modified_at"] = self.modified_at.isoformat()
        return res

    @staticmethod
    def from_dict(dict_: Dict[str, Any]) -> "RemoteFile":
        return RemoteFile(
            local_file=FilePath.parse(dict_["local_file"]),
            remote_uri=URI.parse(dict_["remote_uri"]),
            modified_at=datetime.fromisoformat(dict_["modified_at"]) if "modified_at" in dict_ else None
        )

    def __hash__(self) -> int:
        return hash(str(self.local_file) + "::" + str(self.remote_uri))
