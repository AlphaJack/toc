#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of toc.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── MODULES
# ├──┐CLASS
# │  ├──┐PUBLIC METHODS
# │  │  ├── COMMENT CHARACTER
# │  │  └──┐TOC OUTPUT
# │  │     ├── STDOUT
# │  │     └── FILE
# │  └──┐INTERNAL METHODS
# │     ├──┐TOC OUTPUT
# │     │  └──┐FILE
# │     │     ├── ADD
# │     │     └── UPDATE
# │     └──┐TOC GENERATION
# │        ├── HEADER
# │        ├──┐BODY
# │        │  ├── BEANCOUNT AND MARKDOWN
# │        │  ├── PERL
# │        │  ├── OTHERS
# │        │  └── PRETTIFY CONNECTORS
# │        └── FOOTER
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ MODULES

# regex
import re
# stderr
import sys


# ################################################################ CLASS

class Toc:
    def __init__(self, input: str = "", output=None, lineNumbers: bool = False, character: str = "#"):
        self.input = str(input)
        self.output = output
        self.extension = self.input.split(".")[-1].lower() if "." in self.input else ""
        self.lineNumbers = lineNumbers
        self.character = character
        self.err = None
        self.updated = False
        self.innerTocBegin = None
        self.innerTocTitle = None
        self.innerTocEnd = None
        self.levels = {
            64: 1,
            32: 2,
            16: 3,
            8: 4,
            4: 5,
            2: 6
        }

# ################################ PUBLIC METHODS

# ################ COMMENT CHARACTER

    def set_character(self):
        # automatically select the comment type from its extension, if not already set
        match self.extension:
            case "c" | "carbon" | "cc" | "coffee" | "cpp" | "cs" | "css" | "d" | "dart" | "go" | "h" | "hpp" | "htm" | "html" | "hxx" | "java" | "js" | "kt" | "md" | "pas" | "php" | "pp" | "proto" | "qmd" | "qs" | "rs" | "scala" | "sc" | "swift" | "ts" | "typ" | "xml" | "zig":
                self.character = "//"
            case "ahk" | "asm" | "beancount" | "cl" | "clj" | "cljs" | "cljc" | "edn" | "fasl" | "ini" | "lisp" | "lsp" | "rkt" | "scm" | "ss":
                self.character = ";"
            case "bib" | "cls" | "erl" | "hrl" | "mat" | "sty" | "tex":
                self.character = "%"
            case "adb" | "ads" | "elm" | "hs" | "lua" | "sql":
                self.character = "--"
            # https://www.gnu.org/software/groff/manual/, https://manpages.bsd.lv/mdoc.html
            case "1" | "1m" | "2" | "3" | "4" | "5" | "6" | "7" | "8":
                self.character = '.\\"'
            case "ml" | "mli":
                self.character = "*"
            case "vb" | "vba" | "vbs":
                self.character = "'"
            case "apl":
                self.character = "⍝"
            # https://www.gavilan.edu/csis/languages/comments.html#_Toc53710123
            case "bas" | "bat" | "cmd" | "com" | "sbl":
                self.character = "REM"
            # https://stackoverflow.com/a/17665688
            case "cbl" | "cob":
                self.character = "      *>"
            case "f" | "for":
                self.character = "C"
            # https://github.com/textmate/fortran.tmbundle/issues/10#issuecomment-22660333
            case "f90" | "f95" | "f03" | "f08" | "f15" | "f18":
                self.character = "!"
            # jl mojo pl pm ps1 py r rb sh, yml, and anything else
            case _:
                self.character = "#"
        return self.character

