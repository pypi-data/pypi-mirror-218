import logging
from typing import Iterable, Optional
import json
from logging import Logger

from singer import get_logger
from cherre_types import BigQueryTable
from cherre_google_clients import GoogleBigQueryClient, GoogleClientFactory
from cherre_domain import get_project_id

from cherre_singer_ingest.repositories.base_state_repository import (
    BaseIngestStateRepository,
)
from cherre_singer_ingest.value_items import IngestBookmark, BookmarkTypes


class BigQueryIngestStateRepository(BaseIngestStateRepository):
    def __init__(
        self,
        storage_table: Optional[BigQueryTable] = None,
        big_query_client: Optional[GoogleBigQueryClient] = None,
        logger: Optional[Logger] = None,
    ):
        super().__init__(logger=logger)

        if not storage_table:
            project_id = get_project_id()
            storage_table = BigQueryTable.parse(f"{project_id}.ingest_state.current")
        self.storage_table = storage_table

        if not big_query_client:
            factory = GoogleClientFactory()
            big_query_client = factory.get_big_query_client(
                project_id=storage_table.project_id
            )
        self.big_query_client = big_query_client

        self._db_existence_verified = False

        # currently used just to escape projects that can't store in the state repository!
        self.is_ignored = False

    def _init_db_if_needed(self):
        if not self._db_existence_verified:
            if not self.big_query_client.does_dataset_exist(
                project_id=self.storage_table.project_id,
                dataset=self.storage_table.dataset,
            ):
                self.logger.info(
                    f"Dataset {self.storage_table.project_id}.{self.storage_table.dataset} does not exist, ignoring state"
                )
                self.is_ignored = True
                self._db_existence_verified = True
                return

            self._db_existence_verified = self.big_query_client.does_table_exist(
                self.storage_table
            )

        if not self._db_existence_verified:
            logging.info(f"Creating table {str(self.storage_table)}")
            query = f"""CREATE TABLE `{str(self.storage_table)}`(
                id INT64,
                title STRING,
                stream_name STRING,
                success BOOLEAN,
                pipeline_name STRING,
                bookmark_type STRING,
                errors STRING,
                timestamp TIMESTAMP,
                additional_data STRING
            )
            """

            self.big_query_client._run_no_result_query(query)

            self._db_existence_verified = self.big_query_client.does_table_exist(
                self.storage_table
            )

    def add_bookmark(self, bookmark: IngestBookmark) -> IngestBookmark:
        self._init_db_if_needed()

        if self.is_ignored:
            self.logger.debug("State database is ignored, not recording bookmark")
            return bookmark

        bookmark_id = hash(bookmark)

        cleaned_errors = [e.replace("'", "").replace(",", "") for e in bookmark.errors]
        error_str = ",".join(cleaned_errors)

        additional_data = json.dumps(bookmark.additional_data)

        query = f"""
        INSERT INTO `{str(self.storage_table)}`({self.col_list})
        VALUES ({bookmark_id}, '{bookmark.title}', '{bookmark.stream_name}', {bookmark.success}, '{bookmark.pipeline_name}', '{str(bookmark.bookmark_type)}', '{error_str}', '{str(bookmark.timestamp)}', '{additional_data}')
        """
        self.big_query_client._run_no_result_query(full_query=query)
        return bookmark

    def get_all(self) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []
        if not self.big_query_client.does_table_exist(self.storage_table):
            return []
        rows = self.big_query_client.read_table(self.storage_table)
        for row in rows:
            bk = self._row_to_object(row)
            yield bk

    def get_by_pipeline(self, pipeline_name: str) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []

        query = f"SELECT * FROM {self.storage_table.get_sql_string()} WHERE pipeline_name = '{pipeline_name}'"
        rows = self.big_query_client._run_result_query(query=query)

        for row in rows:
            bk = self._row_to_object(row)
            yield bk

    def get_by_type(self, bookmark_type: BookmarkTypes) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []
        if not self.big_query_client.does_table_exist(self.storage_table):
            return []
        query = f"SELECT {self.col_list} from {self.storage_table.get_sql_string()} WHERE bookmark_type = '{str(bookmark_type)}'"

        for row in self.big_query_client._run_result_query(query=query):
            yield self._row_to_object(row)

    def get(self, bookmark_id: int) -> Optional[IngestBookmark]:
        if self.is_ignored:
            return None
        if not self.big_query_client.does_table_exist(self.storage_table):
            return None

        query = f"SELECT {self.col_list} FROM {self.storage_table.get_sql_string()} WHERE id={bookmark_id}"

        for row in self.big_query_client._run_result_query(query=query):
            return self._row_to_object(row)
        return None

    def save(self) -> bool:
        # currently we write all as they come in, so done already
        return True
