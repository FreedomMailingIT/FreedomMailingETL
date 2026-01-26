"""Central point for specifying file locations."""


import json
import os
from pathlib import Path


PROJECT = Path.cwd().name
src_dir = PROJECT == 'src'

ROOT = Path.cwd().parent.parent if src_dir else Path.cwd().parent
ROOT = ROOT.as_posix().replace('C:', '')  # + '/'
DATA_DIR = 'FreedomMailingData'

# print(f'{PROJECT=}, {ROOT=}, {DATA_DIR=}')

with open(f'{'.' if src_dir else 'src'}/app_modules/file_loctn.json', 'r', encoding='utf8') as locs:
    PATHS = json.load(locs)
    for key, val in PATHS.items():
        if key[0] != '_':
            PATHS[key] = PATHS[key]\
                        .replace('{ROOT}', ROOT)\
                        .replace('{PROJECT}', PROJECT)\
                        .replace('{DATA_DIR}', DATA_DIR)


GET = os.environ.get
IDX = (
    GET('FM_FILES', None) or
    GET('USERNAME', None) or
    GET('USER', None) or
    os.name
    )

#Centralize where to find data
FILE_PATH = PATHS.get(IDX, PATHS['default'])
TEST_DATA = PATHS['tests']
DATA_ROOT = PATHS['data_root']
PRODUCTION_DATA = PATHS['production_data']
ORIGINAL_DATA = PATHS['original_data']
ARCHIVE_PATH = PATHS['archive']
LOG_FILE = '.job_execution.log'


if __name__ == '__main__':
    print(f'{FILE_PATH=}\n{TEST_DATA=}\n{PRODUCTION_DATA=}\n{ORIGINAL_DATA=}')
