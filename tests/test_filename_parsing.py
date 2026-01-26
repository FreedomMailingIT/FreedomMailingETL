"""Test filename_parsing function in utilities."""


import app_modules.utilities as utils


DATA = 'tests/data/'  # utils.FILE_PATH


tests = [
    (
        'Effingham Delinquent.xml (2).txt', 'txt',
        'effingham', 'Effingham Delinquent_xml (2).txt',
        DATA
    ),
    (
        'Effingham Delinquent.xml.(2).txt', 'txt',
        'effingham', 'Effingham Delinquent_xml_(2).txt',
        DATA
    ),
    (
        'Effingham Delinquent.xml.txt', 'txt',
        'effingham', 'Effingham Delinquent_xml.txt',
        DATA
    ),
    (
        'lake_point 2025.07.01.csv', 'csv',
        'lake_point', 'lake_point 2025_07_01.csv',
        DATA
    ),
    ]


def test_filename_parsing_0(fname=tests[0][0]):
    """Test filenames are parsed correctly."""
    cname, fname, ftype, fnew, fpath = utils.parse_filename_new(fname)
    assert (fname, ftype, cname, fnew, fpath)[:-1] == tests[0][:-1]


def test_filename_parsing_1(fname=tests[1][0]):
    """Test filenames are parsed correctly."""
    cname, fname, ftype, fnew, fpath = utils.parse_filename_new(fname)
    assert (fname, ftype, cname, fnew, fpath)[:-1] == tests[1][:-1]


def test_filename_parsing_2(fname=tests[2][0]):
    """Test filenames are parsed correctly."""
    cname, fname, ftype, fnew, fpath = utils.parse_filename_new(fname)
    assert (fname, ftype, cname, fnew, fpath)[:-1] == tests[2][:-1]


def test_filename_parsing_3(fname=tests[3][0]):
    """Test filenames are parsed correctly."""
    cname, fname, ftype, fnew, fpath = utils.parse_filename_new(fname)
    assert (fname, ftype, cname, fnew, fpath)[:-1] == tests[3][:-1]


if __name__ == '__main__':
    test_filename_parsing_0()
