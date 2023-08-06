import urllib.request
import uuid
import datetime
import zipfile
import os
import logging
import subprocess
import codecs
import ijson
import shutil
import re
from os.path import isfile, join
from typing import List

from cherre_types import FilePath, File, BucketFile
from cherre_google_clients import GoogleStorageClient, GoogleClientFactory

from cherre_singer_ingest.services.constants import CHERRE_STANDARD_DELIMITER


logging.basicConfig(level=logging.INFO)

temp_folder_name = ".temp"


def get_unique_id():
    return (
        datetime.datetime.utcnow().strftime("%Y_%m_%d_%H_%M")
        + "_"
        + str(uuid.uuid4())[:8]
    )


def create_temp_folder(ephemeral_id=None):
    id = ephemeral_id if ephemeral_id else get_unique_id()
    temp_folder_path = f"{temp_folder_name}/{id}/"
    os.makedirs(temp_folder_path, exist_ok=True)

    return temp_folder_path


def create_temp_file_path(file_name):
    temp_folder_path = create_temp_folder()

    return join(temp_folder_path, file_name)


def clean_up_temp_folder():
    logging.info(f"Clean up {temp_folder_name} local folder")

    shutil.rmtree(f"./{temp_folder_name}")
    os.mkdir(f"./{temp_folder_name}")


def execute_bash_script(bash_script):
    logging.info(f"Execute bash script:\n'{bash_script}'")

    subprocess.run(bash_script, shell=True, check=True)


def unzip(archive_file_path, extract_folder_path, zip_password=None):
    """
    Unzips files, used when client provide us when compressed files.
    :param archive_file_path:
    :param extract_folder_path:
    :param zip_password:
    :return:
    """
    logging.info(f"Unzip {archive_file_path} to {extract_folder_path}")
    with zipfile.ZipFile(archive_file_path, "r") as zip_ref:
        if zip_password:
            zip_ref.setpassword(zip_password.encode())
        zip_ref.extractall(extract_folder_path)


def _rename_single_compressed_file(extract_folder_path: str, uncompressed_file: str):
    file = get_file_list(extract_folder_path)
    assert (
        len(file) == 1
    ), f"Only one uncompressed file accepted after the uncompress, not {len(file)}!"
    os.rename(
        join(extract_folder_path, file[0]), join(extract_folder_path, uncompressed_file)
    )
    logging.info(f"File was renamed from {file[0]} to {uncompressed_file}")


def unzip_7z(
    archive_file_path: str,
    extract_folder_path: str,
    overwrite_switch: str = None,
    zip_password=None,
    uncompressed_file=None,
):
    logging.info(
        f"Unzip the {archive_file_path} to the folder: {extract_folder_path} with the 7z CLI"
    )

    # We need to create the directory before we use `get_file_list`.
    # 7z auto. creates the directory if it doesn't exist, but we need to read the directory beforehand.
    os.makedirs(extract_folder_path, exist_ok=True)

    before_file_list = set(get_file_list(extract_folder_path))

    # Creating the 7z command line to extract the compressed file.
    cmd = ["7z", "x", archive_file_path, f"-o{extract_folder_path}"]

    if overwrite_switch:
        cmd.extend([f"-ao{overwrite_switch}"])

    if zip_password:
        cmd.extend([f"-p{zip_password}"])

    logging.info(f"Executing the command, {cmd}")
    subprocess.check_output(cmd, shell=False)

    if uncompressed_file:
        _rename_single_compressed_file(extract_folder_path, uncompressed_file)

    after_file_list = set(get_file_list(extract_folder_path))
    logging.info(
        f"Extraction complete, the files are {after_file_list - before_file_list}"
    )


def zip_file(output_zip_file, file_to_zip):
    """
    Zips individual files!
    :param output_zip_file:
    :param file_to_zip:
    :return:
    """
    logging.info(
        f"Creating the zip file of {output_zip_file} from the file: {file_to_zip}"
    )
    with zipfile.ZipFile(f"{output_zip_file}", "w") as zip_ref:
        zip_ref.write(file_to_zip)


def download_from_http(url, file_path):
    logging.info(f"Download from {url} to {file_path}")
    urllib.request.urlretrieve(url, file_path)


def get_file_list(folder_path):
    return [f for f in os.listdir(folder_path) if isfile(join(folder_path, f))]


def get_filename_by_file_path(file_path):
    return os.path.basename(file_path)


def get_file_base_extension(file_name):
    return os.path.splitext(file_name)


def get_file_base(file_name):
    file_base, _ = get_file_base_extension(file_name)
    return file_base


def get_file_extension(file_name):
    _, file_extension = get_file_base_extension(file_name)
    return file_extension


def get_filename_by_file_path_for_table_id(file_path):
    file_name = get_filename_by_file_path(file_path)
    file_base = get_file_base(file_name)
    return file_base


def change_file_encoding(
    source_file_path, source_encoding, destination_file_path, destination_encoding
):
    BLOCKSIZE = 1048576

    logging.info(
        f"Change encoding from {source_file_path} {source_encoding} to {destination_file_path} {destination_encoding}"
    )

    with codecs.open(source_file_path, "r", source_encoding) as sourceFile:
        with codecs.open(
            destination_file_path, "w", destination_encoding
        ) as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)


