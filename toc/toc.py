#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of toc.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐CLASS
# │  ├──┐TOC OUTPUT
# │  │  ├── STDOUT
# │  │  └──┐INPLACE
# │  │     ├── ADD
# │  │     └── UPDATE
# │  └──┐TOC GENERATION
# │     ├── HEADER
# │     ├──┐BODY
# │     │  ├── MARKDOWN FILES
# │     │  ├── OTHER FILES
# │     │  └── PRETTIFY OUTPUT
# │     └── FOOTER
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ LIBRARIES

# regex
import re


# ################################################################ CLASS

class Toc:
    def __init__(self, file: str = "", lineNumbers: bool = False, character: str = ""):
        self.file = file
        self.extension = file.split(".")[-1]
        self.character = character
        self.lineNumbers = lineNumbers

    def set_character(self):
        # automatically select the comment type from its extension, if not already set
        match self.extension:
            case "c" | "cc" | "cpp" | "d" | "go" | "js" | "rs" | "swift" | "ts" | "typ":
                self.character = "//"
            case "ini":
                self.character = ";"
            case "bib" | "cls" | "mat" | "sty" | "tex":
                self.character = "%"
            case "hs" | "sql":
                self.character = "--"
            case _:
                self.character = "#"
        return self.character

# ################################ TOC OUTPUT
# ################ STDOUT

    def toStdout(self):
        _, outerToc = self.generate_toc()
        print(outerToc)

# ################ INPLACE

    def toFile(self):
        # run twice because updating the toc may shift everything down
        if self.lineNumbers:
            # print("using line numbers")
            n = 2
        else:
            n = 1
        for i in range(n):
            self.add_or_update_toc()

    def add_or_update_toc(self):
        # now we can generate the toc, since it's run twice when line numbers are used
        innerToc, outerToc = self.generate_toc()
        self.begin = f"{self.character} ┌───────────────────────────────────────────────────────────────┐"
        self.end   = f"{self.character} └───────────────────────────────────────────────────────────────"
        with open(self.file) as f:
            data = f.read()
            # https://stackoverflow.com/a/52921874/13448666
            if re.search(r'^%s$' % self.begin, data, re.M):
                # print("updating existing toc")
                self.update_toc(innerToc)
            else:
                # print("adding new toc")
                self.add_toc(outerToc)

    def write_newtoc(self, data):
        # common function to write output to file
        with open(self.file, "w") as f:
            f.write(data)

# ######## ADD

    def add_toc(self, outerToc):
        data = self.add_toc_after_shebang(outerToc)
        self.write_newtoc(data)

    def add_toc_after_shebang(self, outerToc):
        with open(self.file) as f:
            # if shebang is found, append after first line
            data = f.read()
            firstLine = data.split("\n", 1)[0]
            if re.search(r'^#!/usr', firstLine):
                # print("adding toc after shebang")
                firstLines = firstLine + "\n\n" + outerToc
            # else prepend as first line and put everything else after
            else:
                # print("adding toc before content")
                firstLines = outerToc + "\n\n" + firstLine
            # print(firstLines)
            data = re.sub(firstLine, firstLines, data, flags=re.DOTALL)
            return data

# ######## UPDATE

    def update_toc(self, innerToc):
        data = self.replace_multiline_multipattern(innerToc)
        self.write_newtoc(data)

    def replace_multiline_multipattern(self, innerToc):
        with open(self.file) as f:
            data = f.read()
            data = re.sub('%s(.*?)%s' % (self.begin, self.end), innerToc, data, flags=re.DOTALL)
            return data

# ################################ TOC GENERATION

    def generate_toc(self):
        # run text processors and store outputs
        tocPrefix, tocHeader = self.toc_header()
        tocBody = self.toc_body()
        tocFooter, tocSuffix = self.toc_footer()
        # exclude empty body
        innerToc = tocHeader + "\n" + tocFooter if tocBody == "" else tocHeader + "\n" + tocBody + "\n" + tocFooter
        # exclude prefix and suffix from innerToc, used for updating toc inline
        outerToc = innerToc if tocPrefix == "" else tocPrefix + "\n" + innerToc + "\n" + tocSuffix
        return innerToc, outerToc

# ################ HEADER

    def toc_header(self):
        # begin the toc with the title of the file and print a multiline comment delimiter if needed
        match self.extension:
            case "css":
                tocPrefix = "/*"
            case "html" | "md":
                tocPrefix = "<!--"
            case _:
                tocPrefix = ""
        # truncates file name to fit in a 64-characters-long box
        filename = self.file.split("/")[-1]
        file = (filename[:46] + "...") if len(filename) > 46 else filename
        tocHeader  = f"{self.character} ┌───────────────────────────────────────────────────────────────┐\n"
        tocHeader += f"{self.character} │ Contents of {file}{' ' * (50 - len(file))}│\n"
        tocHeader += f"{self.character} ├───────────────────────────────────────────────────────────────┘\n"
        tocHeader += f"{self.character} │"
        return tocPrefix, tocHeader

