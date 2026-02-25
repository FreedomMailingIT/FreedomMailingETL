"""Test Heber Light & Power's indexing programs."""


from pathlib import Path
import subprocess
from shutil import copyfile
import app_modules.utilities as utils


DATA = utils.FILE_PATH


# Prepare for testing
DATA = Path(utils.FILE_PATH)
FNAME = 'hlap Aug 2023 cycle 2.pdf'
copyfile(DATA / 'archive' / FNAME, DATA / FNAME)
utils.initialize_log_file(path=utils.FILE_PATH)  # FILE_PATH needed because utilities uses it


def test_hlap_idx(fname=FNAME):
    """Test PDF indexing program."""
    command = ['py', 'src/pdf_bill_indexing/hlap_pdf_idx.py', '-f', fname]
    subprocess.run(command, check=True)


def test_hlap_idx_log():
    """Intergate log to see if indexing was successful."""
    lines = utils.get_last_log_segment()
    assert '250 bills indexed' in lines[-2]


def test_cleanup():
    """Remove results to keep test data directory clean."""
    for test_file in [x for x in DATA.iterdir() if x.name.startswith('B47001')]:
        test_file.unlink(missing_ok=True)
    (DATA / FNAME).unlink(missing_ok=True)


if __name__ == '__main__':
    test_hlap_idx()
