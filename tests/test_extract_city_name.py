"""Test determiniing filename parts (city name, file type etc)."""


import pathlib
import pytest
import app_modules.utilities as utils


data = [
    ('rawlins', (
        'rawlins dupes 0728.csv',
        '.csv',
        '.csv',
        'rawlins dupes 0728',
        'rawlins dupes 0728.csv',
        )),
    ('effingham', (
        'Effingham Delinquent 0722.xml.(2).txt',
        '.txt',
        '.xml',
        'Effingham Delinquent 0722',
        )),
    ('frederick', (
        'USBXMLF-0107292022.zip',
        '.zip',
        '.zip',
        'USBXMLF-0107292022',
        )),
    ('draper', (
        'draper xml',
        '',
        '',
        'draper xml',
        )),
    ('eagle_mtn', (
        'eagle',
        '',
        '',
        'eagle',
        )),
    ('lehi', (
        'lehi.txt',
        '.txt',
        '.txt',
        'lehi',
        )),
]


@pytest.mark.parametrize('cname, parts', data)
def test_filename_parse(cname, parts):  # pylint: disable=redefined-outer-name
    """Breakdown filename to it's parts."""
    fparts = pathlib.PurePath(parts[0])
    first = fparts.suffixes[0] if fparts.suffixes else ''
    city = utils.xtract_city_name(fparts.stem)
    assert fparts.name == parts[0]  # filename
    assert fparts.suffix == parts[1]  # last suffix
    assert first == parts[2]  # first suffix
    assert fparts.stem.split('.')[0] == parts[3]  # new fname
    assert utils.TRANSLATE.get(city, city) == cname
