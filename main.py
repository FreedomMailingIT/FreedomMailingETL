"""
Main entry point at project top level to change to source directory
and call dispatcher.py with optional single argument of a file name.


See dispatcher.py comments for explanation of the option.
"""



import os
import sys
from typing import List



def main(args: List[str]):
    os.chdir('./src')
    if args:
        os.system(f'py dispatcher.py {args[0]} "{args[1]}"')
    else:
        os.system('py dispatcher.py')



if __name__ == "__main__":
    main(sys.argv[1:])
