"""Transform Eagle Mtn source file into format needed by Freedom Mailing."""


import csv
import decimal


ACC_NUM = 0
SEQ_NUM = 1
PAY_AMT = 56
TOTAL_BAL = 60
CURR_BILL = 59
NEW_AMT_POS = 130
CURR_USAGE_COLS = (113, 118)
HIST_USAGE_COLS = (183, 208)
# cols_to_conv = [55, 56, 57, 58, 59, 60]


"""
Electric -> columns Q and AK
Natural Gas -> columns R and AL
Sales Tax -> columns U and AO
Utility Tax -> columns V and AP
Electric Demand -> columns Y and AS
"""
COLS_TO_BLANK = (
    16, 17, 20, 21, 24,  # unused service descriptions
    36, 37, 40, 41, 44,  # unused service amounts
    )
METER_DATA_COLS = (
    84, 85, 86, 87, 88,
    96, 97, 98, 99, 100,
    108, 109, 110, 111, 112,
    114, 115, 116, 117, 118,
    )


def blank_unused_cols(row):
    """Modify column contents for unused cols."""
    return ['' if i in COLS_TO_BLANK else x for i, x in enumerate(row)]


def blank_zero_amounts(row):
    """Modify column contents for zero amounts."""
    return ['' if x == '0.00' else x for x in row]


def blank_zero_meters(row):
    """Modify column contents for zero meter read."""
    return ['' if i in METER_DATA_COLS and x == '0' else x
            for i, x in enumerate(row)]


def transform_data(csv_w, source_text):
    """Convert Eagle Mtn source CSV into required format."""
    csv_r = csv.reader(source_text)
    col_count = len(next(csv_r))  # read 1st record & count cols

    csv_r = csv.reader(source_text)  # reset to beg of file to process file
    count = 0
    for row in csv_r:
        if row:  # bypass empty list entry
            if col_count > 209:
                # skip extra cols in new file format (2021-03)
                row = row[:52] + row[55:]
            past_due_amt = decimal.Decimal(row[TOTAL_BAL])\
                - decimal.Decimal(row[CURR_BILL])

            row[ACC_NUM] = f'{int(row[ACC_NUM]):06d}'  #.format(int(row[ACC_NUM]))
            row[SEQ_NUM] = f'{int(row[SEQ_NUM]):03d}'  #.format(int(row[SEQ_NUM]))
            row[PAY_AMT] = f'{row[PAY_AMT]}CR' if row[PAY_AMT] > '0' else ''
            row[NEW_AMT_POS] = f'{max(past_due_amt, 0):9.2f}'.strip()
            for col in range(CURR_USAGE_COLS[0], CURR_USAGE_COLS[1] + 1):
                if row[col]:
                    row[col] = f'{int(float(row[col])):d}'  #.format(int(float(row[col])))
            for col in range(HIST_USAGE_COLS[0], HIST_USAGE_COLS[1] + 1):
                if row[col]:
                    row[col] = f'{int(float(row[col])):d}'  #.format(int(float(row[col])))
            row = blank_unused_cols(row)
            row = blank_zero_amounts(row)
            row = blank_zero_meters(row)
            csv_w.writerow(row)
            count += 1
    return count
