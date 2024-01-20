#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of cli.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐FUNCTIONS
# │  ├── ARGUMENTS
# │  └── MAIN
# ├── ENTRYPOINT
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ LIBRARIES


# accept arguments
import argparse
# heredoc epilogue
from argparse import RawDescriptionHelpFormatter
# toc (installed vs dev)
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

​    # ################################################################ First level
​    # ################################ Second level
​    # ################ Third level
​    # ######## Fourth level
​    # #### Fifth level
"""
    parser = argparse.ArgumentParser(
        prog="toc",
        description="Generate a table of contents from the comments of a file",
        epilog=example_usage,
        formatter_class=RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.set_defaults(character=None)
    group.add_argument("-b", action="store_const", dest="character", const="#", help="set #  as the comment character")
    group.add_argument("-c", action="store_const", dest="character", const="//", help="set // as the comment character")
    group.add_argument("-i", action="store_const", dest="character", const=";", help="set ;  as the comment character")
    group.add_argument("-l", action="store_const", dest="character", const="%", help="set %%  as the comment character")
    group.add_argument("-s", action="store_const", dest="character", const="--", help="set -- as the comment character")
    parser.add_argument("-n", action="store_true", help="print line numbers in toc")
    parser.add_argument("-u", action="store_true", help="update or add toc in file")
    parser.add_argument("-v", action='version', version='%(prog)s {__version__}', help="Show version and exit")
    parser.add_argument("filename", help="file to analyze")
    args = parser.parse_args()
    return args

# ################################ MAIN


def main():
    # parse arguments
    args = parse_args()
    file = args.filename
    lineNumbers = args.n
    updateToc = args.u
    # initialize instance, set extension and comment character
    t = Toc(file, lineNumbers)
    t.character = args.character if args.character else t.set_character()
    # update toc in file or print it to stdout
    if updateToc:
        t.toFile()
    else:
        t.toStdout()


# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    main()
