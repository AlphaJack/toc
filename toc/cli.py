#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of cli.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐FUNCTIONS
# │  ├── ARGUMENTS
# │  └── MAIN
# ├── ENTRY POINT
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ LIBRARIES


# accept arguments
import argparse
__version__ = "2.1.0"

# heredoc in help epilog
from argparse import RawDescriptionHelpFormatter

# toc (dist vs dev)
try:
    from toc.toc import Toc
except ImportError:
    from toc import Toc


# ################################################################ FUNCTIONS
# ################################ ARGUMENTS


def parse_args():
    # read user-provided comment type
    example_usage = """
example comments:

# ################################################################ First level
# ################################ Second level
# ################ Third level
# ######## Fourth level
# #### Fifth level
"""
    parser = argparse.ArgumentParser(
        prog="toc",
        description="Generate a table of contents from the comments of a file",
        epilog=example_usage,
        formatter_class=RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("files", nargs="*", help="files to process")
    parser.add_argument("-c", action="store", dest="character", type=str, help="set an arbitrary comment character (e.g. //)")
    parser.add_argument("-f", "--to-file", action="store_true", help="add or update toc in file")
    group.add_argument("-l", "--from-list", action="store_true", help="process a list of files")
    parser.add_argument("-n", "--line-numbers", action="store_true", help="print line numbers in toc")
    group.add_argument("-o", action="store", dest="output_file", type=str, help="print output to another file")
    parser.add_argument("-v", "--version", action='version', version="%(prog)s " + __version__, help="Show version and exit")
    args = parser.parse_args()
    return args

# ################################ MAIN


def main():
    # parse arguments
    args = parse_args()
    if args.from_list:
        files = []
        for list in args.files:
            with open(list, "r") as list_content:
                files += list_content.read().splitlines()
    else:
        files = args.files
    for file in files:
        # initialize instance
        t = Toc(file)
        # set comment character and line numbers
        t.character = args.character if args.character else t.set_character()
        t.lineNumbers = args.line_numbers if args.line_numbers else False
        t.output = args.output_file if args.output_file else None
        # print output
        if args.to_file or args.output_file:
            t.to_file()
        else:
            t.to_stdout()


# ################################################################ ENTRY POINT

if __name__ == "__main__":
    main()
