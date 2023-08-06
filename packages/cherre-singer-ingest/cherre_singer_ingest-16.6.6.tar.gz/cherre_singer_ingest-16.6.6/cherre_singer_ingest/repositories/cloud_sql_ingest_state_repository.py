import json
from typing import Optional, List, Iterable, Any
from logging import Logger

import google.auth
import google.auth.transport.requests

from cherre_google_clients import (
    GoogleClientFactory,
    GoogleCloudSQLConnector,
    CloudSQLInstance,
)
from cherre_types import Secret
from cherre_domain import get_project_id

from cherre_singer_ingest.repositories.base_state_repository import (
    BaseIngestStateRepository,
)
from cherre_singer_ingest.value_items import IngestBookmark, BookmarkTypes


class CloudSQLIngestStateRepository(BaseIngestStateRepository):
    _col_list = [
        "id",
        "title",
        "stream_name",
        "success",
        "pipeline_name",
        "bookmark_type",
        "errors",
        "timestamp",
        "additional_data",
    ]

    def __init__(
        self,
        storage_table: Optional[str] = "ingest_state",  # this is the default table!
        cloud_sql_connector: Optional[GoogleCloudSQLConnector] = None,
        cloud_sql_instance: Optional[CloudSQLInstance] = None,
        logger: Optional[Logger] = None,
    ):
        super().__init__(logger=logger)

        self.storage_table = storage_table

        user = self._get_postgres_username()
        project_id = get_project_id()
        cloud_sql_instance = cloud_sql_instance or CloudSQLInstance(
            instance="ingest-state",
            region="us-east4",
            user=user,
            db="ingest_state",
        )
        self.cloud_sql_connector = (
            cloud_sql_connector
            or GoogleClientFactory().get_google_cloud_sql_connector(
                cloud_sql_instance=cloud_sql_instance,
                google_cloud_project=project_id,
            )
        )

        # Currently used just to escape databases that can't store in the state repository!
        self.is_ignored = not self.cloud_sql_connector.does_database_exist()
        if not self.is_ignored:
            self.create_ingest_state_table()

    def _get_postgres_username(self) -> List[str]:
        # The project_id only return the Cherre projects (i.e., cherre-sandbox)
        credentials, unused_project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        # When using workload identity, we need to refresh the token to learn the
        # service account email
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        try:
            service_account_email = credentials.service_account_email
            user = service_account_email.replace(
                ".gserviceaccount.com", ""
            )  # For IAM, we need to clean the SA!

        # When configured via Google Cloud SDK, the SA (even when using the "cherre-sandbox-airflow" SA)
        # doesn't have the `service_account_email` property!
        except AttributeError:
            # When authenticated via Google Cloud SDK, we will default to devteam group!
            user = "devteam@cherre.com"

        return user

    def _get_column_values_from_bookmark(self, bookmark: IngestBookmark) -> List[Any]:
        bookmark_id = hash(bookmark)

        cleaned_errors = [e.replace("'", "").replace(",", "") for e in bookmark.errors]
        error_str = ",".join(cleaned_errors)

        additional_data = json.dumps(bookmark.additional_data)

        return [
            bookmark_id,
            bookmark.title,
            bookmark.stream_name,
            bookmark.success,
            bookmark.pipeline_name,
            str(bookmark.bookmark_type),
            error_str,
            str(bookmark.timestamp),
            additional_data,
        ]

    def get_all(self) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []

        rows = self.cloud_sql_connector.read_table(self.storage_table)

        for row in rows:
            bk = self._row_to_object(row)
            yield bk

    def get_by_pipeline(self, pipeline_name: str) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []

        query = f"SELECT * FROM {self.storage_table} WHERE pipeline_name = '{pipeline_name}'"
        rows = self.cloud_sql_connector.run_query(query=query)

        for row in rows:
            bk = self._row_to_object(row)
            yield bk

    def get(self, bookmark_id: int) -> Optional[IngestBookmark]:
        if self.is_ignored:
            return None

        query = (
            f"SELECT {self._col_list} FROM {self.storage_table} WHERE id={bookmark_id}"
        )
        rows = self.cloud_sql_connector.run_query(query=query)

        if len(rows) == 1:
            return self._row_to_object(rows[0])
        elif len(rows) < 1:
            return None
        else:
            self.logger.info(
                f"There are multiple occurrences for {bookmark_id}, unable to identify which row to return."
            )
            raise Exception

    def get_by_type(self, bookmark_type: BookmarkTypes) -> Iterable[IngestBookmark]:
        if self.is_ignored:
            return []

        query = f"SELECT {self._col_list} from {self.storage_table} WHERE bookmark_type = '{str(bookmark_type)}'"
        rows = self.cloud_sql_connector.run_query(query=query)

        for row in rows:
            yield self._row_to_object(row)

    def add_bookmark(self, bookmark: IngestBookmark) -> IngestBookmark:
        if self.is_ignored:
            self.logger.info("State database is ignored, not recording bookmark")
            return bookmark

        col_values = self._get_column_values_from_bookmark(bookmark)

        self.cloud_sql_connector.insert_row(
            table=self.storage_table,
            column_names=self._col_list,
            column_values=col_values,
        )
        return bookmark

    @property
    def does_database_exist(self) -> bool:
        if self.cloud_sql_connector.does_database_exist():
            return True
        return False

    @staticmethod
    def _get_ingest_table_schema() -> str:
        return """
            id              text PRIMARY KEY,
            title           text,
            stream_name     text,
            success         boolean,
            pipeline_name   text,
            bookmark_type   text,
            errors          text,
            timestamp       timestamp with time zone,
            additional_data text
        """

    def create_ingest_state_table(self) -> Optional[str]:
        if self.cloud_sql_connector.does_table_exist(self.storage_table):
            return self.storage_table

        storage_table = self.cloud_sql_connector.create_table(
            table=self.storage_table, schema=self._get_ingest_table_schema()
        )
        return storage_table

    def save(self) -> bool:
        # currently we write all as they come in, so done already
        return True
