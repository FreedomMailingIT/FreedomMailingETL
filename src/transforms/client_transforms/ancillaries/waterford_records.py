"""Definition of various record types in Waterford bill file."""


import decimal as dec

NEG_SIGN = 'CR'
FIELDS = {
    'BILL': [
        'Rec Type',
        'Bill ID',
        'Seq #',
        'Bill Type',
        'Account Number',
        'Account Suffix',
        'CID#',
        'Account Name',
        'Route',
        'Sequence',
        'Service Address 1',
        'Service Address 2',
        'Service City',
        'Service State',
        'Service Zip',
        'Service ZIP4',
        'Mail to Name',
        'Mail to Attention',
        'Mail to Address 1',
        'Mail to Address 2',
        'Mail to City',
        'Mail to State',
        'Mail to Zip',
        'Mail to ZIP4',
        'Mail to Carrier Route',
        'Mail to Delivery Point',
        'IMB Full',
        'Bill Date',
        'Discount Date',
        'Due Date',
        'Service From Date',
        'Service To Date',
        'Previous Balance*',
        'Payments*',
        'Adjustments*',
        'Past Due Balance*',
        'Penalties Applied*',
        'Interest Applied*',
        'Lien Amount*',
        'Current Bill Amount*',
        'Balance Due*',
        'Penalty Amount*',
        'ACH Date',
        'ACH Amount*',
        'Discounted Amount*',
        'Extended Discount Date',
        'Extended Discount Amount*',
        'Last Payment Date',
        'Last Payment Amount*',
        'Extended Discount Name',
        'EDU',
        'Municipality Name',
        'Municipality Code',
        'Units Override',
        'Discounts Taken*',
        'Applied Deposits and Interest*',
        'Shutoff Date',
        'Bill Amount*',
        'Penalty Amount*',
        'Interest Amount*',
        'Leak Detection',
        'Payplan Amount*',
        'OCR Scanline',
        'Ach Flag',
        # 'Parcel Number',
        # 'Tax ID',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved'
        ],
    'MTR': [
        'Rec Type',
        'Bill ID',
        'Seq #',
        'Meter Number',
        'Meter Type',
        'Display Order',
        'Read Date',
        'Previous Reading',
        'Current Reading',
        'Usage',
        'Units',
        'Reading Type',
        'Service Type',
        'Meter Exchange Type',
        'Services',
        'Demand Units',
        'Demand Reading',
        'Previous Reading Date',
        'Meter Size Text',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved'
        ],
    'SVC': [
        'Rec Type',
        'Bill ID',
        'Seq #',
        'Display Order',
        'Service',
        'Type',
        'Amount*',
        'Description',
        'Quantity',
        'Calculation Type',
        'Service Usage',
        # 'Reserved ',
        # 'Reserved ',
        # 'Reserved ',
        # 'Reserved ',
        # 'Reserved '
        ],
    'ADJ': [
        'Rec Type',
        'Date',
        'Bill Heading',
        'Placement',
        'Service',
        'Type',
        'Amount*',
        'Description',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved'
        ],
    'MSG': [
        'Rec Type',
        'Bill ID',
        'Seq #',
        'Message Type',
        'Message Text',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved'
        ],
    'LOAN': [
        'Rec Type',
        'Title',
        'Principle Service Title',
        'Original Amount*',
        'Principle Remaining*',
        'Interest Remaining*',
        'Payment Due*',
        'Interest Due*',
        'Bill Pay Amount*',
        'Interest Pay Amount*',
        'Bill Adjustment Amount*',
        'Interest Adjustment Amount*',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved',
        # 'Reserved'
        ],
    }

class Record():
    """Build and release constructed record from multi-line inputs."""

    def __init__(self):
        """Init."""
        rec_types = FIELDS.keys()
        # max records for each record type
        self.type_max = dict(zip(rec_types, [1, 3, 7, 6, 5, 1]))
        # type start needed as each has varying amounts of system data start
        self.rec_start = dict(zip(rec_types, [4, 3, 4, 1, 3, 1]))
        # type sizes needed as all records have 64 fields, only some used
        self.rec_size = dict(zip(
            rec_types,
            [len(FIELDS[field]) for field in rec_types]
            ))
        self.prev_type = None
        self.reset()

    @staticmethod
    def cnvt_amount(amount):
        """Convert amounts to decimal format."""
        amount = dec.Decimal(amount.replace(',', '') or '0')
        neg_sign = NEG_SIGN if amount < 0 else ' ' * len(NEG_SIGN)
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
        for idx, fld_name in enumerate(FIELDS[rec_type]):
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
        for rec_type, vals in FIELDS.items():
            for item in range(self.type_max[rec_type]):
                for field in vals[self.rec_start[rec_type]:]:
                    if rec_type == 'BILL':
                        headings.append(f'{field}')
                    elif rec_type == 'LOAN':
                        headings.append(f'{rec_type} {field}')
                    else:
                        headings.append(f'{rec_type}{item+1} {field}')
        return headings
