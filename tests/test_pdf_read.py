"""Test PyMuPDF which promises fast, cross platform PDF text extract."""


import os
from pathlib import Path
import pymupdf

import app_modules.file_locations as loctns
import app_modules.utilities as utils


# Prepare for testing
TEST_DATA = Path(loctns.TEST_DATA)
utils.initialize_log_file(path=utils.FILE_PATH)
FNAME = 'hlap Aug 2023 cycle 2.pdf'


def test_page_count():
    """Checks number of pages in PDF document."""
    #delete files that may interfere with testing
    for file in Path(TEST_DATA).iterdir():
        if file.match('B47001*.*'):
            os.remove(file)

    with pymupdf.open(TEST_DATA / 'archive' / FNAME) as pdf:
        num = 0
        for num, page in enumerate(pdf):
            text = page.get_text()
            lines = text.split('\n')
            lines[2].isalpha()
        assert num == 249


if __name__ == "__main__":
    test_page_count()
