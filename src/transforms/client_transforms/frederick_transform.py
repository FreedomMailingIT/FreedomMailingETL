"""Transform TylerTech XML for Frederick CO."""


from app_modules import csv_io
import transforms.client_transforms.tyler_tech_xml as ttx
import transforms.client_transforms.ancillaries.frederick_fields as ff


def add_global_messages(bill, source):
    """Add maximum of four BillComments from XML file to all records."""
    for idx in range(min(4, len(source.comments))):
        bill[f'message{idx + 1}'] = source.comments[idx]
    return bill


def strip_leading_zeros(name, value):
    """Strip zeros, except on account number (needed for bills & notices)."""
    return value.lstrip('0') if name in ff.currency_fields else value


def extract_notice(notice):
    """Extract late pay file data."""
    for name, value in notice.items():
        notice[name] = strip_leading_zeros(name, value)
    return notice


def build_consumption_history(bill):
    """Build consumption columns from extracted data."""
    start_per = 12 - int(bill['Cons_prd'].split('/')[0])
    for idx, usage in enumerate(bill[ttx.CONS_KEY][start_per - 36:-15]):
        bill[f'usagepri{idx}' if idx else 'currusage'] = usage
    return bill


def correct_meter_types(bill):
    """Erase meter type value if not metered service.

    (no meter_id for service).
    """
    for idx in range(1, 11):
        meter_type = f'meter{idx}'
        if bill.get(meter_type, False) and not bill.get(f'meter_id{idx}'):
            bill[meter_type] = ''
    return bill


def format_currency(bill, name, value):
    """Format extracted data into suitable currency field."""
    value = value.replace('-', 'CR').lstrip('0')
    value = ('0.00' if value == '.00'
             else (f'0{value}' if value[0] == '.' else value))
    bill[name] = value


def set_direct_pay(bill):
    """Set Direct Pay CSV column."""
    msg = ff.direct_pay['message'].replace(
        '{draft_date}', bill[ff.direct_pay['pay_date']])
    bill[ff.direct_pay['msg_col']] = msg
    return bill


def set_contract_pay(bill):
    """Set Contract Pay message (if ever needed)."""
    return bill


def unpack_list_values(bill, name, values):
    """Unpack returned list into appropriate CSV columns."""
    for idx, item in enumerate(values):
        new_key = name.replace('?', str(idx+1))
        new_key = f'curr{new_key}' if new_key == 'usage1' else new_key
        bill[new_key] = item.lstrip('0')
    return bill


def format_data(bill):
    """Format extracted XML data for output."""
    bill = (build_consumption_history(bill)
            if bill.get(ttx.CONS_KEY, False)
            else bill)
    bill = (set_direct_pay(bill)
            if ff.DIR_PAY_MSG and bill.get('directpay', False) == 'Y'
            else bill)
    bill = set_contract_pay(bill) if bill.get('contrctamt', False) else bill
    new_bill = {k: v for (k, v) in bill.items() if not k.endswith('?')}
    new_bill |= ff.bill_literals
    new_bill['baraccnum'] = new_bill['accnumber'].replace('-', '')
    for name, value in bill.items():
        if name in ff.currency_fields:
            format_currency(new_bill, name, value)
        elif isinstance(value, list):
            unpack_list_values(new_bill, name, value)
        else:
            strip_leading_zeros(name, value)
    return new_bill


def transform_data(csv_w, source_text):
    """Convert Frederick source XML into required format."""
    count = 0
    # if 'bill' in csv_w.name or 'usbx' in csv_w.name:
    if 'BillExtract' in source_text[1]:
        # bills extraction
        source = ttx.SourceXML(
            source_text, ff.bill_extract, active_only=ff.ACTIVE_ONLY,
            zero_balance=ff.ZERO_BALANCE)
        csv_out = csv_io.CSVhandler(csv_w, ff.bill_headings)
        for bill in source.traverse_xml():
            new_bill = format_data(bill)
            # correct meter types must be done after everything loaded
            new_bill = correct_meter_types(new_bill)
            new_bill = add_global_messages(new_bill, source)
            csv_out.write_record(new_bill)
            count += 1
    else:
        # late pay extractiom
        source = ttx.SourceXML(
            source_text, ff.late_pay_extract, root='Account')
        csv_out = csv_io.CSVhandler(csv_w, ff.late_pay_headings)
        for notice in source.traverse_xml():
            notice = extract_notice(notice)
            csv_out.write_record(notice)
            count += 1
    return count
