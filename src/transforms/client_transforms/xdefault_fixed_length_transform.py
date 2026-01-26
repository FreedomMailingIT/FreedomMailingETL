"""
A default implementation of a custom function for transform.py.

Receives csv file handle (for transformed data) and source text to transform.
"""


def transform_data(csv_w, source):
    """Assumes text source that is written unchanged to output file."""
    count = 0
    try:
        with open(source, 'r', encoding='utf8') as source_text:
            for row in source_text:
                if row:  # bypass empty list entry
                    # process csv row
                    csv_w.writerow(row)
                    count += 1
    except Exception as err:
        raise err

    return count
