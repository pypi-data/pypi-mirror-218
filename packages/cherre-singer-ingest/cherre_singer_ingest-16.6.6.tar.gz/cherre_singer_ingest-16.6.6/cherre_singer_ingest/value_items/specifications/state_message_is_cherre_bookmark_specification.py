from cherre_types import BaseSpecification
from singer import StateMessage


class StateMessageIsCherreBookmarkSpecification(BaseSpecification):
    def is_satisfied_by(self, candidate: StateMessage) -> bool:
        if not candidate.value:
            return False

        if "bookmarks" not in candidate.value:
            return False

        for key, dic in candidate.value["bookmarks"].items():
            if "timestamp" not in dic:
                return False
            if "bookmark_type" not in dic:
                return False
        return True
