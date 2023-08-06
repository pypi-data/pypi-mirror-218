import paramiko
import logging
from dataclasses import dataclass


@dataclass
class SFTPContext:
    """
    This object is slated for deprecation for the FTP Info Object
    """

    host: str
    port: str
    username: str
    password: str


def get_client(sftp_context: SFTPContext):
    """
    This function is slated for deprecation for the FTP Info Object
    """
    transport = paramiko.Transport((sftp_context.host, int(sftp_context.port)))
    transport.connect(username=sftp_context.username, password=sftp_context.password)
    return paramiko.SFTPClient.from_transport(transport)


def get_folder_list(sftp_context: SFTPContext, folder_path):
    """
    This function is slated for deprecation for the FTP Info Object
    """
    with get_client(sftp_context) as sftp:
        return sftp.listdir(folder_path)


def log_download_progress(downloaded_bytes, total_bytes):
    logging.info(
        f"Downloaded {downloaded_bytes/(1024*1024)} of {total_bytes/(1024*1024)} MB"
    )


def download_file(sftp_context: SFTPContext, sftp_file_path, local_file_path):
    """
    This function is slated for deprecation for the FTP Info Object
    """
    with get_client(sftp_context) as sftp:
        sftp.get(sftp_file_path, local_file_path, log_download_progress)
