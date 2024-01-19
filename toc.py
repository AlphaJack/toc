#!/usr/bin/env python


# ┌───────────────────────────────────────────────────────────────┐
# │ CONTENTS OF toc.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├── VARIABLES
# ├──┐ARGUMENTS
# │  └── ARGUMENTS
# ├──┐FUNCTIONS
# │  ├── MAIN
# │  ├── HELPERS
# │  └── TOC GENERATION
# ├── EXECUTION
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ LIBRARIES


# accept arguments
import argparse
# heredoc epilogue
from argparse import RawDescriptionHelpFormatter
# path of files
# import os
# regex
import re


# ################################################################ VARIABLES

prog = "toc"
version = "2.0.0"
extension = ""
file = ""
example_usage = """
example comments:

​    # ################################################################ First level
​    # ################################ Second level
​    # ################ Third level
​    # ######## Fourth level
​    # #### Fifth level
"""


# ################################################################ ARGUMENTS
# ################################ ARGUMENTS


# read user-provided comment type
parser = argparse.ArgumentParser(
                prog = prog,
                description = "Generate a table of contents from the comments of a file",
                epilog = example_usage,
                formatter_class = RawDescriptionHelpFormatter)
parser.add_argument("-b", action="store_const", const="#",  help = "set #  as the comment character")
parser.add_argument("-c", action="store_const", const="//", help = "set // as the comment character")
parser.add_argument("-i", action="store_const", const=";",  help = "set ;  as the comment character")
parser.add_argument("-l", action="store_const", const="%",  help = "set %%  as the comment character")
parser.add_argument("-s", action="store_const", const="--", help = "set -- as the comment character")
parser.add_argument("-n", action="store_true", help = "srint line numbers in toc")
parser.add_argument("-r", action="store_true", help = "replace or add toc in file")
parser.add_argument("-v", action="version", version=f"{prog} {version}", help = "Show version and exit")
parser.add_argument("filename",  help = "file to analyze")
args = parser.parse_args()
c = args.b or args.c or args.i or args.l or args.s or None
lineNumbers = args.n
replaceToc = args.r
file = args.filename


# ################################################################ FUNCTIONS
# ################################ MAIN


def main():
    extension = check_extension(file)
    c = check_comment(file, extension)
    toc_header(file, extension, c)
    toc_body(file, extension, c)
    toc_footer(extension, c)


# ################################ HELPERS


def check_extension(file):
    # automatically select the comment type from its extension, if not already set
    extension = file.split(".")[-1]
    return extension


def check_comment(file, extension):
    # automatically select the comment type from its extension, if not already set
    global c
    if c is None:
        match extension:
            case ["c", "cc", "cpp", "d", "go", "js", "rs", "swift", "typ"]:
                c = "//"
            case "ini":
                c = ";"
            case ["bib", "cls", "mat", "sty", "tex"]:
                c = "%"
            case ["hs", "sql"]:
                c = "--"
            case _:
                c = "#"
    return c

# ################################ TOC GENERATION


def toc_header(file, extension, c):
    # print multiline comment if needed
    match extension:
        case "css":
            print("/*")
        case ["html", "md"]:
            print("<!--")
        case _:
            pass

    # truncates file name to fit in a 64-characters-long box
    filename = file.split("/")[-1]
    file = (filename[:46] + "...") if len(filename) > 46 else filename

    # draw box
    print(f"{c} ┌───────────────────────────────────────────────────────────────┐")
    print(f"{c} │ CONTENTS OF {file}{' ' * (50 - len(file))}│")
    print(f"{c} ├───────────────────────────────────────────────────────────────┘")
    print(f"{c} │")


def toc_body(file, extension, c):
    with open(file, "r") as f:
        lines = f.readlines()
        if extension == "md":
            newtoc = process_markdown(lines)
        else:
            newtoc = process_other(lines)
        newtoc = "".join(newtoc)
        #print(newtoc)
        lines = newtoc.split("\n")
        print(newtoc)
        #lines.reverse()
        #flags = [0] * len(max(lines, key=len))
        #for i, line in enumerate(lines):
        #    if "└" in line or "├" in line:
        #        idx = line.index("└") if "└" in line else line.index("├")
        #        if flags[idx]:
        #            lines[i] = lines[i][:idx] + "├" + lines[i][idx+1:]
        #        flags[idx] = 1
        #        idx += 3
        #        if flags[idx]:
        #            lines[i] = lines[i][:idx] + "┐" + lines[i][idx+1:]
        #        flags[idx] = 0
        #        for j in range(idx):
        #            if flags[j]:
        #                lines[i] = lines[i][:j] + "│" + lines[i][j+1:]
        #lines.reverse()
        #newtoc = "\n".join(line for line in lines if line.strip())
        return newtoc


def process_markdown(lines, oldtoc=None, newtoc=None):
    oldtoc, newtoc = [], []
    if lineNumbers:
        oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if re.match(r'^#+ [^#│├└┌]', line)]
    else:
        oldtoc = [line for line in lines if re.match(r'^#+ [^#│├└┌]', line)]
    newtoc = [re.sub(r"^#{6}", "\t│              └──", line.strip()) for line in oldtoc]                        
    newtoc = [re.sub(r"^#{5}", "\t│           └──", line) for line in newtoc]
    newtoc = [re.sub(r"^#{4}", "\t│        └──", line) for line in newtoc]
    newtoc = [re.sub(r"^#{3}", "\t│     └──", line) for line in newtoc]
    newtoc = [re.sub(r"^#{2}", "\t│  └──", line) for line in newtoc]
    newtoc = [re.sub(r"^#", "\t├──", line) for line in newtoc]
    newtoc = [line.replace("\t", "\n# ") for line in newtoc]
    return newtoc


def process_other(lines, oldtoc=None, newtoc=None):
    oldtoc, newtoc = [], []
    if lineNumbers:
        oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if line.startswith(c) and "####" in line]
    else:
        oldtoc = [line.strip() for line in lines if line.startswith(c) and "####" in line]
    newtoc = [re.sub(r"^" + re.escape(c) + " ################################################################", "\n" + c + " ├──", line) for line in oldtoc]
    newtoc = [re.sub(r"^" + re.escape(c) + " ################################", "\n" + c + " │  └──", line) for line in newtoc]
    newtoc = [re.sub(r"^" + re.escape(c) + " ################", "\n" + c + " │     └──", line) for line in newtoc]
    newtoc = [re.sub(r"^" + re.escape(c) + " ########", "\n" + c + " │        └──", line) for line in newtoc]
    newtoc = [re.sub(r"^" + re.escape(c) + " ####", "\n" + c + " │           └──", line) for line in newtoc]
    return newtoc


def toc_footer(extension, c):
    # end the toc with an horizontal line
    print(f"{c} │")
    print(f"{c} └───────────────────────────────────────────────────────────────")

    # print multiline comment if needed
    match extension:
        case "css":
            print("*/")
        case ["html", "md"]:
            print("-->")
        case _:
            pass


# ################################################################ EXECUTION


if __name__ == "__main__":
    main()
