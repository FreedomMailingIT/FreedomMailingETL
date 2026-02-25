"""Test Heber Light & Power's convert of their RAW text to FM TSV.

Refactored 2026-02-25 after deprecation warning of os.system() reported.
"""

from pathlib import Path
import subprocess
from shutil import copyfile
import app_modules.utilities as utils


# Prepare for testing
DATA = Path(utils.FILE_PATH)
FNAME = 'hlap Jan 25 CYCLE 2.TXT'
copyfile(DATA / 'archive' / FNAME, DATA / FNAME)
utils.initialize_log_file(path=utils.FILE_PATH)  # utilities expects a string path


def test_hlap_cnvt(fname=FNAME):
    """Test conversion program."""
    command = ['py', 'src/transforms/hlap_cnvrt.py', '-f', fname]
    subprocess.run(command, check=True)


def test_hlap_cnvt_log():
    """Interrogate log to see if conversion was successful."""
    lines = utils.get_last_log_segment()
    assert 'Printed: 250' in lines[-2]


def test_cleanup():
    """Remove results to keep test data directory clean."""
    test_files = [
        p for p in DATA.iterdir()
        if p.name.startswith('fxd') and not p.name.endswith('.zip')
    ]
    for test_file in test_files:
        test_file.unlink(missing_ok=True)
    (DATA / FNAME).unlink(missing_ok=True)


if __name__ == '__main__':
    test_hlap_cnvt()
