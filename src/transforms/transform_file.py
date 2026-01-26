"""
Read and modify csv files within zip file and return modified zip file.

Used by any city that has <city_name>_transform.py script.  As of May 2016:
Draper (we get two zip files, unzip, add XML suffix, zip to one to process)
Eagle Mountain
Elko
"""


import contextlib
import csv
import importlib
import os
import sys
import zipfile

from pathlib import Path

import app_modules.utilities as utils



def find_encoding(file_stream: bytes) -> str:
    """Find the encoding for the XML file"""
    declaration = str(file_stream.readline()).split("'")
    file_encoding = declaration[-2] if declaration[-3].endswith('encoding=') else 'utf8'
    file_stream.seek(0)
    return file_encoding


def remove_surplus_file(filename):
    """Remove file that is no longer needed."""
    with contextlib.suppress(OSError):
        # delete existing file (if there) to avoid duplication
        os.remove(filename)


def process_files(in_zip, out_zip, custom, file_path):
    """Process files within zipped file and write to another zip file."""
    for zipped_filename in in_zip.namelist():
        utils.logger.debug('*' * 80)
        utils.logger.info('Working on "%s"', zipped_filename)
        byte_stream = in_zip.open(zipped_filename)
        file_encoding = find_encoding (byte_stream) if zipped_filename.endswith('.xml') else 'utf8'
        source_text = byte_stream.read().decode(file_encoding).split('\r\n')
        # make sure new filename has csv extension
        zipped_result_filename = f'{Path(out_zip.filename).stem}'
        mod_filename = f'{zipped_result_filename}.csv'.lower()
        tmp_workfile_name = f'{file_path}{mod_filename}'
        fh_tmp_file = open(tmp_workfile_name, 'w', encoding=file_encoding)

        with fh_tmp_file as csv_out:
            # because Freedom Mailing output will always be a csv file
            try:
                use_csv_dict = custom.ttx
            except AttributeError:
                use_csv_dict = False
            if use_csv_dict:
                csv_w = fh_tmp_file
            else:
                csv_w = csv.writer(
                    csv_out,
                    # quoting=csv.QUOTE_ALL,
                    delimiter='\t',
                    lineterminator='\n'
                    )
            try:
                count = custom.transform_data(csv_w, source_text)
            except Exception as err:
                raise err

        out_zip.write(  # compress transformed data into new zip file
            tmp_workfile_name, mod_filename, zipfile.ZIP_DEFLATED
            )
        utils.logger.info('Converted "%s"', zipped_filename)
        if count:
            utils.logger.info('Created %s CSV data records', count)
        remove_surplus_file(tmp_workfile_name)


if __name__ == '__main__':
    CITY_NAME, FILE_NAME, FILE_TYPE, NEW_FNAME, FILE_PATH = utils.parse_user_input()
    # print(f'{CITY_NAME=}, {FILE_NAME=}, {FILE_TYPE=}, {NEW_FNAME=}, {FILE_PATH=}'); exit()

    if 'nothing using partname' in NEW_FNAME:
        utils.logger.info('%s in %s', NEW_FNAME, FILE_PATH)
        sys.exit(1)

    try:
        CUSTOM = importlib.import_module(f'{utils.TRANSFORM_MODULES}{CITY_NAME}_transform')
    except ModuleNotFoundError:
        utils.logger.info('No "%s" transform module', CITY_NAME)
        sys.exit(1)

    if FILE_TYPE != 'zip':
        # file not a zip file so compress using new filename from original filename
        ZIP_NAME = f'{FILE_PATH}{NEW_FNAME.split(".", maxsplit=1)[0]}.zip'
        with zipfile.ZipFile(ZIP_NAME, 'w') as zip_file:
            zip_file.write(f'{FILE_PATH}{FILE_NAME}', NEW_FNAME,
                compress_type=zipfile.ZIP_DEFLATED)
        utils.logger.info('Compressed %s for processing', NEW_FNAME)
    else:
        OUT_ZIP_NAME = FILE_PATH + utils.TRANS_PREFIX + NEW_FNAME
        remove_surplus_file(OUT_ZIP_NAME)  # previously converted file
        try:
            with zipfile.ZipFile(f'{FILE_PATH}{FILE_NAME}', 'r') as IN_ZIP, \
                    zipfile.ZipFile(OUT_ZIP_NAME, 'a') as OUT_ZIP:
                process_files(IN_ZIP, OUT_ZIP, CUSTOM, FILE_PATH)
            tmp = OUT_ZIP_NAME.split('/')[-1]
            utils.logger.info('Compressed results to "%s"', tmp)
        except zipfile.BadZipFile:
            utils.logger.info('"%s" is not a ZIP file', NEW_FNAME)
        except Exception as ex:  # pylint: disable=broad-except
            if type(ex).__name__ == 'SAXParseException':
                utils.logger.info('"%s" does not contain an XML file.', NEW_FNAME)
            else:
                utils.logger.info('Error processing file!', exc_info=True)
