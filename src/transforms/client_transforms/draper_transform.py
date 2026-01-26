"""
Convert city XML billing files into CSV files.

City supplies two files to be processed, both with same format.

Receives csv file handle (for transformed data) and source text to transform
Apart from converting their files from XML format to CSV format and cleaning
up the data:
- removing leading zero's
- using 'CR' for credit amounts
- removing double spaces
- changing codes like '&amp;' to '&'
the program does the following:

1)  Combines 'GARBAGE/RECYCLE' service with the '300 GAL GARBAGE' service and
total those two services into one amount called 'Garbage/Recycle'.
2)  The only other totaling done is used to make sure the program has caught
all service amounts, but this is only done on test runs, not normal runs.
3)  We only look for a maximum of ten services for each account.  If there
are more than ten services they will be missed, so if Draper adds services
without telling us, there may be problems.

That's all I can see at the moment.  It is possible is missed something.
"""


import decimal as dec
import itertools
import xml.etree.ElementTree as et  # noqa (camelcase)
from io import StringIO

import transforms.client_transforms.ancillaries.draper_fields as df


TESTING = False
CONVERT_FNS = {
    'r': lambda x: x.replace('-', ''),
    'z': lambda x: clean_amount(x),  # pylint: disable=W0108:unnecessary-lambda
    '"': lambda x: x.replace('"', 'in'),
    '': lambda x: x.replace('&amp;', '&')
                    .replace('  ', ' ')
                    .replace('  ', ' ')
                    .rstrip()
}


def _append_account_balance(out_rec, acc_data):
    return out_rec.append(clean_amount(acc_data['bill_detail']['Due']))


def _get_billing_details(acc_rec):
    """Get individual billing items from account record."""
    billing_details = []
    for section, field, bill_type, _ in df.bill_fields:
        try:
            bill_info = CONVERT_FNS[bill_type](acc_rec[section][field])
        except KeyError:
            bill_info = 'Ooops'
        billing_details.append(bill_info)
    return billing_details


def _get_consumption_history(bill):
    """Build consumption history from XML data."""
    # get prior per usages (here to stay in scope with multi services)
    consumption_hist = None
    service = bill.find('Service')
    if service and service.attrib['Ty'] == 'Meter':
        consumption_hist = service.find('Cons_hist')

    if consumption_hist:
        return _extract_consumption(consumption_hist, bill)
    return [''] * 3, None, 1, 13


def _get_headings():
    """Create headings for output file."""
    headings = [
        (hname or hfield).upper()
        for _, hfield, _, hname
        in df.bill_fields]
    headings.extend(('Prev_read', 'Curr_read', 'Usage'))
    for idx in range(1, df.MAX_SERVICES + 1):
        headings.extend((f'Service_{str(idx)}', f'Amount_{str(idx)}'))
    headings.extend(('Acc_bal', 'Equal_Pay', 'Direct_Pay', 'Final_Bill'))
    for idx in range(1, 13):
        headings.extend((f'Use_pri{str(idx)}', f'Use_mth{str(idx)}'))
    headings.extend(f'Message{str(idx)}' for idx in range(1, df.BILL_MSGS + 1))
    headings.extend(
        f'Shutoff_msg{str(idx)}'
        for idx in range(1, df.SHUTOFF_MSGS + 1))
    headings.extend(('Equal_Pay_Title', 'Equal_Pay_Amount', 'Bill_Date'))
    if TESTING:
        headings.extend(('', '', '', 'Calc_Total', 'Diff', ''))
    return headings


def _get_service_details(service):
    """Extract title and amounts for account services."""
    service_details = []
    service_no = combined_total = 0
    for details in service.iter('ServiceDetails'):
        for detail in details.iter('ServiceDetail'):
            detail_desc = detail.find('BillCodeDescription').text
            detail_amt = str_to_amt(detail.find('Amount').text)
            if detail_desc not in df.COMBINE_SERVICES and detail_amt != 0.00:
                service_details.extend([
                    detail_desc
                    .replace('/', ' / ')
                    .title()
                    .replace(' / ', '/'),
                    amount_to_str(detail_amt)
                    ])
                service_no += 1
            else:
                combined_total += detail_amt
    return (service_no, combined_total, service_details)


def _extract_consumption(consumption_hist, bill):
    period = int(consumption_hist.attrib['Cons_prd'].split('/')[0])
    cons_hist = [
        year.attrib[month]
        for year, month
        in itertools.product(consumption_hist.iter('Year'), df.MONTHS)]

    end = len(cons_hist) - (12 - period + 1)  # extra per 12 prior mths
    start = end - 12

    # output current meter reads / useage
    curr_period = bill.find('Service').find('Serv_info').attrib
    return [
        remove_leading_zeros(curr_period['Pr_read']),
        remove_leading_zeros(curr_period['Cr_read']),
        remove_leading_zeros(curr_period['Usage'])
        ], cons_hist, start, end


def _pack_equal_pay_reserve(out_rec, acc_data):
    _ = str_to_amt(acc_data['bill_detail']['Amp_resv_total'])
    if _ != 0.00:
        out_rec.extend(['Equal Pay Reserve Amount', amount_to_str(_)])
    else:
        out_rec.extend(['']*2)


def _pack_message_lines(out_rec, acc_data):
    out_rec.extend(
        message.text.split('\n')[0]
        for message in acc_data['everyone']['msg'])
    for _ in range(1, df.BILL_MSGS-(len(acc_data['everyone']['msg'])-1)):
        out_rec.append('')


