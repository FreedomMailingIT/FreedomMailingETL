"""
Test file_system_monitor by copying files into monitored directory
(ususally the tests/data directory, indentified by the FM_FILES=tests
environment variable in both terminal sessions).

The file_system_monitor program needs to be already running in another
terminal session, monitoring the DEST directory.  For this reason this
test program is usually run manually (hence the program 'x_' prefix).

*** Unless a 'test' directory is being monitored the hlap_pdf_idx    ***
*** program will FTP files to server & you will need to delete them. ***

To fully test monitor program at least one example of each type of file
that is monitored should be copied:
- a sort file
- a hlap conversion
- a hlap PDF index
- a transform file

Logging in the terminal sessions where 'x_test_file_system_monitor' is
running will show logging indicating files being copied from the archive
into the 'watched' directory.  Logging in the terminal session running the
'file_system_monitor' program, will show normal logs for file processing.

Logging from both terminal sessions will be recorded in the '.job_execution.log
in the 'watched' directory.
"""


import shutil
import os
import time
import sys
from pathlib import Path

import app_modules.utilities as utils


SOURCE = f'{utils.FILE_PATH}archive/'
DEST = utils.FILE_PATH

CLEANUP_FILES = [  # files that may mess up testing
    'fxd hlap Jan 25 CYCLE 2_PDF.csv',
    'fxd hlap Jan 25 CYCLE 2_PRN.csv',
    'fxd draper water.zip',
    'sorted ashley valley dupes 0310.txt',
    ]
TEST_FILES = [  # files in archive prepended with '_' to indicate they are keepers
    'ashley valley dupes 0310.txt',
    'draper water.zip',
    'hlap Aug 2023 cycle 2.pdf',
    'hlap Jan 25 CYCLE 2.TXT',
    ]


def copy_file(test_file):
    """Copy specified files into monitied direcory."""
    shutil.copyfile(f'{SOURCE}_{test_file}', f'{DEST}{test_file}')
    utils.logger.info('Copied %s to %s', f'{SOURCE}_{test_file}', f'{DEST}{test_file}')


def delete_files():
    """Delete previous temporary files that will foil testing."""
    utils.logger.info('Deleting previously involved files that will foil testing.')
    # static file names
    for file in CLEANUP_FILES + TEST_FILES:
        try:
            os.remove(f'{DEST}{file}')
        except FileNotFoundError:
            pass
    #dynamic file names
    for file in Path(DEST).iterdir():
        if file.match('B47001*.*'):
            os.remove(file)
    time.sleep(3)  # give system time to cleanup


if __name__ == '__main__':
    delete_files()
    utils.initialize_log_file()
    if len(sys.argv) > 1:
        tfile = sys.argv[1]
        copy_file(tfile)
    else:
        for tfile in TEST_FILES:
            copy_file(tfile)
            time.sleep(3)  # don't thrash system
