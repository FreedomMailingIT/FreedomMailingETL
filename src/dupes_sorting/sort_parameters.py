"""
Indentify spreadsheet columns (using alphabet) used for sorting and testing.

for zip_code sorts:
first - zip+4 column
second - last line of mailing address (in effect same order as zip+4)
third - next to last line of mailing address (used if second is blank)

For alpha sorts:
first - zip+4 column
second - account name
third - next to last line of mailing address (C/O etc)

fourth column is an optioanl due date column (used to confirm correct file)
"""

ORGS = {
    'akron': ['J', 'G', 'F', 'A'],
    'afton': ['F', 'C', 'B', 'AK'],
    'af': ['G', 'H', 'L', 'A'],
    'american': ['G', 'H', 'L', 'A'],
    'ashley': ['G', 'C', 'B', 'N'],
    'baca': ['J', 'G', 'M', 'C'],
    'battlement': ['C', 'A', 'F', 'AB'],  # bmmd by another name
    'bear': ['L', 'I', 'H', 'O'],
    'blanding': ['I', 'G', 'L', 'A'],
    'bluffdale': ['G', 'I', 'L', 'A'],
    'bmmd': ['F', 'A', 'B', 'AB'],  # battlement by another name
    'bona': ['P', 'M', 'K', 'A'],  # also farr, harrisville, marriott & plain
    'burley': ['I', 'G', 'L', 'A'],
    'cedar': ['M', 'J', 'I', 'A'],
    'charlevoix': ['J', 'E', 'F', 'P'],
    'clearfield': ['CQ', 'CL', 'CN', 'G'],
    'clinton': ['L', 'I', 'H', 'A'],
    'driggs': ['T', 'Q', 'O'],
    'eagle': ['M', 'G', 'E', 'BK'],
    'eagle_mtn': ['M', 'G', 'E', 'BK'],
    'eaton': ['Q', 'M', 'L', 'E'],
    'farr': ['P', 'M', 'K', 'A'],  # also bona, harrisville, marriott & plain
    'frisco': ['L', 'G', 'I', 'C'],
    'gresham': ['H', 'E', 'D', 'K'],
    'haines': ['H', 'D', 'B'],
    'harrisville': ['P', 'M', 'K', 'A'],  # also bona, farr, marriott & plain
    'heber': ['L', 'H', 'G', 'A'],
    'hurricane': ['G', 'D', 'B', 'J'],
    'hyrum': ['I', 'E', 'F', 'A'],
    'ivins': ['G', 'C', 'B', 'M'],
    'iona': ['O', 'K', 'J', 'D'],
    'jerome': ['BX', 'BU', 'BS', 'E'],
    'johnstown': ['M', 'H', 'I', 'A'],
    'jordan': ['G', 'B', 'D', 'L'],
    'jordanelle': ['CB', 'BY', 'BX', 'G'],
    'kemmerer_diamondville': ['K', 'H', 'F', 'B'],
    'kemmerer': ['K', 'G', 'F', 'B'],
    'lehi': ['I', 'G', 'L', 'A'],  #
    'lehi_main': ['I', 'G', 'L', 'A'],  #
    'lehi_enerlyte': ['I', 'G', 'L', 'A'],  #
    'liberty': ['EE', 'EB', 'EA', 'J'],
    'marinette': ['H', 'C', 'E', 'K'],
    'marinett': ['H', 'C', 'E', 'K'],
    'marriott': ['P', 'M', 'K', 'A'],  # also bona, farr, harrisville & plain
    'oak': ['M', 'J', 'H', 'A'],
    'pagosa': ['N', 'K', 'J', 'A'],
    'parowan': ['L', 'I', 'G', 'A'],
    'payson': ['F', 'C', 'B', 'H'],
    'perry': ['G', 'E', 'K', 'ES'],
    'plain': ['P', 'M', 'K', 'A'],  # also bona, farr, harrisville & marriott
    'pleasant': ['G', 'B', 'C', 'H'],
    'pg': ['G', 'B', 'D', 'H'],
    'rawlins': ['R', 'O', 'M', 'F'],
    'stansbury': ['M', 'J', 'H', 'B'],
    'thomasville': ['K', 'I', 'N', 'A'],

    'nodate': ['?', '?', '?'],
    'last1': ['', '', '', ''],
    }