# ################ TOC OUTPUT
# ######## STDOUT

    def to_stdout(self):
        _, _outerToc = self._generate_toc()
        if _outerToc == "":
            # skip error if we already set self.err
            print(f'Skipping empty "{self.character}" toc for "{self.input}"', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            print(_outerToc)

# ######## FILE

    def to_file(self, output=None):
        # if file has been specified, print there instead of the original file (useful for testing)
        if self.output is None:
            self.output = output if output else self.input
        # run twice because updating the toc may shift everything down
        n = 2 if self.lineNumbers else 1
        for i in range(n):
            self._add_or_update()

# ################################ INTERNAL METHODS
# ################ TOC OUTPUT
# ######## FILE

    def _add_or_update(self):
        # if the file does not contain a toc, add it, otherwise update it
        _innerToc, _outerToc = self._generate_toc()
        if _outerToc == "":
            print(f'Skipping empty "{self.character}" toc for "{self.input}"', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            with open(self.input) as f:
                _data = f.read()
                # re.MULTILINE: https://docs.python.org/3/library/re.html#re.M
                if re.search(r"^%s\n%s" % (self.innerTocBegin, self.innerTocTitle), _data, re.MULTILINE) and re.search(r"^%s$" % self.innerTocEnd, _data, re.MULTILINE):
                    self._update_toc(_innerToc)
                else:
                    self._add_toc(_outerToc)

    def _write_toc(self, data):
        # common function to rewrite file
        if data:
            try:
                with open(self.output, "w") as f:
                    f.write(data)
            except PermissionError:
                print(f'Skipping write-protected file "{self.output}"', file=sys.stderr)
                self.err = "write"
        elif not self.updated:
            # data should never be empty if self.updated = False, but in case least we prevented cleaning the file
            print(f'Skipping purging file "{self.output}"', file=sys.stderr)
            self.updated = True
        # elif self.updated: we skipped replacing the same toc

# #### ADD

    def _add_toc(self, outerToc):
        # check for begin-of-file directives and write output
        _data = self._check_directives(outerToc)
        self._write_toc(_data)
        print(f'Adding toc to file "{self.output}"', file=sys.stderr)
        self.updated = True

    def _check_directives(self, outerToc):
        # if a frontmatter, shebang or directive is found, append after first line(s)
        with open(self.input) as f:
            _data = f.read()
            _firstLine = _data.splitlines()[0]
            if _firstLine == "":
                # if _firstLine was be empty, re.sub would destroy the original file by inserting an outerToc between every character
                _data = outerToc + "\n" + _data
            else:
                match self.extension:
                    case "md":
                        # multi line yaml, toml, js frontmatter for markdown
                        if re.search(r"^---", _firstLine):
                            _frontmatter = re.search(r"^---\n.*?\n---", _data, re.DOTALL).group(0)
                        elif re.search(r"^\+\+\+", _firstLine):
                            _frontmatter = re.search(r"^\+\+\+\n.*?\n\+\+\+", _data, re.DOTALL).group(0)
                        elif re.search(r"^\{", _firstLine):
                            _frontmatter = re.search(r"^\{\n.*?\n\}", _data, re.DOTALL).group(0)
                        else:
                            _frontmatter = None
                        _firstLine = _frontmatter if _frontmatter else _firstLine
                        _firstFewLines = _firstLine + "\n\n" + outerToc if _frontmatter else outerToc + "\n\n" + _firstLine
                        # print(_frontmatter)
                        # print(_firstFewLines)
                    case _:
                        # single line shebang, xml, html, vim, emacs, perl pod
                        if (re.search(r"^#!", _firstLine)
                            or re.search(r"<\?xml", _firstLine, re.IGNORECASE)
                            or re.search(r"<!doctype", _firstLine, re.IGNORECASE)
                            or re.search(r"^" + re.escape(self.character) + r"\s+([Vv]im?|ex):", _firstLine)
                            or re.search(r"^" + re.escape(self.character) + r"\s*-\*-", _firstLine)
                            or re.search(r"^" + re.escape(self.character) + r"^=pod$", _firstLine)):
                            # print("adding toc after shebang")
                            _firstFewLines = _firstLine + "\n\n" + outerToc
                        # else prepend as first line and put everything else after
                        else:
                            # print("adding toc before content")
                            _firstFewLines = outerToc + "\n\n" + _firstLine
                _data = re.sub(re.escape(_firstLine), _firstFewLines, _data, count=1)
            return _data

# #### UPDATE

    def _update_toc(self, innerToc):
        # replace existing toc and write output
        _data = self._replace_existing_toc(innerToc)
        self._write_toc(_data)
        if not self.updated:
            print(f'Updating toc in file "{self.output}"', file=sys.stderr)
            self.updated = True

    def _replace_existing_toc(self, innerToc):
        # replace over multiple lines between two patterns
        with open(self.input) as f:
            _data = f.read()
            # if the new toc is already present in the file, it makes no sense to rewrite the file
            # re.escape to treat dots and other characters literally
            if re.search(re.escape(innerToc), _data, re.MULTILINE):
                self.err = "same"
                _data = None
                if not self.updated or self.output != self.input:
                    print(f'Skipping replacing same toc in file "{self.output}"', file=sys.stderr)
                    self.updated = True
            else:
                # use non-greedy regex to only replace the smalles portion of text between innerTocBegin and innerTocEnd
                # use count to only replace the first valid region in file
                _data = re.sub(r"%s\n%s(.*?)%s" % (self.innerTocBegin, self.innerTocTitle, self.innerTocEnd), innerToc, _data, count=1, flags=re.DOTALL)
            return _data

# ################ TOC GENERATION

    def _generate_toc(self):
        # run text processors and store outputs
        _tocPrefix, _tocHeader = self._toc_header()
        _tocBody = self._toc_body()
        _tocFooter, _tocSuffix = self._toc_footer()
        # exclude empty body
        if not _tocBody:
            return "", ""
        _innerToc = "\n".join([_tocHeader, _tocBody, _tocFooter])
        # exclude prefix and suffix from innerToc, used for updating toc inline
        _outerToc = _innerToc if not _tocPrefix else "\n".join([_tocPrefix, _innerToc, _tocSuffix])
        return _innerToc, _outerToc

# ######## HEADER

    def _toc_header(self):
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocPrefix = "/*"
            case "html" | "xml" | "md" | "qmd" | "rmd":
                _tocPrefix = "<!--"
            case "ml" | "mli" | "scpd" | "scpt":
                _tocPrefix = "(*"
            case "pl" | "pm" | "pod":
                _tocPrefix = "=encoding utf8\n=begin comment"
            case _:
                _tocPrefix = ""
        # begin the toc with the file name, truncating it if necessary
        _filename = self.input.split("/")[-1]
        _truncated_filename = (_filename[:46] + "...") if len(_filename) > 46 else _filename
        _padding = ' ' * (50 - len(_truncated_filename))
        self.innerTocBegin = f"{self.character} ┌───────────────────────────────────────────────────────────────┐"
        self.innerTocTitle = f"{self.character} │ Contents of {_truncated_filename}{_padding}│"
        # building the toc header
        _tocHeaderLines = [
            self.innerTocBegin,
            self.innerTocTitle,
            f"{self.character} ├───────────────────────────────────────────────────────────────┘",
            f"{self.character} │"
        ]
        _tocHeader = "\n".join(_tocHeaderLines)
        # innerTocEnd not used here, but generated anyway as it used in re.search
        self.innerTocEnd = f"{self.character} └───────────────────────────────────────────────────────────────"
        return _tocPrefix, _tocHeader

# ######## BODY

    def _toc_body(self):
        # read file content and process it accordingly
        # display alert for common errors
        _tocBody = ""
        try:
            with open(self.input, "r") as f:
                _lines = f.readlines()
                match self.extension:
                    case "beancount":
                        _newtoc = self._process_increasing(_lines, "*")
                    case "md":
                        _newtoc = self._process_increasing(_lines, "#")
                    case "pl" | "pm" | "pod":
                        _newtoc = self._process_perl(_lines)
                    case _:
                        _newtoc = self._process_other(_lines)
                _tocBody = self._prettify_connectors(_newtoc)
        except FileNotFoundError:
            print(f'Skipping non-existing file "{self.input}"', file=sys.stderr)
            _tocBody = ""
            self.err = "notfound"
        except PermissionError:
            print(f'Skipping read-protected file "{self.input}"', file=sys.stderr)
            _tocBody = ""
            self.err = "read"
        except IsADirectoryError:
            print(f'Skipping directory "{self.input}"', file=sys.stderr)
            _tocBody = ""
            self.err = "directory"
        except UnicodeDecodeError:
            print(f'Skipping binary file "{self.input}"', file=sys.stderr)
            _tocBody = ""
            self.err = "binary"
        #except BaseException:
        #    print(f'Skipping file "{self.input}"', file=sys.stderr)
        #    _tocBody = ""
        #    self.err = "unknown"
        finally:
            return _tocBody

# #### BEANCOUNT AND MARKDOWN

    def _process_increasing(self, lines, heading):
        # parse markdown and beancount files, reusing headings or sections
        _newtoc = []
        # ignore comments for other languages
        _pattern = re.compile(r"^(" + re.escape(heading) + "+) (?!#)(.*)$")
        # print(_pattern)

        def replace_heading(match):
            _heading_level = len(match.group(1))
            _heading_text = f"{match.group(2)} {n+1}" if self.lineNumbers else match.group(2)
            # 3 spaces per heading level
            _indentation = "   " * (_heading_level - 2)
            if _heading_level == 1:
                _replacement = "\n" + self.character + " ├── " + _heading_text
            else:
                _replacement = "\n" + self.character + " │  " + _indentation + "└── " + _heading_text
            return _replacement

        for n, line in enumerate(lines):
            if _pattern.match(line):
                # strip line and replace comment with indentation
                _newtoc.append(_pattern.sub(replace_heading, line.strip()))
                # print(_newtoc)
        return _newtoc

# #### PERL

    # https://perldoc.perl.org/perlpod
    def _process_perl(self, lines):
        # parse perl files, reusing headings
        _newtoc = []
        # difference compared to markdown
        _pattern = re.compile(r"^=head(\d) (.*)$")

        def replace_heading_perl(match):
            # difference compared to markdown
            _heading_level = int(match.group(1))
            _heading_text = f"{match.group(2)} {n+1}" if self.lineNumbers else match.group(2)
            # 3 spaces per heading level
            _indentation = "   " * (_heading_level - 2)
            if _heading_level == 1:
                _replacement = "\n" + self.character + " ├── " + _heading_text
            else:
                _replacement = "\n" + self.character + " │  " + _indentation + "└── " + _heading_text
            return _replacement

        for n, line in enumerate(lines):
            if _pattern.match(line):
                _newtoc.append(_pattern.sub(replace_heading_perl, line.strip()))
        # print(_newtoc)
        return _newtoc

# #### OTHERS

    def _process_other(self, lines):
        _newtoc = []
        # define regex pattern once, using groups to capture the count of '#'
        _pattern = re.compile(rf"^{re.escape(self.character)} (#{{64}}|#{{32}}|#{{16}}|#{{8}}|#{{4}}|#{{2}}) (.*)$")
        # print(_pattern)
        # define a function to replace patterns with a new TOC line structure

        def replace_heading_other(match):
            _heading_level = self.levels[len(match.group(1))]
            _heading_text = f"{match.group(2)} {n+1}" if self.lineNumbers else match.group(2)
            # 3 spaces per heading level
            _indentation = "   " * (_heading_level - 2)
            # print(_heading_level)
            # print(_heading_text)
            if _heading_level == 1:
                _replacement = "\n" + self.character + " ├── " + _heading_text
            else:
                _replacement = "\n" + self.character + " │  " + _indentation + "└── " + _heading_text
            return _replacement

        # cobol not being recognized
        #match self.extension:
        #    case "cbl" | "cob":
        #        _oldtoc = [re.sub(r"^\*>", self.character, line) for line in _oldtoc]
        for n, line in enumerate(lines):
            if _pattern.match(line):
                # print(line)
                # special pre-processing for cobol
                # match self.extension:
                #    case "cbl" | "cob":
                #        _newtoc.append(_pattern.sub(replace_heading_other, line))
                #    case _:
                #        _newtoc.append(_pattern.sub(replace_heading_other, line.strip()))
                _newtoc.append(_pattern.sub(replace_heading_other, line.strip()))

        # special post-processing for r
        match self.extension:
            case "r" | "rpres":
                _newtoc = [re.sub(r" [#-=]{4,}", "", line) for line in _newtoc]
        return _newtoc

# #### PRETTIFY CONNECTORS

    def _prettify_connectors(self, newtoc):
        # improves nested appearance adding ┐ and │ where needed
        _newtoc = "".join(newtoc)
        # split the input string into lines and reverse it
        _lines = _newtoc.split('\n')[::-1]
        # use a dictionary for flags instead of a list
        _flags = {}
        # iterate over the lines
        for index, line in enumerate(_lines):
            # perform the regex search once and store the result
            match = re.search("[└├]", line)
            # if the line contains either '└' or '├'
            if match:
                # find the position of the match
                i = match.start()
                # if the flag at position i is set, replace the character at position i with '├'
                if _flags.get(i, 0) == 1:
                    line = line[:i] + "├" + line[i + 1:]
                # set the flag at position i
                _flags[i] = 1
                # Find the position of the nested children
                j = i + 3
                # if the flag at position j is set, replace the character at position j with '┐'
                if _flags.get(j, 0) == 1:
                    line = line[:j] + "┐" + line[j + 1:]
                # reset the flag at position j
            _flags[j] = 0
            # for all positions less than i
            for k in range(i - 1, -1, -1):
                # if the flag at position k is set, replace the character at position k with '│'
                if _flags.get(k, 0) == 1:
                    line = line[:k] + "│" + line[k + 1:]
            # update the line in the list
            _lines[index] = line
        # reverse the lines and join them into a single string with newline characters
        _tocBody = '\n'.join(line for line in _lines[::-1] if line.strip() != '')
        return _tocBody

# ######## FOOTER

    def _toc_footer(self):
        # end the toc with an horizontal line
        self.innerTocEnd = f"{self.character} └───────────────────────────────────────────────────────────────"
        _tocFooterLines = [
            f"{self.character} │",
            self.innerTocEnd,
        ]
        _tocFooter = "\n".join(_tocFooterLines)
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocSuffix = "*/"
            case "html" | "xml" | "md" | "qmd" | "rmd":
                _tocSuffix = "-->"
            case "ml" | "mli" | "scpd" | "scpt":
                _tocSuffix = "*)"
            case "pl" | "pm" | "pod":
                _tocSuffix = "=end comment"
            case _:
                _tocSuffix = ""
        return _tocFooter, _tocSuffix
