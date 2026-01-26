"""Test the ability to connect to HL&P FTP sever."""


# from modules.sftp import SftpConnect
# import modules.utilities as utils


# sftp_server = SftpConnect()
# files_to_upload = ['requirements.txt', 'file_loctn.json']


# def test_connection():
#     """Make sure can connect to server."""
#     assert sftp_server.list_dir()


# def test_put():
#     """Put files to server."""
#     assert sftp_server.put(files_to_upload)


# def test_delete():
#     """Delete files on server."""
#     assert sftp_server.delete(files_to_upload)


# def test_log_for_removals():
#     """Intergate log to see if removals were successful."""
#     lines = utils.get_last_log_segment(lines=5)
#     assert str(lines).count('removed') == 2
