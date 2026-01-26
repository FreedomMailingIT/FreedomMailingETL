"""
A default implementation of a custom function for transform.py.

Receives csv file handle (for transformed data) and source text to transform
"""

import csv


def transform_data(csv_w, source_text):
    """Assumes a csv source that is written unchanged to output file."""
    count = 0
    try:
        csv_r = csv.reader(source_text)
        for row in csv_r:
            if row:  # bypass empty list entry
                # process csv row
                csv_w.writerow(row)
                count += 1
    except Exception as err:
        raise err

    return count
