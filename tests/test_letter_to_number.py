"""Test letter_to_number function in utilities."""


from app_modules.utilities import convert_col_letter_to_number as convert


def test_single_letter_convert():
    """Test convert_col_letter_to_number with single letter column labels."""
    values = {'A': 0, 'B': 1, 'C': 2, 'X': 23, 'Y': 24, 'Z': 25}
    for letter, value in values.items():
        assert convert(letter) == value


def test_double_letter_convert():
    """Test convert_col_letter_to_number with two letter column labels."""
    values = {'AA': 26, 'AB': 27, 'AC': 28, 'AX': 49, 'AY': 50, 'AZ': 51}
    for letter, value in values.items():
        assert convert(letter) == value


def test_second_rack_double_letter_convert():
    """Test function with two letter column labels starting with CA."""
    values = {'CA': 78, 'CB': 79, 'CC': 80, 'CX': 101, 'CY': 102, 'CZ': 103}
    for letter, value in values.items():
        assert convert(letter) == value


def test_tripple_letter_convert():
    """Test convert_col_letter_to_number with three letter column labels."""
    values = {'AAA': 702, 'AAB': 703, 'AAC': 704,
              'AAX': 725, 'AAY': 726, 'AAZ': 727}
    for letter, value in values.items():
        assert convert(letter) == value
