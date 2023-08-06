import pathlib

from cherre_types import FilePath, FolderPath, BucketFile, File

from cherre_singer_ingest.value_items import URI


class RemoteFileURIFactory:
    """RemoteFileURIFactory will return an Uniform Resource Identifier (URI) on a remote server (FTP, GCS, et cetera).
    If a RemoteFileURI is required for local files, a RemoteFileURI should be generated via the RemoteFileURI.parse() method.

    Returns:
        [type]: [description]

    TODO: Network protocol should be parameterized: ftp, http, etc should be one function
    """

    @staticmethod
    def get_unzipped_file_path(archive_remote_path: URI, file: FilePath) -> URI:
        if "#" in archive_remote_path.value:
            # this is a sub-archive of another
            res = archive_remote_path.value + "/" + file.file.name_with_extension
        else:
            res = archive_remote_path.value + "#" + file.file.name_with_extension

        return URI.parse(res)

    @staticmethod
    def get_ftp_uri_from_local_file(host: str, local_path: FilePath, local_containing_dir: FolderPath) -> URI:
        remote_folder_str = str(local_path.path).replace(str(local_containing_dir), "")
        remote_folder = FolderPath.parse(remote_folder_str)
        return RemoteFileURIFactory.get_ftp_uri(
            host=host, remote_folder=remote_folder, file=local_path.file
        )

    @staticmethod
    def get_ftp_uri(host: str, remote_folder: FolderPath, file: File) -> URI:
        folder_part = str(remote_folder)
        if folder_part.startswith("/"):
            folder_part = folder_part[1:]
        return URI.parse(f"ftp://{host}/{folder_part}/{file.name_with_extension}")

    @staticmethod
    def get_file_path_uri(file: FilePath) -> URI:
        if file.path.folders.startswith("/"):
            path = file.path.folders[1:]
        else:
            path = file.path
        return URI.parse(f"file://{path}/{file.name_with_extension}")

    @staticmethod
    def get_google_bucket_file_uri(bucket_file: BucketFile) -> URI:
        return URI.parse(str(bucket_file))

    @staticmethod
    def get_http_file_uri(host: str, path: FolderPath, file: File) -> URI:
        folder_part = str(path)
        if folder_part.startswith("/"):
            folder_part = folder_part[1:]
        return URI.parse(f"https://{host}/{folder_part}/{file.name_with_extension}")
