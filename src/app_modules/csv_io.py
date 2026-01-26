"""Module designed to output FreedomMailing results to a CSV file."""


import csv


class CSVhandler:
    """Handle CSV input/ouput."""

    def __init__(self, open_file, headings):
        """Create Dict CSV file using given open file & headings."""
        self.file_ptr = csv.DictWriter(
            open_file, headings, extrasaction='ignore',
            delimiter='\t', lineterminator='\n')
        self.file_ptr.writeheader()

    def write_record(self, row):
        """Write given row to CSV file."""
        self.file_ptr.writerow(row)
