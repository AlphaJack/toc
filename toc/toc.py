#!/usr/bin/env python


# todo:
# fix md case array not appearing
# fix md case array white line betweeen inner toc
# https://stackoverflow.com/questions/20021693/how-to-pass-argparse-arguments-to-a-class
# rewrite readme

# ┌───────────────────────────────────────────────────────────────┐
# │ CONTENTS OF cli.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐FUNCTIONS
# │  ├── MAIN
# │  ├── HELPERS
# │  ├──┐TOC GENERATION
# │  │  ├── HEADER
# │  │  ├──┐BODY
# │  │  │  ├── MARKDOWN TYPE
# │  │  │  ├── OTHER TYPES
# │  │  │  └── PRETTIFY OUTPUT
# │  │  └── FOOTER
# │  └──┐TOC OUTPUT
# │     ├──┐INPLACE
# │     │  ├── ADD
# │     │  └── UPDATE
# │     └── STDOUT
# ├── ENTRYPOINT
# │
# └───────────────────────────────────────────────────────────────

# ################################################################ LIBRARIES


# accept arguments
import argparse
# heredoc epilogue
from argparse import RawDescriptionHelpFormatter
# regex
import re


# ################################################################ FUNCTIONS
# ################################ MAIN


def main():
    # parse arguments
    args = parse_args()
    lineNumbers = args.n
    updateToc = args.u
    file = args.filename
    extension = get_extension(file)
    c = args.character if args.character else get_character(extension)
    # update file or print to stdout
    if args.u:
        inplace_toc(file, extension, c, lineNumbers)
    else:
        stdout_toc(file, extension, c, lineNumbers)

# ################################ HELPERS


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
    group.add_argument("-b", action="store_const", dest="character", const="#",  help="set #  as the comment character")
    group.add_argument("-c", action="store_const", dest="character", const="//", help="set // as the comment character")
    group.add_argument("-i", action="store_const", dest="character", const=";",  help="set ;  as the comment character")
    group.add_argument("-l", action="store_const", dest="character", const="%",  help="set %%  as the comment character")
    group.add_argument("-s", action="store_const", dest="character", const="--", help="set -- as the comment character")
    parser.add_argument("-n", action="store_true", help="print line numbers in toc")
    parser.add_argument("-u", action="store_true", help="update or add toc in file")
    parser.add_argument("-v", action='version', version='%(prog)s {__version__}', help="Show version and exit")
    parser.add_argument("filename",  help="file to analyze")
    args = parser.parse_args()
    return args


def get_extension(file):
    # automatically select the comment type from its extension, if not already set
    extension = file.split(".")[-1]
    return extension


def get_character(extension):
    # automatically select the comment type from its extension, if not already set
    match extension:
        case ["c", "cc", "cpp", "d", "go", "js", "rs", "swift", "ts", "typ"]:
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

def generate_toc(file, extension, c, lineNumbers):
    # run text processors and store outputs
    tocPrefix, tocHeader = toc_header(file, extension, c)
    tocBody = toc_body(file, extension, c, lineNumbers)
    tocFooter, tocSuffix = toc_footer(extension, c)
    # exclude prefix and suffix from innerToc, used for updating toc inline
    innerToc = tocHeader + "\n" + tocBody + "\n" + tocFooter
    outerToc = innerToc if tocPrefix == "" else tocPrefix + "\n" + innerToc + "\n" + tocSuffix
    return innerToc, outerToc

# ################ HEADER

def toc_header(file, extension, c):
    # begin the toc with the title of the file and print a multiline comment delimiter if needed
    match extension:
        case "css":
            tocPrefix = "/*\n"
        case ["html", "md"]:
            tocPrefix = "<!--\n"
        case _:
            tocPrefix = ""
    # truncates file name to fit in a 64-characters-long box
    filename = file.split("/")[-1]
    file = (filename[:46] + "...") if len(filename) > 46 else filename
    tocHeader  = f"{c} ┌───────────────────────────────────────────────────────────────┐\n"
    tocHeader += f"{c} │ CONTENTS OF {file}{' ' * (50 - len(file))}│\n"
    tocHeader += f"{c} ├───────────────────────────────────────────────────────────────┘\n"
    tocHeader += f"{c} │"
    return tocPrefix, tocHeader

# ################ BODY

def toc_body(file, extension, c, lineNumbers):
    # reads file content and processes it accordingly
    with open(file, "r") as f:
        lines = f.readlines()
        if extension == "md":
            newtoc = process_markdown(c, lines, lineNumbers)
        else:
            newtoc = process_other(c, lines, lineNumbers)
        tocBody = prettify_joints(newtoc)
        return tocBody

# ######## MARKDOWN FILES

