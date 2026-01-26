"""
A default implementation of a custom function for transform.py.

Receives csv file handle (for transformed data) and source text to transform
"""

import transforms.client_transforms.ancillaries.xfixed_length_fields as fields


# # define constants here for code brevity & clarity
NAME = 0
START = 1
END = 2
EOR_MARKER = '^'

ACCT_NO_COL = fields.ACCT_NO_COL
BARCODE_COL = fields.BARCODE_COL
ACH_DIRECT_PAY = fields.ACH_DIRECT_PAY
WATER_HIST_START = fields.WATER_HIST_START
ELECT_HIST_START = fields.ELECT_HIST_START
HIST_END = fields.HIST_END_COL
PAPERLESS = fields.FIELDS[fields.PAPERLESS]


def _convert_to_columns(row_in):
    """Converts fixed length records to columns for processing."""
    return [row_in[x[START]:x[END]].strip() for x in fields.INCLUDE]


def _massage_data_(row_in):
    """Massage data to meet client requirements."""
    row_out = row_in

    # Create digits only Acct# in column 'Barcode (unformatted)' for printing
    row_out[BARCODE_COL] = (
        row_out[ACCT_NO_COL].replace('.', '') + fields.BARCODE_SUFFIX
        if row_out[BARCODE_COL] != 'Barcode'
        else row_out[BARCODE_COL]
        )

    # Set Direct Pay message
    if len(row_out[ACH_DIRECT_PAY]) == 1:
        row_out[ACH_DIRECT_PAY] = 'DO NOT PAY - AUTOPAY' if row_out[ACH_DIRECT_PAY] == 'T' else ''

    # Group history data by service (bypass to return to cols for HIST)
    water = [(row_out[idx], row_out[idx+1]) for idx in range(WATER_HIST_START, HIST_END, 4)]
    elect = [(row_out[idx], row_out[idx+1]) for idx in range(ELECT_HIST_START, HIST_END, 4)]

    idx = WATER_HIST_START
    for water_lbl, water_use in water:
        row_out[idx] = water_lbl
        row_out[idx+1] = water_use
        idx += 2

    # idx carries over from last loop
    for elect_lbl, elect_use in elect:
        row_out[idx] = elect_lbl
        row_out[idx+1] = elect_use
        idx += 2

    row_out[-1] = row_out[-1] or EOR_MARKER  # add EOR character if missing

    return row_out


def transform_data(csv_w, source_text):
    """Output required headings and columns (based on '*' being 1st char in heading)."""
    try:
        csv_w.writerow(_massage_data_(fields.HEADINGS))
        count = 0
        for row in source_text:
            # bypass empty row & paperless
            if row and row[PAPERLESS[START]:PAPERLESS[END]] == 'F':
                if not isinstance(row, list):
                    row = _convert_to_columns(row)
                csv_w.writerow(_massage_data_(row))
                count += 1
    except Exception as err:
        raise err

    return count