# ################ BODY

    def toc_body(self):
        # reads file content and processes it accordingly
        with open(self.file, "r") as f:
            lines = f.readlines()
            if self.extension == "md":
                newtoc = self.process_markdown(lines)
            else:
                newtoc = self.process_other(lines)
            tocBody = self.prettify_joints(newtoc)
            return tocBody

# ######## MARKDOWN FILES

    def process_markdown(self, lines):
        # parses markdown files, for which we reuse the headings
        oldtoc, newtoc = [], []
        if self.lineNumbers:
            oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if re.match(r'^#+ [^#│├└┌]', line)]
        else:
            oldtoc = [line for line in lines if re.match(r'^#+ [^#│├└┌]', line)]
        newtoc = [re.sub(r"^#{6}", "\t│              └──", line.strip()) for line in oldtoc]
        newtoc = [re.sub(r"^#{5}", "\t│           └──", line) for line in newtoc]
        newtoc = [re.sub(r"^#{4}", "\t│        └──", line) for line in newtoc]
        newtoc = [re.sub(r"^#{3}", "\t│     └──", line) for line in newtoc]
        newtoc = [re.sub(r"^#{2}", "\t│  └──", line) for line in newtoc]
        newtoc = [re.sub(r"^#", "\t├──", line) for line in newtoc]
        newtoc = [line.replace("\t", f"\n{self.character} ") for line in newtoc]
        return newtoc

# ######## OTHER FILES

    def process_other(self, lines):
        # parse all kind of files, for which we need our comment convention
        oldtoc, newtoc = [], []
        if self.lineNumbers:
            oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if line.startswith(self.character) and "####" in line]
        else:
            oldtoc = [line.strip() for line in lines if line.startswith(self.character) and "####" in line]
        newtoc = [re.sub(r"^" + re.escape(self.character) + " ################################################################", "\n" + self.character + " ├──", line) for line in oldtoc]
        newtoc = [re.sub(r"^" + re.escape(self.character) + " ################################", "\n" + self.character + " │  └──", line) for line in newtoc]
        newtoc = [re.sub(r"^" + re.escape(self.character) + " ################", "\n" + self.character + " │     └──", line) for line in newtoc]
        newtoc = [re.sub(r"^" + re.escape(self.character) + " ########", "\n" + self.character + " │        └──", line) for line in newtoc]
        newtoc = [re.sub(r"^" + re.escape(self.character) + " ####", "\n" + self.character + " │           └──", line) for line in newtoc]
        return newtoc

# ######## PRETTIFY OUTPUT

    def prettify_joints(self,newtoc):
        # improves toc appearance adding ┐ and │ where needed
        newtoc = "".join(newtoc)
        # split the input string into lines and reverse it
        lines = newtoc.split('\n')[::-1]
        # initialize a large list of zeros
        flags = [0] * 1000
        # iterate over the lines
        for index, line in enumerate(lines):
            # if the line contains either '└' or '├'
            if re.search("[└├]", line):
                # find the position of the match
                i = re.search("[└├]", line).start()
                # if the flag at position i is set, replace the character at position i with '├'
                if flags[i] == 1:
                    line = line[:i] + "├" + line[i + 1:]
                # set the flag at position i
                flags[i] = 1
                # Find the position of the nested children
                j = i + 3
                # if the flag at position j is set, replace the character at position j with '┐'
                if flags[j] == 1:
                    line = line[:j] + "┐" + line[j + 1:]
                # reset the flag at position j
                flags[j] = 0
                # for all positions less than i
                while i > 0:
                    i -= 1
                    # if the flag at position i is set, replace the character at position i with '│'
                    if flags[i] == 1:
                        line = line[:i] + "│" + line[i + 1:]
                # update the line in the list
                lines[index] = line
        # reverse the lines and join them into a single string with newline characters
        tocBody = '\n'.join(lines[::-1])
        # print lines that are not empty
        tocBody = '\n'.join([line for line in tocBody.split('\n') if line.strip() != ''])
        return tocBody

# ################ FOOTER

    def toc_footer(self):
        # end the toc with an horizontal line, and print multiline comment delimiter if needed
        tocFooter = f"{self.character} │\n"
        tocFooter = tocFooter + f"{self.character} └───────────────────────────────────────────────────────────────"
        match self.extension:
            case "css":
                tocSuffix = "*/"
            case "html" | "md":
                tocSuffix = "-->"
            case _:
                tocSuffix = ""
        return tocFooter, tocSuffix
