#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on 2013-05-04 18:46:23 US MT

@author: gregory
"""


bill_fields = [
    ('AccountNumber', ''),
    ('CustomerNumber', ''),
    ('CustomerName', ''),
    ('MailAddressLineOne', ''),
    ('MailAddressLineTwo', ''),
    ('MailCity', ''),
    ('MailvsState', ''),
    ('MailZip', ''),
    ('ServiceAddress', ''),
    ('ServiceFromDate', ''),
    ('ServiceToDate', ''),
    ('BillingDate', ''),
    ('BalanceDue', 'c'),
    ('PenaltyActivity', 'c'),
    ('PaymentActivity', 'c'),
    ('AdjustmentActivity', 'c'),
    ('CurrentCharges', 'c'),
    ('BalanceDue', 'c'),
    ('DueAfterAmount', 'c'),
    ('BankDraftDate', ''),
    ('BalanceAtBilling', 'c'),
]
# for column headings before bill fields
prefix_cols = [
    ('Due Date', ''),
    ]

# for column headings after bill fields
postfix_cols = [
    ('Billing Message', ''),
    ('Stub Message', ''),
    ]

# column headings for charges columns (there are six sets of charges fields)
charges_cols = [
    ('Service', ''),
    ('Amount', ''),
    ]

# column headings for meter columns (there are 20 sets of meter fields)
meter_cols = [
    ('Meter Size', ''),
    ('Meter Type', ''),
    ('Prev Read', ''),
    ('Curr Read', ''),
    ('Cons.', ''),
    ]
