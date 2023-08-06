import logging
from os.path import join
from typing import List, Optional
from datetime import datetime

from google.api_core import page_iterator
from cherre_google_clients import GoogleClientFactory

from cherre_singer_ingest.services import common

logging.basicConfig(level=logging.INFO)

"""GCS(Google Cloud Storage) terminology
GCS URI example
'gs://test/path/to/file.txt'
where
'test' is bucket_name
'/path/to/file.txt' is path_to_blob
'/path/to/' is path_to_blob_folder
"""


def download(bucket_name, path_to_blob, local_file_path):
    """Downloads file from GCS to local file system
    DEPRECATED use cherre google client instead!
    Args:
        bucket_name (string): Bucket name
        path_to_blob (string): Path to file in bucket
        local_file_path (string): Local file system file path
    """

    logging.info(
        "Download from gs://{}/{} to {}".format(
            bucket_name, path_to_blob, local_file_path
        )
    )

    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(path_to_blob)

    with open(local_file_path, mode="wb") as file_obj:
        client.download_blob_to_file(blob, file_obj)


def get_storage_client():
    client_wrapped = GoogleClientFactory().get_storage_client()
    client = client_wrapped.google_client
    return client


def upload(bucket_name, path_to_blob, local_file_path):
    """Uploads file to GCS to local file system
    DEPRECATED use cherre google client instead!
    Args:
        bucket_name (string): Bucket name
        path_to_blob (string): Path to file in bucket
        local_file_path (string): Local file system file path
    """

    logging.info(
        "Upload {} to gs://{}/{}".format(local_file_path, bucket_name, path_to_blob)
    )

    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(path_to_blob)
    blob.upload_from_filename(filename=local_file_path)


def unzip(
    source_bucket_name,
    source_path_to_blob_archive,
    destination_bucket_name,
    destination_path_to_blob_folder,
    zip_password: str = None,
    uncompressed_new_file_name: str = None,
):
    """Unzips inside GCS. Downloads archive file from GCS to local file system,
    unzips archive file in local file system,
    uploads archive file content to GCS
    Args:
        source_bucket_name (string): Archive source file bucket name
        source_path_to_blob_archive (string): Archive source file path to blob
        destination_bucket_name (string): Destination extracted archive bucket name
        destination_path_to_blob_folder (string): Destination extracted archive path to blob folder
        zip_password (string): Password for zip files that require a password
        uncompressed_new_file_name (string): Functionality to rename a single uncompressed file.
    """

    logging.info(
        "Unzip gs://{}/{} to gs://{}/{}".format(
            source_bucket_name,
            source_path_to_blob_archive,
            destination_bucket_name,
            destination_path_to_blob_folder,
        )
    )

    archive_file_path = common.create_temp_file_path("archive.zip")

    download(source_bucket_name, source_path_to_blob_archive, archive_file_path)

    extracted_zip_folder_path = common.create_temp_folder()

    common.unzip_7z(
        archive_file_path,
        extracted_zip_folder_path,
        zip_password,
        uncompressed_new_file_name,
    )

    file_list = common.get_file_list(extracted_zip_folder_path)

    for file in file_list:
        upload(
            destination_bucket_name,
            join(destination_path_to_blob_folder, file),
            join(extracted_zip_folder_path, file),
        )


def copy_file(from_bucket_name, from_path_to_blob, to_bucket_name, to_path_to_blob):
    """Copies file inside GCS
    Args:
        from_bucket_name (string): Copying source bucket name
        from_path_to_blob (string): Copying source path to blob
        to_bucket_name (string): Copying destination bucket name
        to_path_to_blob (string): Copying destination path to blob
    """

    logging.info(
        "Copy file from gs://{}/{} to gs://{}/{}".format(
            from_bucket_name, from_path_to_blob, to_bucket_name, to_path_to_blob
        )
    )

    client = get_storage_client()

    source_bucket = client.get_bucket(from_bucket_name)
    source_blob = source_bucket.blob(from_path_to_blob)
    destination_bucket = client.get_bucket(to_bucket_name)

    source_bucket.copy_blob(source_blob, destination_bucket, to_path_to_blob)


def get_file_list(
    bucket_name: str, path_to_blob_folder: str, delimiter: Optional[str] = "/"
):
    """Gets file list for blob folder
    Args:
        bucket_name (string): Bucket name
        path_to_blob_folder (string): Path to blob folder
    Returns:
        array[string]: List of file names
        e.g.
        [
            "1.txt",
            "2.txt",
            "3.txt",
        ]
        :param bucket_name:
        :param path_to_blob_folder:
        :param delimiter:
    """

    logging.info(
        f"Get file list from bucket {bucket_name} by folder path {path_to_blob_folder}"
    )

    client = get_storage_client()

    source_bucket = client.bucket(bucket_name)
    path_to_blob_folder = (
        path_to_blob_folder
        if path_to_blob_folder.endswith("/")
        else path_to_blob_folder + "/"
    )
    blob_list = source_bucket.list_blobs(
        prefix=path_to_blob_folder, delimiter=delimiter
    )

    return list(
        map(lambda blob: common.get_filename_by_file_path(blob.name), blob_list)
    )


