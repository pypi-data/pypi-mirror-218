# flake8: noqa
from cherre_singer_ingest.services.get_login_token import get_login_token
from cherre_singer_ingest.services.run_command import (
    run_tap_and_target,
    write_values_to_config_file,
)
from cherre_singer_ingest.services.taps import (
    BaseTap,
    BigQueryTableTap,
    GoogleCloudCSVBucketFileTap,
    BaseFileParsingTap,
    BaseGoogleCloudBucketFileTap,
    GoogleCloudBucketShapefileFileTap,
    BaseGoogleCloudBucketFolderTap,
    BaseFTPFileTap,
    WebPageTap,
    BaseAPITap
)
from cherre_singer_ingest.services.targets import (
    CherreParsedDataLakeTarget,
    BaseCherreTarget,
)
from cherre_singer_ingest.services.targets import (
    BaseCherreTarget,
    CherreParsedDataLakeTarget,
    CherreBigQueryExternalDataTarget,
)
from cherre_singer_ingest.services.env_var_utils import get_bool_environmental_variable
from cherre_singer_ingest.services.common import (
    get_filename_by_file_path_for_table_id,
    get_filename_by_file_path,
    download_from_http,
    create_temp_file_path,
    get_file_base,
    create_temp_folder,
    unzip,
    get_file_list,
    execute_bash_script,
    clean_up_temp_folder,
    unzip_7z,
    get_items_in_regex_filtered_list,
    convert_json_to_csv,
    convert_shp_to_geojson_cmd,
    shp_to_geojson,
    zip_directory,
    zip_file,
    clean_date_isoformat_from_bigquery,
    download_bucket_file_to_local_machine,
)
import cherre_singer_ingest.services.sftp as sftp
from cherre_singer_ingest.services.flatten_object import flatten_object
from cherre_singer_ingest.services.streams import (
    BaseTapStream,
    BaseFileParsingTapStream,
    CSVFileStream,
    AVROFileStream,
    FixedWidthFileStream,
    ShapefileFileStream,
    RESTStream,
    CachedStream,
    JSONFileStream,
    Prop,
)
from cherre_singer_ingest.services.unzip_service import UnzipService
from cherre_singer_ingest.services.unzip_service_with_bookmarks import (
    UnzipServiceWithBookmarks,
)
from cherre_singer_ingest.services.run_custom_image_tap import (
    run_custom_image_tap,
    get_required_env,
)
from cherre_singer_ingest.services.bookmark_service import BookmarkService
