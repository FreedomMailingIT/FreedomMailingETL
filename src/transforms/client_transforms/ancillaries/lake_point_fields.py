"""Field locations for Lake Point."""


HEADER = {
    'ID': 'Y',  # sometimes not true
    'NAME': 'L',
    'MAIL ADDRESS': 'N',
    'CITY': 'O',
    'STATE': 'P',
    'ZIP': 'Q',
    'SERV_ADDR': 'S',
}

BODY = {
    'TRANS_DATE_{}': 'A',
    'TRANS_DESC_{}': 'B',
    'TRANS_PERD_{}': 'C',
    'TRANS_CHRG_{}': 'D',
}

FOOTER = {
    '30_DAYS': 'B',
    '60_DAYS': 'D',
    '90_DAYS': 'F',
    'OVER_90': 'H',
    'BALANCE': 'J',
}
