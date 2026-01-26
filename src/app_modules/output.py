"""
Classes describing Freedom Mailing output file
"""

import csv
import os
import zipfile


class Output():
    """
    Write output to tab delimited CSV file
    """
    def __init__(self, filename, de_dup, zip_me, comma):
        self.file_hndl = open(filename, 'w')
        self.filename = filename
        self.de_dup = de_dup
        self.zip_fn = filename.split('.')[0] + '.zip' if zip_me else None
        self.unique = set()
        self.csv_w = csv.writer(
            self.file_hndl,
            delimiter=',' if comma else '\t',
            lineterminator='\n'
            )

    def write(self, record):
        if self.de_dup:
            # this outputs record in random order
            self.unique.add(tuple(record))
        else:
            self.csv_w.writerow(record)

    # context manager methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.de_dup:
            for row in self.unique:
                self.csv_w.writerow(row)
        self.file_hndl.close()
        if self.zip_fn:
            try:
                # delete existing file (if there) to avoid duplication
                os.remove(self.zip_fn)
            except OSError:
                # not a problem the file was not there
                pass
            with zipfile.ZipFile(self.zip_fn, 'a') as zip_file:
                filename = self.filename.split('/')[-1]
                zip_file.write(self.filename, filename, zipfile.ZIP_DEFLATED)
                os.remove(self.filename)
