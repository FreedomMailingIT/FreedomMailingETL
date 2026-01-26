"""
Produce index of PDF bill file.

Extracts account & page numbers from PDF file into file with name structure:
B47001_02_201702_47001.spdfi (company_billcycle_yearmonth_company).

Switched to PyMuPDF (import as fitz) because os independent Python package
that is ~20 faster that PyPDF4.
"""

import os
import sys
from pathlib import Path

import pymupdf as pdf_reader
import hlap_sftp_host as c
from pdf_bill_indexing.hlap_idx_check import check_idx_file
import app_modules.utilities as utils


def create_index(new_abs_fn_prefix):
    """
    Create index.

    With account number, start and end page number on each line.
    """
    tmp_file = f'{new_abs_fn_prefix}.tmp'
    spdfi_file = f'{new_abs_fn_prefix}.spdfi'
    pdf_file = f'{new_abs_fn_prefix}.pdf'
    utils.logger.info('Scaning %s.', pdf_file.rsplit('/', maxsplit=1)[-1])

    with open(tmp_file, 'w', encoding='utf8') as idxf:
        pdf_doc = pdf_reader.open(pdf_file)
        out_line = '{0:0>10},{sp},{ep}\n'
        page_no = align_no = first_acc = 0
        for page_no, page in enumerate(pdf_doc):
            text = page.get_text()
            if 'ALIGNMENT' in text:
                # bump page count for alignment test page & skip outlup
                align_no += 1
            else:
                # output index info to file
                lines = text.split('\n')
                idx_no = page_no + 1 + align_no
                acc_no = lines[8]
                first_acc = first_acc or acc_no
                idxf.write(out_line.format(acc_no, sp=idx_no, ep=idx_no))
        page_no = page_no + 1
    if Path(spdfi_file).exists():
        utils.logger.info('Found %s exists; removing', spdfi_file)
        os.remove(spdfi_file)
    os.rename(tmp_file, spdfi_file)
    checkout_idx(spdfi_file, page_no, first_acc, acc_no)


def checkout_idx(spdfi_file, page_no, first_acc, acc_no):
    """Verify index file makes sense and report results."""
    results = check_idx_file(spdfi_file, first_acc, acc_no, page_no)
    checkout = all(results.values())
    if checkout:
        msg = 'correctly.'
    else:
        probs = {key: value for key, value in results.items() if not value}
        msg = f'with problems {probs}'
    utils.logger.info('%s bills indexed %s', page_no, msg)


def put_files_to_sftp(fn_prefix):
    """Copy required files to SFTP server."""
    cmd = f"sshpass -p {c.pswd} scp {fn_prefix}* {c.user}@{c.host}:~"
    err = os.system(cmd)
    if err:
        utils.logger.info('Problems coping B47001* files to SFTP server.')
    else:
        utils.logger.info('Copied B47001* files to SFTP server.', )


def main(input_fp, input_fn=None):
    """
    Extract account & page numbers.

    Read though PDF text file and extracts account & page numbers which are
    output to index file as single line CSV. Account number must be 10 digits
    with leading zeros, both beginning and ending page numbers
    (always the same) also output
    eg 0123456789,10,10
    """
    file_path = input_fp
    filename = utils.compose_hlap_filename()
    new_abs_fn_prefix = f'{file_path}{filename}'
    if input_fn != filename:
        old_fn = f'{file_path}{input_fn}'
        new_fn = f'{new_abs_fn_prefix}.pdf'
        msg = [
            'Renaming', '"'+old_fn.rsplit('/', maxsplit=1)[-1]+'"',
            'to', '"'+new_fn.rsplit('/', maxsplit=1)[-1]+'"'
            ]
        utils.logger.info(' '.join(msg))
        if Path(new_fn).exists():
            utils.logger.info('Found %s exists; removing', new_fn)
            os.remove(new_fn)
        os.rename(old_fn, new_fn)
    create_index(new_abs_fn_prefix)
    if 'test' not in input_fp:
        # no FTP if testing
        put_files_to_sftp(new_abs_fn_prefix)
    utils.logger.info('Process completed.')


if __name__ == '__main__':
    CITY_NAME, FILE_NAME, FILE_TYPE, NEW_FNAME, FILE_PATH = utils.parse_user_input()
    # must have source filename, fsmonitor usually supplies this
    if FILE_NAME:
        main(FILE_PATH, NEW_FNAME)
        # put_files_to_sftp(FILE_NAME)
    else:
        sys.exit(1)
