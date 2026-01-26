"""Find file extension at end of __doc__ string."""

import re

EXAMPLES = (
    'input is csv and output to <filename>.json.',
    'input is json and output to <filename>.json.',
    'output to <filename>.json.',
    'output to <filename>.json',
    'output to csv.',
    'input is from csv file and output is to sql',
    'output to json file',
)
PATTERN = r"(json|csv|sql)[.\s\.]*"


def test_extraction(examples=EXAMPLES, pattern=PATTERN):
    """..."""
    for example in examples:
        extracted = re.findall(pattern, example)[-1]
        print(f'{example} -> {extracted}')
        # assert example.endswith((f'{extracted}.'))
