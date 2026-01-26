"""
Class to describe csv source file formats
"""

import csv


class Source():
    """
    Read records, one at a time, from csv file
    """
    def __init__(self, filename, pad_cols, split_csz):
        delim = ','
        self.file_hndl = open(filename)
        self.csv_file = csv.reader(self.file_hndl, delimiter=delim)
        self.split_csz = split_csz

    # context manager methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_hndl.close()

    # iterator methods
    def __iter__(self):
        return self

    def __next__(self):
        record = next(self.csv_file)
        return record
