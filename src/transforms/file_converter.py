"""
OO approach to file conversion.  Object for input (of various types)
and object for output.
"""


import argparse
import importlib
import sys
from app_modules import output
import app_modules.utilities as utils


def main(fname, opts):
    """Process the file and output as specified."""
    infile, outfile = utils.get_absolute_filenames(fname)
    try:
        sfile = importlib.import_module('app_modules.' + opts.source_type).Source
    except FileNotFoundError:
        print(f'*** File type "{opts.source_type}" not valid ***')
        sys.exit()
    try:
        afile = importlib.import_module('app_modules.' + opts.action).Process
        opts.action = afile(infile, outfile)
    except ModuleNotFoundError:
        print(f'*** Action type "{opts.action}" not valid ***')
        sys.exit()

    with sfile(infile, opts.pad, opts.split) as file_in, \
            output.Output(outfile, opts.de_dup, opts.zipo, opts.comma) as file_out:
        for record in file_in:
            if opts.action:
                record = opts.action.process(record, opts.verbose)
            if record:
                file_out.write(record)
    if opts.action:
        opts.action.close()


def setup_args():
    """Handle program option input."""
    parser = argparse.ArgumentParser(
        description=f'*** File ETL for files in {utils.FILE_PATH} ***')
    # positional Arguments (listed ordinally)
    parser.add_argument(
        'source_type',
        help='Source file class (e.g. labels)')
    parser.add_argument(
        'action', nargs='?', default='no_action',
        help='Optional class that defines actions on file')
    parser.add_argument(
        'filen', nargs='?', default=None,
        help='Optional part filename to process (else uses latest)')
    parser.add_argument(
        'file_type', nargs='?', default='csv,txt',
        help='Optional file type (default is txt/csv)')
    # optional arguments (listed alphabetically)
    parser.add_argument(
        '-c', '--comma', default=False, action='store_true',
        help='Use commas as output delimiter (default is tabs)')
    parser.add_argument(
        '-d', '--dedup', default=True, action='store_false',
        help='Turn off option to remove duplicate records')
    parser.add_argument(
        '-p', '--pad', default=True, action='store_false',
        help='Turn off option to pad output columns')
    parser.add_argument(
        '-s', '--split', default=False, action='store_true',
        help='Split city/state/zip into cols')
    parser.add_argument(
        '-v', '--verbose', default=False, action='store_true',
        help='Display activity on screen')
    parser.add_argument(
        '-z', '--zipo', default=False, action='store_true',
        help='Compress output file')
    return parser


if __name__ == '__main__':
    options = setup_args()
    args = options.parse_args()

    filename = utils.get_filename(args.filen, file_type=args.file_type)
    args.zipo = True if '.zip' in filename else args.zipo
    main(filename, args)
