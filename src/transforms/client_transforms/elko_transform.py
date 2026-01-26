"""
Convert city XML billing files into CSV files.

City supplies four files to be processed, all with same format.
Receives csv file handle (for transformed data) and source text to transform
"""


import xml.etree.ElementTree as et
from io import StringIO  # Py3

import transforms.client_transforms.ancillaries.elko_fields as ef


def to_currency(number):
    """Convert amount to standard currency format 0.00."""
    dpoint = number.find('.')
    if dpoint == -1:
        return f'{number}.00'
    if dpoint == len(number) - 2:
        return f'{number}0'
    return number


def get_headings():
    """Create headings for output file."""
    col_specs = (
        ef.prefix_cols +
        ef.bill_fields +
        ef.postfix_cols +
        (ef.charges_cols * 6) +
        (ef.meter_cols * 20)
        )
    return [item[0] for item in col_specs]


def transform_data(csv_w, source_text):
    """Transform XML file into CSV file."""
    fname = StringIO('\n'.join(source_text))
    bills = et.ElementTree(file=fname).getroot()
    csv_w.writerow(get_headings())

    # get billing messages
    bill_msg = bills.findtext('BillingMessage')
    stub_msg = bills.findtext('StubMessage')
    due_date = bills.findtext('DueDate')

    # cycle through billing records
    count = 0
    for bill in bills.iter('BILL'):
        count += 1
        # output billing due date
        out_rec = [due_date]

        # output account information
        for field, ntype in ef.bill_fields:
            try:
                if ntype == 'c':
                    out_rec.append(to_currency(bill.attrib[field]))
                else:
                    out_rec.append(
                        bill.attrib[field].
                        replace('&amp;', '&').
                        replace('  ', ' ').
                        replace('  ', ' ').
                        rstrip()
                        )
            except KeyError:
                out_rec.append('')

        # output billing messages
        out_rec.append(bill_msg)
        if stub_msg != '':
            out_rec.append(stub_msg)
        else:
            try:
                out_rec.append(
                    'Direct Pay amount will be processed on or about ' +
                    bill.attrib['BankDraftDate']
                    )
            except KeyError:
                out_rec.append('')

        #  output account billing records
        charge_no = 0
        for charge in bill.iter('CHARGES'):
            if charge.attrib['Parent'] == '1':
                # assumes parent (summary record) always exits (it should)
                out_rec.append(
                    charge.attrib['ChargeCategoryDescription'].
                    replace(' Summary', '')
                    )
                out_rec.append(
                    to_currency(charge.attrib['Amount'])
                    )
                charge_no += 1
        # fill in blank columns to make up six service charges
        while charge_no < 6:
            out_rec.extend(('', ''))
            charge_no += 1

        # output account meter information
        for service in bill.iter('CONSUMPTION'):
            try:
                out_rec.append(service.attrib['MeterSize'].replace('""', '"'))
            except KeyError:
                out_rec.append('')
            out_rec.append(service.attrib['MeterType'])
            try:
                out_rec.append(service.attrib['PreviousRead'])
            except KeyError:
                out_rec.append('')
            try:
                out_rec.append(service.attrib['CurrentRead'])
            except KeyError:
                out_rec.append('')
            out_rec.append(service.attrib['Consumption'])

        # output account meter history
        csv_w.writerow(out_rec)
    return count