def process_markdown(c, lines, lineNumbers):
    # parses markdown files, for which we reuse the headings
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
    newtoc = [line.replace("\t", f"\n{c} ") for line in newtoc]
    return newtoc

# ######## OTHER FILES

def process_other(c, lines, lineNumbers):
    # parse all kind of files, for which we need our comment convention
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

# ######## PRETTIFY OUTPUT

def prettify_joints(newtoc):
    # improves toc appearance adding ┐ and │ where needed
    newtoc = "".join(newtoc)
    # split the input string into lines and reverse it
    lines = newtoc.split('\n')[::-1]
    # initialize a large list of zeros
    flags = [0] * 1000
    # iterate over the lines
    for index, line in enumerate(lines):
        # if the line contains either '└' or '├'
        if re.search('[└├]', line):
            # find the position of the match
            i = re.search('[└├]', line).start()
            # if the flag at position i is set, replace the character at position i with '├'
            if flags[i] == 1:
                line = line[:i] + '├' + line[i+1:]
            # set the flag at position i
            flags[i] = 1
            # Find the position of the nested children
            j = i + 3
            # if the flag at position j is set, replace the character at position j with '┐'
            if flags[j] == 1:
                line = line[:j] + '┐' + line[j+1:]
            # reset the flag at position j
            flags[j] = 0
            # for all positions less than i
            while i > 0:
                i -= 1
                # if the flag at position i is set, replace the character at position i with '│'
                if flags[i] == 1:
                    line = line[:i] + '│' + line[i+1:]
            # update the line in the list
            lines[index] = line
    # reverse the lines and join them into a single string with newline characters
    tocBody = '\n'.join(lines[::-1])
    # print lines that are not empty
    tocBody = '\n'.join([line for line in tocBody.split('\n') if line.strip() != ''])
    return tocBody

# ################ FOOTER


def toc_footer(extension, c):
    # end the toc with an horizontal line, and print multiline comment delimiter if needed
    tocFooter = f"{c} │\n"
    tocFooter = tocFooter + f"{c} └───────────────────────────────────────────────────────────────"
    match extension:
        case "css":
            tocSuffix = + "\n*/"
        case ["html", "md"]:
            tocSuffix = + "\n-->"
        case _:
            tocSuffix = ""
    return tocFooter, tocSuffix


# ################################ TOC OUTPUT
# ################ INPLACE


def inplace_toc(file, extension, c, lineNumbers):
    if lineNumbers:
        # run twice because updating the toc may shift everything down
        print("using line numbers")
        for i in range(2):
            add_or_update_toc(file, extension, c, lineNumbers,)
    else:
        add_or_update_toc(file, extension, c, lineNumbers)

def add_or_update_toc(file, extension, c, lineNumbers):
    # now we can generate the toc, since it's run twice when line numbers are used
    innerToc, outerToc = generate_toc(file, extension, c, lineNumbers)
    with open(file) as f:
        data = f.read()
        begin = f"{c} ┌───────────────────────────────────────────────────────────────┐"
        end   = f"{c} └───────────────────────────────────────────────────────────────"
        # https://stackoverflow.com/a/52921874/13448666
        if re.search(r'^%s$' % begin, data, re.M):
            print("updating existing toc")
            update_toc(file, extension, c, lineNumbers, innerToc, begin, end)
        else:
            print("adding new toc")
            add_toc(file, extension, c, lineNumbers, outerToc)

def write_newtoc(file, data):
    # common function to write output to file
    with open(file, "w") as f:
        f.write(data)

# ######## ADD


def add_toc(file, extension, c, lineNumbers, outerToc):
    data = add_toc_after_shebang(outerToc)
    write_newtoc(file, data)


def add_toc_after_shebang(file, outerToc):
    with open(file) as f:
        # if shebang is found, append after first line
        data = f.read()
        firstLine = data.split("\n", 1)[0]
        if re.search(r'^#!/usr', firstLine):
            print("adding toc after shebang")
            firstLines = firstLine + "\n\n" + outerToc
        # else prepend as first line and put everything else after
        else:
            print("adding toc before content")
            firstLines = outerToc + "\n\n" + firstLine
        # print(firstLines)
        data = re.sub(firstLine, firstLines, data, flags=re.DOTALL)
        return data

# ######## UPDATE


def update_toc(file, extension, c, lineNumbers, innerToc, begin, end):
    data = replace_multiline_multipattern(file, innerToc, begin, end)
    write_newtoc(file, data)


def replace_multiline_multipattern(file, innerToc, begin, end):
    with open(file) as f:
        data = f.read()
        data = re.sub('%s(.*?)%s' % (begin, end), innerToc, data, flags=re.DOTALL)
        return data

# ################ STDOUT


def stdout_toc(file, extension, c, lineNumbers):
    _, outerToc = generate_toc(file, extension, c, lineNumbers)
    print(outerToc)


# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    main()
