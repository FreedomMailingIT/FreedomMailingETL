"""Test Heber Light & Power's convert and indexing programs."""


import os
from shutil import copyfile
import app_modules.utilities as utils


# Prepare for testing
DATA = utils.FILE_PATH
FNAME = '_hlap Aug 2023 cycle 2'
NEW_FILE = f'{DATA}{FNAME[:1]}.pdf'
copyfile(f'{DATA}/archive/{FNAME}.pdf', NEW_FILE)


def test_hlap_cnvt(fname=f'{FNAME[1:]}.txt'):
    """Test conversion program."""
    assert os.system(f'py src/transforms/hlap_cnvrt.py -f "{fname}"') == 0


def test_hlap_cnvt_log():
    """Intergate log to see if conversion was successful."""
    lines = utils.get_last_log_segment()
    assert 'Not printed: 0' in lines[-1]


def test_cleanup():
    """Archive results to keep test data directory clean."""
    if old_files := [
            x for x in os.listdir(DATA)
            if x.startswith(f'fxd {FNAME}') and not x.endswith('.zip')]:
        utils.archive_files(old_files, DATA)
    if old_files := [
            x for x in os.listdir(DATA)
            if x.startswith('B47001') and not x.endswith('.zip')]:
        utils.archive_files(old_files, DATA)


if __name__ == '__main__':
    test_hlap_cnvt()