def _pack_prior_period_usages(out_rec, cons_hist, water_serv, start, end):
    if water_serv:
        for ws_idx in range(start, end):
            out_rec.extend([
                df.MONTHS[ws_idx % 12],
                remove_leading_zeros(cons_hist[ws_idx])
                ])
    else:
        for _ in range(1, end):
            out_rec.extend(['']*2)


def _pack_service_charges(bill, out_rec, acc_data):
    # output account service charges
    water_serv = False
    service_no = combined_total = 0
    for service in bill.iter('Service'):
        if service.attrib['S_des'] == 'WATER':
            water_serv = True
        num_of_services, services_total, _ = _get_service_details(service)
        out_rec.extend(_)
        service_no += num_of_services
        combined_total += services_total

    # append combined service
    if combined_total > 0:
        out_rec.extend(['Garbage/Recycle', amount_to_str(combined_total)])
        service_no += 1

    # standard charges
    for charge in df.std_charges:
        _ = str_to_amt(acc_data[charge[0]][charge[1]])
        if _ != 0.00:
            out_rec.extend([charge[2], amount_to_str(_)])
            service_no += 1

    # extract contract charges
    try:
        contract = bill.find('Contracts/Contract').attrib
        contract_amt = contract['Curr_bal']
    except AttributeError:
        contract_amt = '0'
    if contract_amt != '0':
        out_rec.extend([
            contract['Desc'].title(),
            clean_amount(contract['Curr_bal'])
            ])
        service_no += 1

    # fill in blank columns to make up max service charges
    out_rec.extend(['']*(df.MAX_SERVICES-service_no)*2)

    return water_serv


def _pack_shutoff_message(out_rec, acc_data):
    # if 'arrear' in 'Acct_Det' has non-zero value
    if str_to_amt(acc_data['acct_detail']['arrear']) > 0.00:
        out_rec.extend(
            df.shutoff_message[line]
            for line in range(df.SHUTOFF_MSGS))
    else:
        out_rec.append('')


def _set_account_details(bill):
    """Return list of account details (number, address etc)."""
    return [('account', bill.attrib),
            ('addr_info', bill.find('Address_info').attrib),
            ('bill_detail', bill.find('Bill_det').attrib),
            ('acct_detail', bill.find('Acct_det').attrib)]


def _set_account_flags(out_rec, acc_data):
    _ = clean_amount(acc_data['bill_detail']['Amp_b_net'])
    out_rec.extend([
        'Equal Pay' if _.strip() != '0.00' else '',  # neg amt not valid
        'Direct Pay' if acc_data['acct_detail']['Drf_cst'] == 'Y' else '',
        'Final Bill' if acc_data['bill_detail']['F_bill'] == 'Y' else ''
        ])


def _set_formulas(row_no):
    """Create spreadsheet formulas to test account math."""
    cols_add_formula = ['=']
    compare_totals_formula = ['=']
    cols_add_formula.extend(col + row_no + '+' for col in df.COLS_TO_ADD)
    compare_totals_formula.extend(col + row_no + '-' for col in df.TOTAL_COLS)
    return [cols_add_formula, compare_totals_formula]


def _set_global_elements(message):
    """Return dictionary of elements to be added to every account."""
    return {'msg': message,
            'pb_title': 'Previous Balance',
            'pay_title': 'Payments',
            'adj_title': 'Adjustments'}


def str_to_amt(amount):
    """Convert strings to decimal amount."""
    # if trailing sign shift minus sign for Decimal conversion
    amount = f'-{amount[:-1]}' if amount[-1] == '-' else amount
    return dec.Decimal(amount)


def amount_to_str(amount):
    """Format decimal amount as output string."""
    if TESTING:
        neg_sign = '-' if amount < 0 else ' '  # needed for balance formulii
    else:
        neg_sign = df.NEG_SIGN if amount < 0 else ' ' * len(df.NEG_SIGN)
    return f'{abs(dec.Decimal(amount)):0.2f}{neg_sign}'


def clean_amount(amount):
    """Cleanup amounts from XML file which have leading zeros."""
    return amount_to_str(str_to_amt(amount))


def remove_leading_zeros(number):
    """Remove leading zeros from non dollar value (readings, usage etc)."""
    number = f'-{number[:-1]}' if number[-1] == '-' else number
    return f'{dec.Decimal(number):0f}'


def transform_data(csv_w, source_text):
    """Transform XML file into CSV file."""
    bills = et.ElementTree(file=StringIO('\n'.join(source_text))).getroot()
    csv_w.writerow(_get_headings())
    line_no = 2 if TESTING else None  # used in formula for totals  noqa
    acc_data = {'everyone': _set_global_elements(
        bills.findall('BillComments/BillComment'))
               }

    count = 0
    for bill in bills.iterfind('Accounts/Account'):
        acc_data |= _set_account_details(bill)
        out_rec = _get_billing_details(acc_data)

        history, cons_hist, start, end = _get_consumption_history(bill)
        out_rec.extend(history)

        water_serv = _pack_service_charges(bill, out_rec, acc_data)
        _append_account_balance(out_rec, acc_data)
        _set_account_flags(out_rec, acc_data)
        _pack_prior_period_usages(out_rec, cons_hist, water_serv, start, end)
        _pack_message_lines(out_rec, acc_data)
        _pack_shutoff_message(out_rec, acc_data)
        _pack_equal_pay_reserve(out_rec, acc_data)
        out_rec.append(acc_data['bill_detail']['Bill_dt'])

        # calculated columns if testing
        if TESTING:
            out_rec.append('')
            out_rec.extend(iter(_set_formulas(str(line_no))))
            line_no += 1

        count += 1
        csv_w.writerow(out_rec)

    return count
