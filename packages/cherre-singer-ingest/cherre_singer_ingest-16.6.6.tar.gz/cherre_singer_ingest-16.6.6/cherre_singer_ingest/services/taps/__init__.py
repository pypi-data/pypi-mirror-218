# flake8: noqa
from cherre_singer_ingest.services.taps.google_cloud_csv_bucket_file_tap import (
    GoogleCloudCSVBucketFileTap,
)
from cherre_singer_ingest.services.taps.big_query_table_tap import BigQueryTableTap
from cherre_singer_ingest.services.taps.base_tap import BaseTap
from cherre_singer_ingest.services.taps.google_cloud_json_bucket_file_tap import (
    GoogleCloudBucketJSONFileTap,
)
from cherre_singer_ingest.services.taps.base_file_parsing_tap import BaseFileParsingTap
from cherre_singer_ingest.services.taps.base_google_cloud_bucket_file_tap import (
    BaseGoogleCloudBucketFileTap,
)
from cherre_singer_ingest.services.taps.google_cloud_shapefile_bucket_file_tap import (
    GoogleCloudBucketShapefileFileTap,
)
from cherre_singer_ingest.services.taps.base_ftp_file_tap import BaseFTPFileTap
from cherre_singer_ingest.services.taps.base_google_cloud_bucket_folder_tap import (
    BaseGoogleCloudBucketFolderTap,
)
from cherre_singer_ingest.services.taps.webpage_tap import WebPageTap
from cherre_singer_ingest.services.taps.base_api_tap import BaseAPITap