def get_folder_list(bucket_name: str, path_to_folder: str) -> List[str]:
    """Gets file list for blob folder
    Extract folders by using this approach in
    https://github.com/googleapis/google-cloud-python/issues/920#issuecomment-326125992
    Args:
        bucket_name (string): Bucket name
        path_to_folder (string): Path to folder
    Returns:
        array[string]: List of folders (prefixes)
        :param bucket_name:
        :param path_to_folder:
    """
    path_to_folder = (
        path_to_folder if path_to_folder.endswith("/") else path_to_folder + "/"
    )
    blob_iterator = _get_blobs(bucket_name, path_to_folder, "/")

    # in order to get all folders we need to loop though all pages
    # that will populate 'prefixes' property
    for page in blob_iterator.pages:
        pass

    return list(blob_iterator.prefixes)


def get_blob_path_list_modified_after(
    bucket_name,
    path_to_blob_folder,
    start_date: datetime,
    delimiter: Optional[str] = "/",
) -> List[str]:
    blobs = _get_blobs(bucket_name, path_to_blob_folder, delimiter)

    in_range = [blob for blob in blobs if blob.time_created > start_date]

    return list(map(lambda blob: blob.name, in_range))


def get_blob_path_list(
    bucket_name: str, path_to_blob_folder: str, delimiter: Optional[str] = "/"
) -> List[str]:
    """Gets list of paths to blobs for blob folder
    Args:
        bucket_name (string): Bucket name
        path_to_blob_folder (string): Path to blob folder
    Returns:
        array[string]: List of pathes to blobs
        e.g.
        [
            "/path/to/blob/folder/1.txt",
            "/path/to/blob/folder/2.txt",
            "/path/to/blob/folder/3.txt",
        ]
        :param bucket_name:
        :param path_to_blob_folder:
        :param delimiter:
    """

    blob_list = _get_blobs(bucket_name, path_to_blob_folder, delimiter)

    return list(map(lambda blob: blob.name, blob_list))


def get_file_size(
    bucket_name: str, path_to_blob_folder: str, file_name: str
) -> Optional[int]:
    client = get_storage_client()
    logging.info(
        f"Getting information for {bucket_name}/{path_to_blob_folder}/{file_name}"
    )
    bucket = client.bucket(bucket_name)
    blob = bucket.get_blob(f"{path_to_blob_folder}/{file_name}")

    if blob:
        return blob.size

    return None


def _get_blobs(
    bucket_name: str, path_to_blob_folder: str, delimiter: Optional[str] = "/"
) -> page_iterator.HTTPIterator:
    client = get_storage_client()
    logging.info(
        f"Getting file list for Bucket: {bucket_name} and Folder: {path_to_blob_folder}"
    )

    source_bucket = client.bucket(bucket_name)
    blob_list = source_bucket.list_blobs(
        prefix=path_to_blob_folder, delimiter=delimiter
    )
    logging.info(f"Raw blob list: {blob_list}")
    return blob_list


def copy_folder(
    from_bucket_name, from_path_to_blob_folder, to_bucket_name, to_path_to_blob_folder
):
    """Copies folder inside GCS
    Args:
        from_bucket_name (string): Copying source bucket name
        from_path_to_blob_folder (string): Copying source path to blob folder
        to_bucket_name (string): Copying destination bucket name
        to_path_to_blob_folder (string): Copying destination path to blob folder
    Additional Info:
        This function is required when a file is in the adhoc bucket. Copying csv files to the BigQuery
        requires developers to have the csv (or any file) to be in the ingestion bucket
    """

    if not from_path_to_blob_folder.endswith("/"):
        raise ValueError(
            "The folder path must end in an /, or no files will be extracted!"
        )

    logging.info(
        "Copy folder from gs://{}/{} to gs://{}/{}".format(
            from_bucket_name,
            from_path_to_blob_folder,
            to_bucket_name,
            to_path_to_blob_folder,
        )
    )

    client = get_storage_client()

    source_bucket = client.bucket(from_bucket_name)
    blob_list = source_bucket.list_blobs(prefix=from_path_to_blob_folder, delimiter="/")

    for blob in blob_list:
        copy_file(
            from_bucket_name,
            blob.name,
            to_bucket_name,
            join(to_path_to_blob_folder, common.get_filename_by_file_path(blob.name)),
        )

        logging.info(f"Copied the file from {from_bucket_name} to {to_bucket_name}")


def get_blobs_by_extension_in_bucket(
    bucket_name: str, folder_in_bucket: str, file_extension: str = "csv"
) -> List[str]:
    """Gets the csv files from the bucket specified above (could have a different file extension)
    Arguments:
        bucket_name {str} -- [the ingest bucket (i.e. "cherre-sandbox-data-ingestion-dump")]
        folder_in_bucket {str} -- [the path to the file in the dest. bucket (i.e. "ingest/zip4/csv_files/"]
    Keyword Arguments:
        file_extension {str} -- [the extension to be filtered from the bucket] (default: {"csv"})
    Returns:
        List[str] -- [A list of filered files from the specified bucket]
    """

    blob_path_list = get_blob_path_list(
        bucket_name, path_to_blob_folder=folder_in_bucket, delimiter=None
    )
    ext_blob_path_list = list(
        filter(lambda blob: blob.endswith(f".{file_extension}"), blob_path_list)
    )

    logging.info(
        f"The blob path of the {file_extension} files are {ext_blob_path_list}"
    )
    return ext_blob_path_list
