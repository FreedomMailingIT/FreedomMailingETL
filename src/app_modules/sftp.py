"""Object to connect to & work with SFTP server.

Replaces third party module 'pysftp' which was overly complicated
for the required task (for client) and had too many dependicies.
"""

import json
from typing import List

import paramiko  # deprecated?
from app_modules.app_logger import logger


class SftpConnect:
    """Class to put files to remote SFTP server."""

    def __init__(self, config_file: str = 'hlp_sftp.json') -> None:
        """Connect to server using connection details in given file."""
        with open(config_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)

        self.tp = paramiko.Transport(creds['host'], 22)
        self.tp.connect(username=creds['user'], password=creds['pswd'])
        self.sftp_client = paramiko.SFTPClient.from_transport(self.tp)
        logger.info('Connected to "%s"', creds['host'])

    def __enter__(self):
        """Enter function for context manager."""
        return self

    def __exit__(self, *exc) -> None:
        """Exit function for context manager."""
        self.sftp_client.close()
        self.tp.close()

    def put(self, files_to_upload: List[str], path: str = './') -> None:
        """Put files to server."""
        path = self.validate_path(path)
        for file in files_to_upload:
            try:
                # source file has full file path, dest only needs filename
                dest_file = file.split("/")[-1]
                self.sftp_client.put(file, f'{path}{dest_file}')
                logger.info('"%s" successfully put to server', dest_file)
            except Exception as err:  # pylint: disable=W0718:broad-exception-caught
                # catch sepecific exceptions as they occur
                logger.info('"%s" put failed - error "%s"', dest_file, err)
                return False
        return True

    def delete(self, files_to_delete: List[str], path: str = './') -> None:
        """Delete files from server."""
        path = self.validate_path(path)
        for file in files_to_delete:
            try:
                self.sftp_client.remove(f'{path}{file}')
                logger.info('"%s" successfully removed from server.', file)
            except Exception as err:  # pylint: disable=W0718:broad-exception-caught
                # catch sepecific exceptions as they occur
                logger.info('"%s" delete failed - error "%s"', file, err)
                return False
        return True

    def list_dir(self, path: str = './') -> List[str]:
        """List the files in the specified directory of the remote sever."""
        path = self.validate_path(path)
        logger.info('Performing directory list.')
        return list(self.sftp_client.listdir(path))

    @staticmethod
    def validate_path(path: str) -> str:
        """Make sure given path ends with /."""
        path += '' if path.endswith('/') else '/'
        return path
