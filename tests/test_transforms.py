"""Test transform programs.

Should test all transforms because they are all unique.

"""


import os
import pytest
import app_modules.utilities as utils
import app_modules.file_locations as loctns

# Prepare for testing
TEST_DATA = f'{loctns.TEST_DATA}transform_data/'
utils.initialize_log_file(path=utils.FILE_PATH)  # FILE_PATH needed because utilities uses it
transforms = [
    'Charlevoix csv_EOR.zip',
    'Charlevoix tsv_EOR.zip',
    'Charlevoix fixed_length.zip',
    'draper non water.zip',
    'draper water.zip',
    'eagle_mtn.zip',
    'effingham bills.zip',
    'effingham delinquents.zip',
    'elko.zip',
    'frederick water.zip',
    'frederick non water.zip',
    'frederick shutoffs.zip',
    'lake_point.zip',
    'roosevelt.zip',
    'waterford.zip',
    ]

@pytest.mark.parametrize('fname', transforms)
def test_transform(fname, subtests):
    """Test transform."""
    with subtests.test(msg=f'{fname} failed to execute!'):
        assert os.system(f'py src/transforms/transform_file.py -f "{fname}" -p "{TEST_DATA}') == 0

    seg_len, lines = utils.trim_log_seg(utils.get_last_log_segment())

    with subtests.test(msg=f'{fname} not converted!'):
        assert seg_len == 4 and 'Converted ' in lines[1]

    with subtests.test(msg=f'{fname} failed to create CSV file!'):
        assert seg_len == 4 and 'Created ' in lines[2]

    with subtests.test(msg=f'{fname} has empty conversion file!'):
        assert seg_len == 4 and int(lines[2].split()[1]) > 0

    with subtests.test(msg=f'{fname} results not compressed!'):
        assert 'Compressed results to "fxd' in lines[-1]


def test_cleanup():
    """Archive results to keep test TEST_DATA directory clean."""
    if old_files := [x for x in os.listdir(TEST_DATA) if x.startswith('fxd ')]:
        utils.logger.debug('*' * 80)
        utils.logger.debug('Files to be archived: %s', old_files)
        utils.archive_files(
            files=old_files,
            path_to_archive=utils.FILE_PATH,
            path_to_files=TEST_DATA,
            arch_name='transformed_files')


if __name__ == '__main__':
    os.system(f'py src/transforms/transform_file.py -f "{TEST_DATA}waterford.zip"')
    test_cleanup()
