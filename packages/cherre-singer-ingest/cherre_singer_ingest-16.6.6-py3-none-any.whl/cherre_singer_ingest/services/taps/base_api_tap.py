from abc import ABC
from typing import List, Union, Dict, Optional
from pathlib import PurePath
from datetime import datetime

from cherre_singer_ingest.services.taps.base_tap import BaseTap
from cherre_singer_ingest.value_items import URI, BookmarkTypes
from cherre_singer_ingest.factories import BookmarkFactory


class BaseAPITap(BaseTap, ABC):
    def __init__(
        self,
        config: List[Union[Dict[str, str], PurePath]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        pipeline_name: str = "",
        num_workers: int = 1,
        worker_id: int = 0,
        bookmark_factory: BookmarkFactory = None
    ):
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            pipeline_name=pipeline_name,
            num_workers=num_workers,
            worker_id=worker_id
        )

        if not bookmark_factory:
            bookmark_factory = BookmarkFactory()
        self.bookmark_factory = bookmark_factory

        self.uris_read: Dict[URI, datetime] = {}
        self.streams_read: Dict[str, datetime]
        self._load_urls_from_bookmarks()

    def get_last_modified_date_for_uri(self, uri: URI) -> Optional[datetime]:
        if uri not in self.uris_read:
            return None
        return self.uris_read[uri]

    def get_last_modified_date_for_stream(self, stream_name: str) -> Optional[datetime]:
        if stream_name not in self.streams_read:
            return None
        return self.streams_read[stream_name]

    def _load_urls_from_bookmarks(self):
        if self.state and "bookmarks" in self.state:
            self.logger.info("Processing previous bookmarks to get skip list . . . .")

            all_bookmarks = self.state["bookmarks"]
            all_bookmark_objects = []
            for bookmark_name in all_bookmarks:
                bookmark = self.bookmark_factory.from_dict(
                    bookmark=bookmark_name, bk=all_bookmarks[bookmark_name]
                )
                if not self.pipeline_name or (
                    self.pipeline_name == bookmark.pipeline_name
                ):
                    all_bookmark_objects.append(bookmark)

            urls_read = [bm for bm in all_bookmark_objects if bm.success and bm.bookmark_type == BookmarkTypes.URI_READ]

            self.uris_read = {URI.parse(bm.title): bm.timestamp for bm in urls_read}
            self.streams_read = {bm.stream_name: bm.timestamp for bm in urls_read}

