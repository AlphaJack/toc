#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of cli.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── MODULES
# ├──┐FUNCTIONS
# │  ├── ARGUMENTS
# │  ├── PROCESS FILE
# │  └── MAIN
# ├── ENTRY POINT
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ MODULES


# accept arguments
import argparse
__version__ = "2.2.0"

# heredoc in help epilog
from argparse import RawDescriptionHelpFormatter

# stderr
import sys

# glob expansion
import glob

# toc (dist vs dev)
try:
    from toc.toc import Toc
except ImportError:
    from toc import Toc


# ################################################################ FUNCTIONS
# ################################ ARGUMENTS


def parse_args():
    # read user-provided comment type
    character = "#"
    example_usage = f"""
example comments:

{character} ################################################################ First level
{character} ################################ Second level
{character} ################ Third level
{character} ######## Fourth level
{character} #### Fifth level
"""
    parser = argparse.ArgumentParser(
        prog="toc",
        description="Generate a table of contents from the comments of a file",
        epilog=example_usage,
        formatter_class=RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("files", nargs="*", help="files or lists of files to process")
    parser.add_argument("-c", action="store", dest="character", type=str, help="set an arbitrary comment character (e.g. //)")
    parser.add_argument("-f", "--to-file", action="store_true", help="add or update toc in the original file")
    group.add_argument("-l", "--from-list", action="store_true", help="consider positional arguments as lists of files")
    parser.add_argument("-n", "--line-numbers", action="store_true", help="print line numbers in toc")
    group.add_argument("-o", action="store", dest="output_file", type=str, help="print output to an arbitrary file")
    parser.add_argument("-v", "--version", action='version', version="%(prog)s " + __version__, help="show the current version and exit")
    args = parser.parse_args()
    return args


def get_files(args):
    # consider all files as lists
    if args.from_list:
        files = []
        for fileList in args.files:
            try:
                with open(fileList, "r") as list_content:
                    for line in list_content.read().splitlines():
                        if not line.startswith("#"):
                            # glob expansion
                            files += [globMatch for globMatch in glob.glob(line, recursive=True)]
            # cannot open that list
            except BaseException:
                print(f'Skipping list "{fileList}"', file=sys.stderr)
    # only consider the first file
    elif args.output_file:
        files = [args.files[0]]
    # consider all files
    else:
        files = args.files
    return files

# ################################ PROCESS FILE


def process_file(file, args):
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

# ################################ MAIN


def main():
    # parse arguments
    args = parse_args()
    files = get_files(args)
    # process all files individually
    for file in files:
        process_file(file, args)
    if not files:
        print("No files provided", file=sys.stderr)


# ################################################################ ENTRY POINT

if __name__ == "__main__":
    main()
