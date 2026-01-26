"""
Created on 2014-09-23 23:16:23 US MT.

@author: gregory
"""


MONTHS = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
MAX_SERVICES = 10
BILL_MSGS = 1
SHUTOFF_MSGS = 1
NEG_SIGN = 'CR'
COMBINE_SERVICES = ('GARBAGE/RECYCLE', '300 GAL GARBAGE')
COLS_TO_ADD = [  # columns labels to be used in formula for calculated total
    'O', 'Q', 'S', 'X', 'Z', 'AB', 'AD', 'AF', 'AH', 'AJ', 'AL', 'AN', 'AP',
    ]
TOTAL_COLS = ['AQ', 'BY']


home_dir = '/home/gregory/Data/freedommailing/draper/201503/'
data_source = 'USBXMLF-0103312015'

bill_fields = [
    # tuple elements are section, field, type, heading (if blank use field)
    ('account', 'No', 'r', 'Bar_acc_no'),
    ('bill_detail', 'S_to_dt', '', ''),
    ('bill_detail', 'Due_dt', '', ''),
    ('account', 'No', '', 'Acc_no'),
    ('account', 'Name', '"', ''),
    ('addr_info', 'B_attn', '', 'Attention'),
    ('addr_info', 'B_a1', '', 'Addr_line1'),
    ('addr_info', 'B_a2', '', 'Addr_line2'),
    ('addr_info', 'B_city', '', 'City'),
    ('addr_info', 'B_st', '', 'State'),
    ('addr_info', 'B_zip', '', 'Zip'),
    ('addr_info', 'Ssa', '', 'Service_address'),
    ('bill_detail', 'S_fr_dt', '', ''),
    ('everyone', 'pb_title', '', ''),
    ('acct_detail', 'L_b_amt', 'z', 'pb_amt'),
    ('everyone', 'pay_title', '', ''),
    ('acct_detail', 'T_pmts', 'z', ''),
    ('everyone', 'adj_title', '', ''),
    ('acct_detail', 'T_adjs', 'z', ''),
    ]

std_charges = [
    # ('bill_detail', 'Tax', 'Franchise Tax'),
    ('acct_detail', 'T_pens', 'Late Fee'),
    ('bill_detail', 'Amp_amt', 'Change to Equal Pay Reserve'),
    ]

shutoff_message = [
    'Your utility account with Draper City is past due.  '
    'If payment is not received in full your service may be terminated.'
]
