"""Convert city XML billing files into CSV bill and delinquent files.

Program decides which conversion function to use based upon XML root element.

Uses ElementTree xpath technique for cleaner code (compared to dict calls).
"""


import xml.etree.ElementTree as et  # noqa (camelcase)
from decimal import Decimal
from io import StringIO

import transforms.client_transforms.ancillaries.effingham_fields as ef


MAX_SERVS = 8


#################################################################
# Common functions used by both bill and delinquent record builds
#################################################################

def format_amount(amount):
    """Format amount to include thousands separator."""
    return f'{Decimal(amount):,}'


def format_date(tdt):
    """Format 8 digit date string to mm/dd/yyyy."""
    return '/'.join([tdt[:2], tdt[2:4], tdt[4:]])


#################################################################
# Functions used to build bill record
#################################################################

def account_details(record, totals, name_addr, out_rec):
    """Output account details."""
    etext = record.findtext
    out_rec.extend([
        etext('ACCT_NO'),
        etext('ACCT_NO'),
        etext('CUST_NO'),
        '',  # mail route
        ])
    out_rec.extend(name_addr)
    # remaining fields appended because python choked on another extend
    out_rec.append(etext('LOC_FMT'))
    out_rec.append(format_date(etext('BILL_DATE')))
    out_rec.append(format_date(etext('DUE_DATE')))
    out_rec.append(etext('TYP_LNG'))
    out_rec.append('F' if totals.findtext('T_RUN') == 'F' else '')
    out_rec.append('')  # equal pay (no longer used)


def account_meters(bill, out_rec):
    """Output details on upto two meters."""
    charges = bill.findall('CHARGE_DETAIL')
    for count, charge in enumerate(charges):  # bill.iterfind('CHARGE_DETAIL'):
        if count >= 2:  # 2 is max number of meters
            break
        ctext = charge.findtext
        meter = charge.find('METER_DETAIL')
        if meter:
            mtext = meter.findtext
            out_rec.extend([
                mtext('MTR_NO'),
                format_date(ctext('PREV_READ_DATE')),
                mtext('PREV_READ'),
                format_date(ctext('CURR_READ_DATE')),
                mtext('CURR_READ'),
                format_amount(mtext('CURR_ACT_USG')),
                ctext('SERV_LNGDESC'),
                ctext('USAGE_DAYS'),
                mtext('CNV_FACT'),
                '',  # meter comment
                ])
        else:  # no meter record
            out_rec.extend([''] * 10)

    if len(charges) == 1:  # only one charge, so pad second
        out_rec.extend([''] * 10)


def account_service_charges(bill, out_rec):
    """Output up to eight service details."""
    serv_count = 0
    for charge in bill.iterfind('CHARGE_DETAIL'):
        etext = charge.findtext
        try:
            out_rec.append(
                format_amount(etext('METER_DETAIL/CURR_ACT_USG')))
        except TypeError:
            out_rec.append('')  # non metered service so no usage
        out_rec.append(format_amount(etext('SERV_CHARGE')))
        out_rec.append(etext('SERV_LNGDESC'))
        serv_count += 1
    # pad unused service columns
    for _ in range(serv_count, MAX_SERVS):
        out_rec.extend([''] * 3)


def account_summary(xml_bill, out_rec):
    """Output Account summary."""
    etext = xml_bill.findtext
    out_rec.extend([
        format_amount(etext('CURR_CHARGES')),
        format_amount(etext('BALANCE_FWD')),
        format_amount(etext('PMTS_SINCE_LAST')),
        format_amount(etext('ADJ_SINCE_LAST')),
        format_amount(etext('PEN_ON_PASTDUE')),
        format_amount(etext('AMT_PAST_DUE')),
        format_amount(etext('TOTDUE_INCL_NOTDUE')),
        format_amount(etext('TOTDUE_PLUSNOTDUE_W_PENBOTH')),
        '',  # direct pay (not longer used)
        etext('BILL_MSG1'),
        etext('BILL_MSG2'),
        etext('BILL_MSG3'),
        etext('BILL_MSG4'),
        etext('SPEC_MSG2'),  # there is no SPEC_MSG1
        etext('SPEC_MSG3'),
        etext('SPEC_MSG4'),
        '',  # pad last message
        format_date(etext('CTL_START')),
        format_date(etext('CTL_END')),
        etext('EFT_COMM'),
        etext('RECURCC_MSG'),
        ])


def build_bill_record(record, totals, name_addr):
    """Build bill record from XML fields."""
    out_rec = []
    hdr = record.find('HEADER')
    account_details(hdr, totals, name_addr, out_rec)
    account_meters(record, out_rec)
    account_service_charges(record, out_rec)
    account_summary(hdr, out_rec)
    return out_rec


def build_name_addr(record):
    """Build name & address from XML fields."""
    name_addr = []
    etext = record.findtext
    if ',' in etext('CUST_NAME1'):
        _ = etext('CUST_NAME1').split(',')
        name_addr.append(f'{_[1].strip()} {_[0].strip()}')
    else:
        name_addr.append(etext('CUST_NAME1'))
    # set city & state field names for bills or delinquents
    city = 'CUST_CTY' if record.tag == 'HEADER' else 'CUST_CITY'
    state = 'CUST_ST' if record.tag == 'HEADER' else 'CUST_STATE'
    name_addr.extend([
        etext('CUST_ADDR1'), etext('CUST_ADDR2'),
        etext(city), etext(state), etext('CUST_ZIP'),
        ])
    return name_addr


#################################################################
# Functions used to build delinquent record
#################################################################

def build_delq_record(record, name_addr):
    """Build delinquent record from XML fields."""
    # print(record)
    # notice = record.find('DELINQUENT_NOTICE')
    etext = record.findtext
    out_rec = [
        format_date(etext('NOTICE_DATE')),
        etext('ACCOUNT_NUMBER'),
        etext('CUSTOMER_NUMBER'),
        format_amount(etext('ALL_TOTAL_DUE')),
        format_date(etext('SHUTOFF_DATE')),
        etext('LOC_FMT'),
        ]
    out_rec.extend(name_addr)
    out_rec.extend([
        etext('MESSAGE_LINE1'),
        etext('BILL_NAME1'),
        ])
    return out_rec


#################################################################
# Function used to process XML input file
#################################################################

def transform_data(csv_w, source_text):
    """Transform XML file into CSV file."""
    count = 0
    try:
        eff_accts = et.ElementTree(
            file=StringIO('\n'.join(source_text))).getroot()
        bills = eff_accts.tag == 'MUNIS_BILL_PRINT_EXPORT'
        csv_w.writerow(ef.BILL_HEADINGS if bills else ef.DELQ_HEADINGS)

        # cycle through XML billing records
        records = (
            eff_accts.iterfind('BILL')
            if bills else
            eff_accts.iterfind('DELINQUENT_NOTICE')
            )
        for record in records:
            hdr = record.find('HEADER') if bills else record
            etext = hdr.findtext
            email = etext('DELIVERY_METHOD') == 'E' and etext('DELIVERY_INFO')
            if not email:
                count += 1
                if bills:
                    csv_w.writerow(
                        build_bill_record(
                            record,
                            record.find('TOTALS_AR_CAT'),
                            build_name_addr(record.find('HEADER')),)
                    )
                else:  # delinquent notice
                    csv_w.writerow(
                        build_delq_record(record, build_name_addr(record)))
    except Exception as err:
        raise err

    return count
