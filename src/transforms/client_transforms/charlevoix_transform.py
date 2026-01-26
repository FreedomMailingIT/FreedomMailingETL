"""
A default implementation of a custom function for transform.py.

Receives csv file handle (for transformed data) and source text to transform
"""


from decimal import Decimal as dec
import csv
import transforms.client_transforms.ancillaries.charlevoix_fields as fields


# define constants here for code brevity
ACCT_NO_COL = fields.ACCT_NO_COL
BARCODE_COL = fields.BARCODE_COL
CURRENT_CHARGES = fields.CURRENT_CHARGES
CURRENT_BILLING = fields.CURRENT_BILLING
CURRENT_TAX = fields.CURRENT_TAX
ACH_DIRECT_PAY = fields.ACH_DIRECT_PAY
MESSAGE_LINES = fields.MESSAGE_LINES
WATER_HIST_START = fields.WATER_HIST_START
ELECT_HIST_START = fields.ELECT_HIST_START
HIST_END = fields.HIST_END_COL
PAPERLESS = fields.FIELDS[fields.PAPERLESS]
NAME = fields.FIELD_NAME
START = fields.FIELD_START
END = fields.FIELD_END


def _convert_to_columns(row):
    """Converts fixed length records to columns for processing."""
    return [row[x[START]:x[END]].strip() for x in fields.SELECTED]


def _massage_data_(row):
    """Massage data to meet client requirements."""
    # Create digits only Acct# in column 'Barcode' for printing
    row[BARCODE_COL] = (
        row[ACCT_NO_COL].replace('.', '') + fields.BARCODE_SUFFIX
        if row[BARCODE_COL] != 'Barcode'
        else row[BARCODE_COL]
        )

    # Set Direct Pay message
    if len(row[ACH_DIRECT_PAY]) == 1:
        row[ACH_DIRECT_PAY] = 'DO NOT PAY - AUTOPAY' if row[ACH_DIRECT_PAY] == 'T' else ''

    # Calculate CURRENT_CHARGES
    if row[CURRENT_CHARGES] != 'Current Charges':
        row[CURRENT_CHARGES] = str( dec(row[CURRENT_BILLING]) + dec(row[CURRENT_TAX]) )

    # Group history data by service (bypass to return to cols for HIST)
    water = [(row[idx], row[idx+1]) for idx in range(WATER_HIST_START, HIST_END, 4)]
    elect = [(row[idx], row[idx+1]) for idx in range(ELECT_HIST_START, HIST_END, 4)]

    idx = WATER_HIST_START
    for water_lbl, water_use in water:
        row[idx] = water_lbl
        row[idx+1] = water_use
        idx += 2

    # idx carries over from last loop
    for elect_lbl, elect_use in elect:
        row[idx] = elect_lbl
        row[idx+1] = elect_use
        idx += 2

    row[-1] = row[-1] or fields.EOR_CHAR  # add EOR character if missing

    return row


def transform_data(csv_w, source_text):
    """Output required headings and columns (based on '*' being 1st char in heading)."""
    try:
        csv_w.writerow(_massage_data_(fields.HEADINGS))

        # test for delimited record, otherwise fixed length records
        if source_text[0].count(',')>1000 or source_text[0].count('\t')>1000:
            records = csv.reader(source_text, delimiter='\t' if '\t' in source_text[0] else ',')
            paperless_field = fields.PAPERLESS
        else:
            records = source_text
            paperless_field = fields.FIELDS[fields.PAPERLESS][START]

        count = 0
        for row in records:
            if row and row[paperless_field] == 'F':  # bypass empty row & paperless
                if paperless_field == fields.PAPERLESS:  # delimited file
                    clean_row = [x.strip() for idx, x in enumerate(row) if idx in fields.INCLUDE]
                else:
                    clean_row = _convert_to_columns(row)
                csv_w.writerow(_massage_data_(clean_row))
                count += 1
    except Exception as err:
        raise err

    return count