def clean_date_isoformat_from_bigquery(uncleaned_date):
    cleaned_date = uncleaned_date[:-1]
    cleaned_date = cleaned_date + "000+00:00"
    return str(cleaned_date)


def convert_json_to_csv(
    json_file_path: str,
    csv_file_path: str,
    data_start_prefix: str,
    delimiter: str = CHERRE_STANDARD_DELIMITER,
) -> None:
    """Downloads a JSON file by HTTP and converts the JSON file to CSV.
    This method expects a JSON array as the columns, data_start_prefix points to the JSON array.

    Arguments:
        url {str} -- The http url
        file_path {str} -- The path to the csv file
        data_start_prefix {str} -- The object path to the object containing the JSON array (example: 'data.item')

    Keyword Arguments:
        delimiter {str} -- The csv delimiter (default: {"🞈"})

    """

    logging.info(
        f"Convert JSON from {json_file_path} to CSV {csv_file_path} using data_start_prefix={data_start_prefix}"
    )

    with open(json_file_path, "r") as json_file:
        # NOTE: Transient errors when parsing ACRIS
        # See https://cherre.atlassian.net/jira/software/projects/MG/boards/59?selectedIssue=MG-51
        items = ijson.items(json_file, data_start_prefix)

        rows_count = 0

        with open(csv_file_path, "w") as csv_file:
            for item in items:
                csv_row = (
                    delimiter.join(
                        [
                            (str(element) if element is not None else "")
                            for element in item
                        ]
                    )
                    + "\n"
                )
                csv_file.write(csv_row)
                rows_count += 1
                if rows_count % 100000 == 0:
                    logging.info(f"Parsed {rows_count} items from {json_file_path}")

        logging.info(
            f"Converted JSON from {json_file_path} to CSV {csv_file_path} {rows_count} rows"
        )


def convert_shp_to_geojson_cmd(
    file_name_without_extension, csv_like_result_file_path, temp_folder_file_path
) -> str:
    """
    Creates the shp to geojson CLI cmd.
    :param file_name_without_extension:
    :param csv_like_result_file_path:
    :param temp_folder_file_path:
    :return:
    """
    return (
        f"ogr2ogr -f csv -dialect sqlite -sql "
        f"'select AsGeoJSON(geometry) as geom, * from {file_name_without_extension}' "
        f"{csv_like_result_file_path} {temp_folder_file_path}"
    )


def shp_to_geojson(out_file_path: FilePath) -> str:
    """Using a `FilePath` object, the shp to GeoJSON CLI cmd is created.

    Args:
        out_file_path (FilePath): The GeoJSON file that will be created (as a CSV).

    Returns:
        str: [description]
    """
    if not out_file_path:
        raise ValueError("out_file_path must be set!")

    if out_file_path.file.extension != "csv":
        raise ValueError("The out_file_path must be a csv file!")

    file_name = out_file_path.file.name
    folder_path = out_file_path.path.folders
    file_path = os.path.join(folder_path, file_name)

    name = str(File.parse(file_name).name)
    return convert_shp_to_geojson_cmd(name, str(out_file_path), str(file_path))


def file_name_match_regex(file_pattern: str, file_name: str) -> bool:
    """Compare a file_name to a regex file_pattern

    Args:
    :param file_pattern (str): regex file pattern
    :param file_name (str): file name
    :return boolean whether the file_name matches the regex expression
    """
    regex_file_pattern = re.compile(file_pattern)
    return regex_file_pattern.match(file_name) is not None


def get_items_in_regex_filtered_list(file_pattern: str, files: List[str]) -> List[str]:
    """
    Given a list of files, only return files that match the regex file pattern!
    :param file_pattern:
    :param files:
    :return:
    """
    regex_file_pattern = re.compile(file_pattern)
    filtered_list = list(
        filter(lambda i: regex_file_pattern.match(i) is not None, files)
    )

    logging.info(f"All the filtered files are {filtered_list}")

    return filtered_list


def get_last_item_in_regex_filtered_list(file_pattern, files):
    """
    Returns the most recent file from the filtered list!
    :param file_pattern:
    :param files:
    :return:
    """
    files = get_items_in_regex_filtered_list(file_pattern, files)
    most_recent_file = sorted(files, reverse=True)[0]

    logging.info(f"The most recent file in the filtered list is {most_recent_file}")

    return most_recent_file


def zip_directory(compressed_folder_path, extract_from_folder_path):
    """
    Provides functionality to zip an entire directory
    :param compressed_folder_path:
    :param extract_from_folder_path:
    :return:
    """
    shutil.make_archive(compressed_folder_path, "zip", extract_from_folder_path)
    logging.info(
        f"Compressed the files in the folder path, {compressed_folder_path} to {extract_from_folder_path}"
    )


def download_bucket_file_to_local_machine(
    bucket_file: BucketFile, client: GoogleStorageClient = None
) -> FilePath:
    if not client:
        client = GoogleClientFactory().get_storage_client()

    file_path = create_temp_file_path(str(bucket_file.file))
    path = FilePath.parse(file_path)

    local_file = client.download_bucket_file(bucket_file, destination=path.path)
    logging.info(f"Local file: {local_file}")

    return local_file
