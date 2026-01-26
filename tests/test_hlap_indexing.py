"""Test Heber Light & Power's indexing programs."""


import os
from shutil import copyfile
import app_modules.utilities as utils


DATA = utils.FILE_PATH


def prepare_for_testing():
    """Copy file to work on from archive."""
    fname = '_hlap Aug 2023 cycle 2.pdf'
    new_file = f'{DATA}{fname[1:]}'
    copyfile(f'{DATA}/archive/{fname}', new_file)
    return fname[1:]


def test_hlap_idx(fname=f'{prepare_for_testing()}'):
    """Test PDF indexing program."""
    command = f'py src/pdf_bill_indexing/hlap_pdf_idx.py -f "{fname}"'
    utils.logger.info('About to execute: %s', command)
    assert os.system(command) == 0


def test_hlap_idx_log():
    """Intergate log to see if indexing was successful."""
    lines = utils.get_last_log_segment()
    assert '250 bills indexed' in lines[-2]


if __name__ == '__main__':
    test_hlap_idx()
