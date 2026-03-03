"""
Transform for Village of Waterford Muni-Link transform (Dec 2019).

Source file is multi-line per account CSV file that needs to be converted to
single line TSV file for FrrredomMailing.

Started with unknown number of meters, services etc.
"""

import csv
import decimal as dec

from transforms.client_transforms.ancillaries import waterford_fields as wf


class Record():
    """Build and release constructed record from multi-line inputs."""
    def __init__(self):
        rec_types = wf.FIELDS.keys()
        # max records for each record type
        self.type_max = dict(zip(rec_types, [1, 3, 7, 6, 5, 1]))
        # type start needed as each has varying amounts of system data start
        self.rec_start = dict(zip(rec_types, [4, 3, 4, 1, 3, 1]))
        # type sizes needed as all records have 64 fields, only some used
        self.rec_size = dict(zip(
            rec_types,
            [len(wf.FIELDS[field]) for field in rec_types]
            ))
        self.prev_type = None
        self.reset()

    @staticmethod
    def cnvt_amount(amount):
        """Convert amounts to decimal format."""
        amount = dec.Decimal(amount.replace(',', '') or '0')
        neg_sign = wf.NEG_SIGN if amount < 0 else ' ' * len(wf.NEG_SIGN)
        # return '{:0,.2f}{}'.format(abs(dec.Decimal(amount)), neg_sign)
        return f'{abs(dec.Decimal(amount)):0,.2f}{neg_sign}'


    def reset(self):
        """Initialize record ready for new bill."""
        self.record = []
        # setup variables for transaction padding
        self.prev_type = 'BILL'
        self.counts = dict(
            zip(list(self.rec_start), [0]*len(self.rec_start))
            )

    def build(self, row):
        """Add input row to output record."""
        rec_type = row[0]
        type_chg = self.prev_type != rec_type
        if type_chg:
            # build blank transactions to max number of type
            o_type = self.prev_type
            for _ in range(self.type_max[o_type] - self.counts[o_type]):
                blnk = [''] * (self.rec_size[o_type] - self.rec_start[o_type])
                self.record.extend(blnk)
        # row end needed because input has many blank fields at eor
        for idx, fld_name in enumerate(wf.FIELDS[rec_type]):
            if fld_name[-1] == '*':
                # print(row, rec_type, idx, fld_name, row[idx])
                row[idx] = self.cnvt_amount(row[idx])
        new_rec = row[self.rec_start[rec_type]:self.rec_size[rec_type]]
        self.record.extend(new_rec)
        # chg prev_type to handle padding for bills with no mtr service
        self.prev_type = 'MTR' if rec_type == 'BILL' else rec_type
        self.counts[rec_type] += 1

    def get(self):
        """Return constructed record."""
        return self.record

    def len(self):
        """Return length of record."""
        return len(self.record)

    def headings(self):
        """Build headings based on field definitions and MAX numbers."""
        headings = []
        for rec_type, vals in wf.FIELDS.items():
            for item in range(self.type_max[rec_type]):
                for field in vals[self.rec_start[rec_type]:]:
                    if rec_type == 'BILL':
                        headings.append(f'{field}')
                    elif rec_type == 'LOAN':
                        headings.append(f'{rec_type} {field}')
                    else:
                        headings.append(f'{rec_type}{item+1} {field}')
        return headings


def transform_data(csv_writer, source_text):
    """Read csv source transfer data and write to output file."""
    csv_reader = csv.reader(source_text)
    record = Record()
    csv_writer.writerow(record.headings())
    count = 0
    for row in csv_reader:
        if row and row[0] != 'HDR':  # bypass empty line and header
            if (row[0] == 'BILL' and record.len() > 99) or row[0] == 'TLR':
                csv_writer.writerow(record.get())
                count += 1
                record.reset()
            if row[0] != 'TLR':
                record.build(row)
    return count
