#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of toc.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── MODULES
# ├──┐CLASSES
# │  ├──┐PUBLIC METHODS
# │  │  ├── COMMENT CHARACTER
# │  │  └──┐TOC OUTPUT
# │  │     ├── STDOUT
# │  │     └──┐FILE
# │  └──┐INTERNAL METHODS
# │     ├── TOC OUTPUT
# │     │     ├── ADD
# │     │     └── UPDATE
# │     ├──┐TOC GENERATION
# │     │  ├── PREFIX AND SUFFIX
# │     │  ├── HEADER
# │     │  ├── FOOTER
# │     │  └──┐BODY
# │     │     ├── ASCIIDOC, BEANCOUNT AND MARKDOWN
# │     │     ├── HTML
# │     │     ├── RESTRUCTUREDTEXT
# │     │     ├── MAN PAGES
# │     │     ├── PERL
# │     │     ├── GENERIC
# │     │     └── PRETTIFY CONNECTORS
# │     └── TOC INPUT
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ MODULES

# regex
import re

# stderr
import sys

# files
from pathlib import Path


# ################################################################ CLASSES


class Toc:
    def __init__(self, inputFile: Path):
        print(f"inputFile: {inputFile}", file=sys.stderr)
        self.inputFile: Path = inputFile
        self.outputFile: Path | None = None
        self.extension: str = self.inputFile.suffix.lower().replace(".", "")
        self.lineNumbers: bool = False
        self.updated: bool = False
        self.character: str = "#"
        self.depth: int = 0
        self.err: str | None = None
        self.innerTocBegin: str | None = None
        self.innerTocTitle: str | None = None
        self.innerTocEnd: str | None = None
        # n=2**(7−l), l=7−math.log(n,2)
        self.levels: dict[int, int] = {64: 1, 32: 2, 16: 3, 8: 4, 4: 5, 2: 6}

    # ################################ PUBLIC METHODS

    # ################ COMMENT CHARACTER

    def set_character(self) -> str:
        # automatically select the comment type from its extension, if not already set
        match self.extension:
            case "ad" | "adoc" | "asc" | "asciidoc" | "c" | "carbon" | "cc" | "coffee" | "cpp" | "cs" | "css" | "cu" | "d" | "dart" | "go" | "h" | "hpp" | "htm" | "html" | "hxx" | "java" | "js" | "jsx" | "kt" | "md" | "mdx" | "qmd" | "rmd" | "pas" | "php" | "pp" | "proto" | "qs" | "rs" | "scala" | "sc" | "swift" | "ts" | "typ" | "xml" | "zig":
                self.character = "//"
            case "ahk" | "asm" | "beancount" | "cl" | "clj" | "cljs" | "cljc" | "edn" | "fasl" | "ini" | "lisp" | "lsp" | "rkt" | "scm" | "ss":
                self.character = ";"
            case "bib" | "cls" | "erl" | "hrl" | "mat" | "sty" | "tex":
                self.character = "%"
            case "adb" | "ads" | "elm" | "hs" | "lua" | "sql":
                self.character = "--"
            # https://www.gnu.org/software/groff/manual/, https://manpages.bsd.lv/mdoc.html
            case "1" | "1m" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "n":
                self.character = '.\\"'
            case "apl":
                self.character = "⍝"
            # https://www.gavilan.edu/csis/languages/comments.html#_Toc53710123
            case "bas" | "bat" | "cmd" | "com" | "sbl":
                self.character = "REM"
            # https://stackoverflow.com/a/17665688
            case "cbl" | "cob":
                self.character = "      *>"
            # https://github.com/textmate/fortran.tmbundle/issues/10#issuecomment-22660333
            case "f90" | "f95" | "f03" | "f08" | "f15" | "f18":
                self.character = "!"
            case "f" | "for":
                self.character = "C"
            case "j":
                self.character = "NB."
            case "mmd" | "mermaid":
                self.character = "%%"
            case "ml" | "mli":
                self.character = "*"
            case "rst":
                self.character = ".."
            case "vb" | "vba" | "vbs":
                self.character = "'"
            # jl mojo pl pm ps1 py r rb sh, yml, and anything else
            case _:
                self.character = "#"
        return self.character

    # ################ TOC OUTPUT
    # ######## STDOUT

    def to_stdout(self) -> None:
        _, _outerToc = self._generate_toc()
        if _outerToc == "":
            # skip error if we already set self.err
            print(
                f'Could not generate a "{self.character}" toc from "{self.inputFile}"',
                file=sys.stderr,
            ) if self.err is None else None
            self.err = "empty"
        else:
            print(_outerToc)

    # ######## FILE

    def to_file(self, output: Path | None = None) -> None:
        # if file has been specified, print there instead of the original file (useful for testing)
        if self.outputFile is None:
            self.outputFile = output if output else self.inputFile
        if self.inputFile == Path("-"):
            print(
                "Cannot write to stdin", file=sys.stderr
            ) if self.err is None else None
            self.err = "stdin"
        else:
            # run twice because updating the toc with self.lineNumbers == True may shift everything down
            n = 2 if self.lineNumbers else 1
            for _ in range(n):
                self._add_or_update()

    # ################################ INTERNAL METHODS
    # ################ TOC OUTPUT

    def _add_or_update(self) -> None:
        _innerToc, _outerToc = self._generate_toc()
        # do not write an empty file
        if _outerToc == "":
            print(
                f'Could not generate a "{self.character}" toc from "{self.inputFile}"',
                file=sys.stderr,
            ) if self.err is None else None
            self.err = "empty"
        else:
            # if the file does not contain a toc, add it, otherwise update it
            # re.MULTILINE: https://docs.python.org/3/library/re.html#re.M
            # match also file name, results in a second toc if file is renamed
            #self.pattern = re.compile(
            #    rf"{self.innerTocBegin}\n{self.innerTocTitle}(.*?){self.innerTocEnd}",
            #    re.DOTALL,
            #)
            # does not match file name, replacing toc even if file gets renamed
            self.pattern = re.compile(
                rf"{self.innerTocBegin}\n{self.character} │ Contents of (.*?){self.innerTocEnd}",
                re.DOTALL,
            )
            # print(self.pattern)
            _data = self._read_file()
            # print(_data)
            if re.search(self.pattern, _data):
                self._update_toc(_innerToc)
            else:
                self._add_toc(_outerToc)

    def _write_toc(self, data: str) -> None:
        # common function to rewrite file
        if data and self.outputFile is not None:
            try:
                with open(self.outputFile, "w") as f:
                    f.write(data)
            except PermissionError:
                print(
                    f'Skipping write-protected "{self.outputFile}"', file=sys.stderr
                ) if self.err is None else None
                self.err = "write"
                self.updated = True
            except BaseException:
                print(
                    f'Unknown error while writing "{self.outputFile}"', file=sys.stderr
                ) if self.err is None else None
                self.err = "unknownw"
                self.updated = True
        elif not self.updated:
            # data should never be empty if self.updated = False, but in case least we prevented cleaning the file
            print(f'Skipping writing "{self.outputFile}"', file=sys.stderr)
            self.updated = True
        # elif self.updated: we skipped replacing the same toc

    # #### ADD

    def _add_toc(self, outerToc: str) -> None:
        # check for begin-of-file directives and write output
        _data = self._check_directives(outerToc)
        self._write_toc(_data)
        if not self.updated:
            print(f'Adding toc to "{self.outputFile}"', file=sys.stderr)
            self.updated = True

    def _check_directives(self, outerToc: str) -> str:
        # if a frontmatter, shebang or directive is found, append after first line(s)
        _data = self._read_file()
        _firstLine = _data.splitlines()[0]
        if _firstLine == "":
            # if _firstLine was be empty, re.sub would destroy the original file by inserting an outerToc between every character
            _data = outerToc + "\n" + _data
        else:
            match self.extension:
                case "md":
                    # multi line yaml, toml, js frontmatter for markdown
                    _firstline_yaml = re.search(r"^---$", _firstLine)
                    _firstline_toml = re.search(r"^\+\+\+$", _firstLine)
                    _firstline_json = re.search(r"^{$", _firstLine)
                    if _firstline_yaml is not None:
                        _frontmatters_yaml = re.search(r"^---\n.*?\n---", _data, re.DOTALL)
                        _frontmatter = _frontmatters_yaml.group(0)
                    elif _firstline_toml is not None:
                        _frontmatters_toml = re.search(
                            r"^\+\+\+\n.*?\n\+\+\+", _data, re.DOTALL
                        )
                        _frontmatter = _frontmatters_toml.group(0)
                    elif _firstline_json is not None:
                        _frontmatters_json = re.search(r"^\{\n.*?\n\}", _data, re.DOTALL)
                        _frontmatter = _frontmatters_json.group(0)
                    else:
                        _frontmatter = None
                    if _frontmatter is not None:
                        _firstLine = _frontmatter
                        _firstFewLines = _firstLine + "\n\n" + outerToc
                    else:
                        _firstFewLines = outerToc + "\n\n" + _firstLine
                    # print(_frontmatter)
                    # print(_firstFewLines)
                case "py":
                    # need to match shebang also here since we have a switch/case by extension
                    _firstline_shebang = re.search(r"^#\!", _firstLine)
                    # module docstring for python
                    _firstline_docstring = re.search(r'^"""$', _firstLine)
                    if _firstline_shebang is not None:
                        _firstFewLines = _firstLine + "\n\n" + outerToc
                    else:
                        if _firstline_docstring is not None:
                            _docstrings = re.search(r'^"""\n.*?\n"""', _data, re.DOTALL)
                            _docstring = _docstrings.group(0)
                            _firstLine = _docstring
                            _firstFewLines = _firstLine + "\n\n" + outerToc
                        else:
                            _firstFewLines = outerToc + "\n\n" + _firstLine
                case _:
                    # single line shebang, xml, html, vim, emacs, perl pod
                    if (
                        re.search(r"^#\!", _firstLine)
                        or re.search(r"<\?xml", _firstLine, re.IGNORECASE)
                        or re.search(r"<!doctype", _firstLine, re.IGNORECASE)
                        or re.search(
                            r"^" + re.escape(self.character) + r"\s+([Vv]im?|ex):",
                            _firstLine,
                        )
                        or re.search(
                            r"^" + re.escape(self.character) + r"\s*-\*-", _firstLine
                        )
                        or re.search(
                            r"^" + re.escape(self.character) + r"^=pod$", _firstLine
                        )
                    ):
                        # print("adding toc after shebang")
                        _firstFewLines = _firstLine + "\n\n" + outerToc
                    # else prepend as first line and put everything else after
                    else:
                        # print("adding toc before content")
                        _firstFewLines = outerToc + "\n\n" + _firstLine
            _data = re.sub(re.escape(_firstLine), _firstFewLines, _data, count=1)
        return _data

    # #### UPDATE

    def _update_toc(self, innerToc: str) -> None:
        # replace existing toc and write output
        _data = self._replace_existing_toc(innerToc)
        self._write_toc(_data)
        if not self.updated:
            print(f'Updating toc in "{self.outputFile}"', file=sys.stderr)
            self.updated = True

    def _replace_existing_toc(self, innerToc: str) -> str:
        # replace over multiple lines between two patterns
        _data = self._read_file()
        # if the new toc is already present in the file, it makes no sense to rewrite the file
        # re.escape to treat dots and other characters literally
        if self.outputFile == self.inputFile and re.search(
            re.escape(innerToc), _data, re.MULTILINE
        ):
            self.err = "same"
            _data = ""
            if not self.updated:
                print(f'Skipping unchanged toc in "{self.outputFile}"', file=sys.stderr)
                self.updated = True
        else:
            # use non-greedy regex to only replace the smalles portion of text between innerTocBegin and innerTocEnd
            # use count to only replace the first valid region in file
            _data = re.sub(self.pattern, innerToc, _data, count=1)
        return _data

    # ################ TOC GENERATION

    def _generate_toc(self) -> tuple[str, str]:
        # run text processors and convert lists to strings
        _tocPrefix, _tocSuffix = self._toc_prefix_suffix()
        _tocHeader = self._toc_header()
        _tocBody = self._toc_body()
        _tocFooter = self._toc_footer()
        # exclude empty body
        if _tocBody:
            _innerTocList = _tocHeader + _tocBody + _tocFooter
            _innerToc = "\n".join(_innerTocList)
            # exclude prefix and suffix from innerToc, used for updating toc inline
            _outerToc = (
                "\n".join(_tocPrefix + _innerTocList + _tocSuffix)
                if _tocPrefix
                else _innerToc
            )
            return _innerToc, _outerToc
        else:
            return "", ""

    # ######## PREFIX AND SUFFIX

    def _toc_prefix_suffix(self) -> tuple[list, list]:
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocPrefix = ["/*"]
                _tocSuffix = ["*/"]
            case "html" | "xml" | "md" | "mdx" | "qmd" | "rmd":
                _tocPrefix = ["<!--"]
                _tocSuffix = ["-->"]
            case "ml" | "mli" | "scpd" | "scpt":
                _tocPrefix = ["(*"]
                _tocSuffix = ["*)"]
            case "pl" | "pm" | "pod":
                _tocPrefix = ["=encoding utf8\n=begin comment"]
                _tocSuffix = ["=end comment"]
            case _:
                _tocPrefix = []
                _tocSuffix = []
        return _tocPrefix, _tocSuffix

    # ######## HEADER

    def _toc_header(self) -> list:
        # begin the toc with the file name, truncating it if necessary
        _filename = self.inputFile.name
        if self.inputFile == Path("-"):
            _truncated_filename = (
                f"stdin.{self.extension}" if self.extension != "" else "stdin"
            )
        else:
            _truncated_filename = (
                (_filename[:46] + "...") if len(_filename) > 46 else _filename
            )
        _padding = " " * (50 - len(_truncated_filename))
        self.innerTocBegin = f"{self.character} ┌───────────────────────────────────────────────────────────────┐"
        self.innerTocTitle = (
            f"{self.character} │ Contents of {_truncated_filename}{_padding}│"
        )
        # building the toc header
        # _tocHeaderLines = [
        _tocHeader = [
            self.innerTocBegin,
            self.innerTocTitle,
            f"{self.character} ├───────────────────────────────────────────────────────────────┘",
            f"{self.character} │",
        ]
        # _tocHeader = "\n".join(_tocHeaderLines)
        return _tocHeader

    # ######## FOOTER

    def _toc_footer(self) -> list:
        # end the toc with an horizontal line
        self.innerTocEnd = f"{self.character} └───────────────────────────────────────────────────────────────"
        # _tocFooterLines = [
        _tocFooter = [
            f"{self.character} │",
            self.innerTocEnd,
        ]
        # _tocFooter = "\n".join(_tocFooterLines)
        return _tocFooter

    # ######## BODY

    def _toc_body(self) -> list:
        # read file content and process it accordingly
        # display alert for common errors
        _data = self._read_file()
        _lines = _data.splitlines()
        match self.extension:
            case "ad" | "adoc" | "asc" | "asciidoc":
                _newtoc = self._process_increasing(_lines, "=")
            case "beancount":
                _newtoc = self._process_increasing(_lines, "*")
            case "md" | "mdx" | "qmd" | "rmd":
                _newtoc = self._process_increasing(_lines, "#")
            case "html":
                _newtoc = self._process_html(_data)
            case "1" | "1m" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "n":
                _newtoc = self._process_man(_lines)
            case "pl" | "pm" | "pod":
                _newtoc = self._process_perl(_lines)
            case "rst":
                _newtoc = self._process_restructuredtext(_data)
            case _:
                _newtoc = self._process_generic(_lines)
        _tocBody = self._prettify_connectors(_newtoc)
        return _tocBody

    def _add_heading(self, level: int, text: str) -> str:
        # limit output to a max level
        if self.depth != 0 and level > self.depth:
            _replacement = ""
        else:
            if level == 1:
                _replacement = self.character + " ├── " + text
            else:
                # character, left toc margin, indentation of 3 spaces per heading level, connectors, text
                _replacement = (
                    self.character + " │  " + "   " * (level - 2) + "└── " + text
                )
            # print(_replacement)
        return _replacement

    # #### ASCIIDOC, BEANCOUNT AND MARKDOWN

    def _process_increasing(self, lines: list, heading_character: str) -> list:
        # parse markdown and beancount files, reusing headings or sections
        _newtoc = []
        # ignore comments for other languages
        # don't consider valid comments in code blocks as headings: "```\n# #### Example comment in python\n```"
        _pattern = re.compile(r"^(" + re.escape(heading_character) + "+) (?!#+)(.*)$")
        for n, line in enumerate(lines):
            _match = _pattern.match(line)
            if _match:
                _heading_level = len(_match.group(1))
                _heading_text = (
                    f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                )
                _newtoc.append(self._add_heading(_heading_level, _heading_text))
                # print(_newtoc)
        return _newtoc

    # #### HTML
    def _process_html(self, data: str) -> list:
        _newtoc = []
        # every time an html page is parsed with regex, a software engineer dies
        # _pattern = re.compile(r"<h(\d).*?>(?:<.*?>)?(.*?)</.*?h\d", re.MULTILINE)
        # https://learnbyexample.github.io/python-regex-possessive-quantifier/
        # _pattern = re.compile(r"<h(\d)(?>.*?)>?(?:\s)*(?:<.*?>)?(?:\s)*(.*?)(?:\s)*</(.*?)h\d>", re.MULTILINE)
        # _pattern = re.compile(r"<h(\d).*?>.*?>?(?:\s)*(?:<.*?>)?(?:\s)*(.*?)(?:\s)*</.*?h\d>", re.DOTALL)
        _pattern = re.compile(
            r"<[hH](\d).*?>.*?>?(?:\s)*(?:<.*?>)?(?:\s)*(.*?)(?:\s)*</[hH]\d>",
            re.DOTALL,
        )
        # _matches = _pattern.finditer(data)
        # print(sum(1 for _ in _matches))
        # for _match in _matches:
        # sometimes it fails if not using list()
        # _matches = list(_pattern.finditer(data))
        # print(len(_matches))
        # print(_matches)
        # used to calculare line numbers without starting from the beginning every time
        _fromLastMatch = 0
        n = 1
        for _match in _pattern.finditer(data):
            # indicates character, not line number
            _heading_level = int(_match.group(1))
            # in case there are fancy tags or other elements inside the title, we remove them
            # blood for the blood god
            _heading_text = re.sub(r"<.*?>", "", _match.group(2)).strip()
            # print(f"Heading text: '{_heading_text}'")
            if self.lineNumbers:
                # return the character number, not the line number
                _untilCurrentMatch = _match.start(0)
                # to calculate the line number, let's count the number of "\n" up to the match start, and add 1 to the result
                n += data.count("\n", _fromLastMatch, _untilCurrentMatch)
                _heading_text = _heading_text + " " + str(n)
                # update with the position of the current match
                _fromLastMatch = _untilCurrentMatch
            _newtoc.append(self._add_heading(_heading_level, _heading_text))
        return _newtoc

    # #### RESTRUCTUREDTEXT

    def _process_restructuredtext(self, data: str) -> list:
        _newtoc = []
        # match the line above a streak of "#" (chapters), "*" (sections), etc., avoiding '"""' heredocs (min 4)
        _pattern = re.compile(
            r"(?:[#\*=\-\^~]{2,}|[\"]{4,}|\n)[ \t]*(?!\.\.)(.+)\n[ \t]*([#\*=\-\^~]{2,}|[\"]{4,})\n",
            re.MULTILINE,
        )
        _fromLastMatch = 0
        n = 1
        # https://devguide.python.org/documentation/markup/#sections
        _levels = {"#": 1, "*": 2, "=": 3, "-": 4, "~": 5, "^": 5, '"': 6}
        for _match in _pattern.finditer(data):
            _heading_text = _match.group(1)
            _symbol = _match.group(2)[:1]
            _heading_level = _levels[_symbol]
            if self.lineNumbers:
                # start counting from _heading_text, not optional overline
                _untilCurrentMatch = _match.start(1)
                n += data.count("\n", _fromLastMatch, _untilCurrentMatch)
                _heading_text = _heading_text + " " + str(n)
                # update with the position of the current match
                _fromLastMatch = _untilCurrentMatch
            _newtoc.append(self._add_heading(_heading_level, _heading_text))
        return _newtoc

    # #### MAN PAGES

    def _process_man(self, lines: list) -> list:
        # parse perl files, reusing headings
        _newtoc = []
        _pattern = re.compile(r'^\.(T[Hh]|S[HhSs]) "?(\w+?(?:\s\w+?)*)"?(\s|$)')
        for n, line in enumerate(lines):
            _match = _pattern.match(line)
            if _match:
                match _match.group(1):
                    case "TH" | "Th":
                        _heading_level = 1
                    case "SH" | "Sh":
                        _heading_level = 2
                    case "SS" | "Ss":
                        _heading_level = 3
                _heading_text = (
                    f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                )
                _newtoc.append(self._add_heading(_heading_level, _heading_text))
        return _newtoc

    # #### PERL

    # https://perldoc.perl.org/perlpod
    def _process_perl(self, lines: list) -> list:
        # parse perl files, reusing headings
        _newtoc = []
        _pattern = re.compile(r"^=head(\d) (.*)$")
        for n, line in enumerate(lines):
            _match = _pattern.match(line)
            if _match:
                _heading_level = int(_match.group(1))
                _heading_text = (
                    f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                )
                _newtoc.append(self._add_heading(_heading_level, _heading_text))
        # print(_newtoc)
        return _newtoc

    # #### GENERIC

    def _process_generic(self, lines: list) -> list:
        _newtoc = []
        # using groups to capture the count of '#'
        _pattern = re.compile(
            rf"^(?:\t| )*{re.escape(self.character)} (#{{64}}|#{{32}}|#{{16}}|#{{8}}|#{{4}}|#{{2}}) (.*)$"
        )
        for n, comment in enumerate(lines):
            # print(comment, n)
            _match = _pattern.match(comment)
            if _match:
                _heading_level = self.levels[len(_match.group(1))]
                _heading_text = (
                    f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                )
                # print(_heading_level)
                # print(_heading_text)
                # removing .strip() for cobol files
                _newtoc.append(self._add_heading(_heading_level, _heading_text))
                # print(_newtoc)
        # special post-processing for r
        match self.extension:
            case "r" | "rpres":
                _newtoc = [re.sub(r" [#-=]{4,}", "", line) for line in _newtoc]
        return _newtoc

    # #### PRETTIFY CONNECTORS

    def _prettify_connectors(self, newtoc: list) -> list:
        # add other unicode box drawing symbols to prettify the tree structure
        # "┐" is added to every heading except the last one. to calculate its position
        # "├" replaces "└" for every siblings at the same level, except the last one
        # "│" is added to connect lower siblings to upper siblings with children. to avoid adding it multiple times at every line, we need to reverse the list
        # print(newtoc)
        if newtoc:
            # process the list in reverse order, removing empty elements
            _headings: list[str] = list(filter(None, newtoc[::-1]))
            # print(_headings, file=sys.stderr)
            # for each line store: int_position_of_match: bool_parent_has_not_yet_been_encountered
            # int_position_of_match is 3x the heading level
            _flags: dict[int, bool] = {}
            _pattern = re.compile(r"[└├]")
            for index, heading in enumerate(_headings):
                # "├": first level, "└": other levels
                # print(f"Original line: '{heading}'")
                # skip empty lines (due to --level)
                match_heading = re.search(_pattern, heading)
                if match_heading is not None:
                    # save the position of the match
                    i = match_heading.start()
                    # for the first heading of each level do nothing, as it is the last sibling of that level
                    # if current level is true, it means this heading is not the last sibling, therefore add "├" to connect to siblings below
                    if _flags.get(i, False):
                        heading = heading[:i] + "├" + heading[i + 1 :]
                        # print('Line after "├": ', heading)
                        # print('Dict after "├": ', dict(sorted(_flags.items())))
                    # print(" ")
                    # flag the current level to True, to indicate we are still operating at this level
                    _flags[i] = True
                    # set position of the child level
                    c = i + 3
                    # if child level is True, it means that now we are operating at a level with children,
                    # therefore add "┐" to connect to the first child
                    # this c flag is set to True with _flags[i] = True if we descended again to the child level, e.g. BEGIN H1 H2 H3 H2 H3 END
                    # print(_flags)
                    if _flags.get(c, False):
                        heading = heading[:c] + "┐" + heading[c + 1 :]
                        # print('Line after "┐": ', heading)
                    # print('Dict after "┐": ', dict(sorted(_flags.items())))
                    # print(" ")
                    # set eventual child level to False, because if it was True we just connected to the first child with "┐",
                    # and if it was False a previous sibling connected to the first child
                    _flags[c] = False
                    # the following code section is not triggered for simple "stairs" table of contents, e.g. BEGIN H1, H2, H3, H3, H4 END
                    # however, if we have a higher heading level after a lower one, e.g. BEGIN H1, H2, H3, H2 END
                    # in the example above, the second H2 should be vertically connected with "│" to the first H2
                    # this affects H3, which should also be added a "│", and it also affects the first H2, which should replace its "└" with "├"
                    # for H3, this is done now, for the first H2, it is done via flag the next iteration of 'for index, heading in enumerate(_lines)'
                    # in BEGIN H1, H2, H3, H4, H2 END, H3 is modified once, but H4 is modified with two parallel "│"
                    # start from the parent level, then go back right-to-left at intervals of 3, until position 4
                    for p in range(i - 3, 4, -3):
                        # if a parent level (15) is True, it means that we should vertically connect that level with "│"
                        if _flags.get(p, False):
                            # print("Adding '│' to ", heading)
                            heading = heading[:p] + "│" + heading[p + 1 :]
                            # print('Line after "│": ', heading)
                            # print('Dict after "│": ', dict(sorted(_flags.items())))
                    # print(" ")
                    # replace the original heading with the modified one
                    _headings[index] = heading
                    # reverse before returning
            _tocBody = _headings[::-1]
        else:
            _tocBody = []
        # print(_tocBody)
        return _tocBody

    # ################ TOC INPUT

    def _read_file(self) -> str:
        # read file content and process it accordingly
        # display alert for common errors
        _data = ""
        try:
            if self.inputFile == Path("-"):
                _data = sys.stdin.read()
            else:
                with open(self.inputFile, "r") as f:
                    _data = f.read()
        except FileNotFoundError:
            print(
                f'Skipping non-existing "{self.inputFile}"', file=sys.stderr
            ) if self.err is None else None
            _data = ""
            self.err = "notfound"
        except PermissionError:
            print(
                f'Skipping read-protected "{self.inputFile}"', file=sys.stderr
            ) if self.err is None else None
            _data = ""
            self.err = "read"
        except IsADirectoryError:
            print(
                f'Skipping directory "{self.inputFile}"', file=sys.stderr
            ) if self.err is None else None
            _data = ""
            self.err = "directory"
        except UnicodeDecodeError:
            print(
                f'Skipping binary "{self.inputFile}"', file=sys.stderr
            ) if self.err is None else None
            _data = ""
            self.err = "binary"
        except BaseException:
            print(
                f'Unknown error while reading "{self.inputFile}"', file=sys.stderr
            ) if self.err is None else None
            _data = ""
            self.err = "unknownr"
        finally:
            return _data
