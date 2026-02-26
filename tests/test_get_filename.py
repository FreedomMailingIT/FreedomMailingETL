"""Test get_filename function in utilities."""


import app_modules.utilities as utils


TEST_DATA = 'tests/data/'  # loctns.TEST_DATA

def test_find_all_files():
    """Find all files."""
    files_found = utils.find_all_files(
        part_name='nodate test',
        file_type='csv',
        file_path=f'{TEST_DATA}multiples_data/'
        )
    assert files_found


def test_get_filename_name_and_type():
    """Test to make function finds right file."""
    fn = utils.get_filename(
        part_name='effingham delinquents',
        file_type='zip',
        file_path=f'{TEST_DATA}transform_data/'
        )
    assert fn == 'effingham delinquents.zip'


def test_get_filename_partial_name_only():
    """Test to make function finds right file."""
    fn = utils.get_filename(
        part_name='eagle',
        file_type=None,
        file_path=f'{TEST_DATA}transform_data/'
        )
    assert fn == 'eagle_mtn.zip'


def test_get_filename_type_only():
    """Test to make function finds the most recent file."""
    fn = utils.get_filename(
        file_type='zip',
        file_path=f'{TEST_DATA}transform_data/'
        )
    assert fn == 'discovery_bay.zip'


def test_get_filename_not_exist():
    """Test to make function finds right file."""
    fn = utils.get_filename(
        part_name='non_existing',
        file_type='txt',
        file_path=f'{TEST_DATA}multiples_data/'
        )
    assert fn.startswith('nothing using')


if __name__ == '__main__':
    test_get_filename_partial_name_only()
