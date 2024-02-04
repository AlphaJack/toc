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
# │     ├──┐TOC GENERATION
# │     │  ├── HEADER
# │     │  ├──┐BODY
# │     │  │  ├── BEANCOUNT AND MARKDOWN
# │     │  │  ├── PERL
# │     │  │  ├── GENERIC
# │     │  │  └── PRETTIFY CONNECTORS
# │     │  └── FOOTER
# │     └── TOC INPUT
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ MODULES

# regex
import re
# stderr
import sys


# ################################################################ CLASS

class Toc:
    def __init__(self, inputFile: str = "", outputFile=None, lineNumbers: bool = False, character: str = "#"):
        self.inputFile = str(inputFile)
        self.outputFile = outputFile
        self.extension = self.inputFile.split(".")[-1].lower() if "." in self.inputFile else ""
        self.lineNumbers = lineNumbers
        self.character = character
        self.err = None
        self.updated = False
        self.innerTocBegin = None
        self.innerTocTitle = None
        self.innerTocEnd = None
        self.pattern = None
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
            print(f'No "{self.character}" toc for "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            print(_outerToc)

# ######## FILE

    def to_file(self, output=None):
        # if file has been specified, print there instead of the original file (useful for testing)
        if self.outputFile is None:
            self.outputFile = output if output else self.inputFile
        # run twice because updating the toc may shift everything down
        n = 2 if self.lineNumbers else 1
        for _ in range(n):
            self._add_or_update()

# ################################ INTERNAL METHODS
# ################ TOC OUTPUT
# ######## FILE

    def _add_or_update(self):
        # if the file does not contain a toc, add it, otherwise update it
        _innerToc, _outerToc = self._generate_toc()
        if _outerToc == "":
            print(f'Skipping writing empty "{self.character}" toc to "{self.outputFile}"', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            # re.MULTILINE: https://docs.python.org/3/library/re.html#re.M
            self.pattern = re.compile(rf"{self.innerTocBegin}\n{self.innerTocTitle}(.*?){self.innerTocEnd}", re.DOTALL)
            # print(self.pattern)
            _data = self._read_file()
            # print(_data)
            if re.search(self.pattern, _data):
                self._update_toc(_innerToc)
            else:
                self._add_toc(_outerToc)

    def _write_toc(self, data):
        # common function to rewrite file
        if data:
            try:
                with open(self.outputFile, "w") as f:
                    f.write(data)
            except PermissionError:
                print(f'Skipping write-protected file "{self.outputFile}"', file=sys.stderr) if self.err is None else None
                self.err = "write"
                self.updated = True
            except BaseException:
                print(f'Skipping writing file "{self.outputFile}"', file=sys.stderr) if self.err is None else None
                self.err = "unknownw"
                self.updated = True
        elif not self.updated:
            # data should never be empty if self.updated = False, but in case least we prevented cleaning the file
            print(f'Skipping writing file "{self.outputFile}"', file=sys.stderr)
            self.updated = True
        # elif self.updated: we skipped replacing the same toc

# #### ADD

    def _add_toc(self, outerToc):
        # check for begin-of-file directives and write output
        _data = self._check_directives(outerToc)
        self._write_toc(_data)
        if not self.updated:
            print(f'Adding toc to file "{self.outputFile}"', file=sys.stderr)
            self.updated = True

    def _check_directives(self, outerToc):
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
            print(f'Updating toc in file "{self.outputFile}"', file=sys.stderr)
            self.updated = True

    def _replace_existing_toc(self, innerToc):
        # replace over multiple lines between two patterns
        _data = self._read_file()
        # if the new toc is already present in the file, it makes no sense to rewrite the file
        # re.escape to treat dots and other characters literally
        if self.outputFile == self.inputFile and re.search(re.escape(innerToc), _data, re.MULTILINE):
            self.err = "same"
            _data = None
            if not self.updated:
                print(f'Skipping replacing same toc in file "{self.outputFile}"', file=sys.stderr)
                self.updated = True
        else:
            # use non-greedy regex to only replace the smalles portion of text between innerTocBegin and innerTocEnd
            # use count to only replace the first valid region in file
            _data = re.sub(self.pattern, innerToc, _data, count=1)
        return _data

# ################ TOC GENERATION

    def _generate_toc(self):
        # run text processors and convert lists to strings
        _tocPrefix, _tocHeader = self._toc_header()
        _tocBody = self._toc_body()
        _tocFooter, _tocSuffix = self._toc_footer()
        # exclude empty body
        if _tocBody:
            _innerTocList = _tocHeader + _tocBody + _tocFooter
            _innerToc = "\n".join(_innerTocList)
            # exclude prefix and suffix from innerToc, used for updating toc inline
            _outerToc = "\n".join(_tocPrefix + _innerTocList + _tocSuffix) if _tocPrefix else _innerToc
            return _innerToc, _outerToc
        else:
            return "", ""

# ######## HEADER

    def _toc_header(self):
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocPrefix = ["/*"]
            case "html" | "xml" | "md" | "qmd" | "rmd":
                _tocPrefix = ["<!--"]
            case "ml" | "mli" | "scpd" | "scpt":
                _tocPrefix = ["(*"]
            case "pl" | "pm" | "pod":
                _tocPrefix = ["=encoding utf8\n=begin comment"]
            case _:
                _tocPrefix = []
        # begin the toc with the file name, truncating it if necessary
        _filename = self.inputFile.split("/")[-1]
        _truncated_filename = (_filename[:46] + "...") if len(_filename) > 46 else _filename
        _padding = ' ' * (50 - len(_truncated_filename))
        self.innerTocBegin = f"{self.character} ┌───────────────────────────────────────────────────────────────┐"
        self.innerTocTitle = f"{self.character} │ Contents of {_truncated_filename}{_padding}│"
        # building the toc header
        # _tocHeaderLines = [
        _tocHeader = [
            self.innerTocBegin,
            self.innerTocTitle,
            f"{self.character} ├───────────────────────────────────────────────────────────────┘",
            f"{self.character} │"
        ]
        # _tocHeader = "\n".join(_tocHeaderLines)
        return _tocPrefix, _tocHeader

# ######## BODY

    def _toc_body(self):
        # read file content and process it accordingly
        # display alert for common errors
        _lines = self._read_file().splitlines()
        match self.extension:
            case "beancount":
                _newtoc = self._process_increasing(_lines, "*")
            case "md":
                _newtoc = self._process_increasing(_lines, "#")
            case "pl" | "pm" | "pod":
                _newtoc = self._process_perl(_lines)
            case _:
                _newtoc = self._process_generic(_lines)
        _tocBody = self._prettify_connectors(_newtoc)
        return _tocBody

    def _replace_comment(self, level, text):
        if level == 1:
            _replacement = self.character + " ├── " + text
        else:
            # 3 spaces per heading level
            _indentation = "   " * (level - 2)
            _replacement = self.character + " │  " + _indentation + "└── " + text
        # print(_replacement)
        return _replacement

# #### BEANCOUNT AND MARKDOWN

    def _process_increasing(self, lines, heading):
        # parse markdown and beancount files, reusing headings or sections
        _newtoc = []
        # ignore comments for other languages
        # don't consider valid comments in code blocks as headings: "```\n# #### Example comment in python\n```"
        _pattern = re.compile(r"^(" + re.escape(heading) + "+) (?!#+)(.*)$")
        for n, comment in enumerate(lines):
            _match = _pattern.match(comment)
            if _match:
                _heading_level = len(_match.group(1))
                _heading_text = f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                _newtoc.append(_pattern.sub(self._replace_comment(_heading_level, _heading_text), comment))
                # print(_newtoc)
        return _newtoc

# #### PERL

    # https://perldoc.perl.org/perlpod
    def _process_perl(self, lines):
        # parse perl files, reusing headings
        _newtoc = []
        _pattern = re.compile(r"^=head(\d) (.*)$")
        for n, comment in enumerate(lines):
            _match = _pattern.match(comment)
            if _match:
                _heading_level = int(_match.group(1))
                _heading_text = f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                _newtoc.append(_pattern.sub(self._replace_comment(_heading_level, _heading_text), comment))
        # print(_newtoc)
        return _newtoc

# #### GENERIC

    def _process_generic(self, lines):
        _newtoc = []
        # using groups to capture the count of '#'
        _pattern = re.compile(rf"^{re.escape(self.character)} (#{{64}}|#{{32}}|#{{16}}|#{{8}}|#{{4}}|#{{2}}) (.*)$")
        for n, comment in enumerate(lines):
            # print(comment, n)
            _match = _pattern.match(comment)
            if _match:
                _heading_level = self.levels[len(_match.group(1))]
                _heading_text = f"{_match.group(2)} {n+1}" if self.lineNumbers else _match.group(2)
                # print(_heading_level)
                # print(_heading_text)
                # removing .strip() for cobol files
                _newtoc.append(_pattern.sub(self._replace_comment(_heading_level, _heading_text), comment))
                # print(_newtoc)
        # special post-processing for r
        match self.extension:
            case "r" | "rpres":
                _newtoc = [re.sub(r" [#-=]{4,}", "", line) for line in _newtoc]
        return _newtoc

# #### PRETTIFY CONNECTORS

    def _prettify_connectors(self, newtoc):
        # add other unicode box drawing symbols to prettify the tree structure
        # "┐" is added to every heading except the last one. to calculate its position
        # "├" replaces "└" for every siblings at the same level, except the last one
        # "│" is added to connect lower siblings to upper siblings with children. to avoid adding it multiple times at every line, we need to reverse the list
        if newtoc:
            # process the list in reverse order, as we
            _headings = newtoc[::-1]
            # for each line store: int_position_of_match: bool_parent_has_not_yet_been_encountered
            # int_position_of_match is 3x the heading level
            _flags = {}
            _pattern = re.compile(r"[└├]")
            for index, heading in enumerate(_headings):
                # "├": first level, "└": other levels
                # print("Original line:  ", heading)
                # save the position of the match
                i = re.search(_pattern, heading).start()
                # for the first heading of each level do nothing, as it is the last sibling of that level
                # if current level is true, it means this heading is not the last sibling, therefore add "├" to connect to siblings below
                if _flags.get(i, False):
                    heading = heading[:i] + "├" + heading[i + 1:]
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
                    heading = heading[:c] + "┐" + heading[c + 1:]
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
                        heading = heading[:p] + "│" + heading[p + 1:]
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

# ######## FOOTER

    def _toc_footer(self):
        # end the toc with an horizontal line
        self.innerTocEnd = f"{self.character} └───────────────────────────────────────────────────────────────"
        # _tocFooterLines = [
        _tocFooter = [
            f"{self.character} │",
            self.innerTocEnd,
        ]
        # _tocFooter = "\n".join(_tocFooterLines)
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocSuffix = ["*/"]
            case "html" | "xml" | "md" | "qmd" | "rmd":
                _tocSuffix = ["-->"]
            case "ml" | "mli" | "scpd" | "scpt":
                _tocSuffix = ["*)"]
            case "pl" | "pm" | "pod":
                _tocSuffix = ["=end comment"]
            case _:
                _tocSuffix = []
        return _tocFooter, _tocSuffix

# ################ TOC INPUT

    def _read_file(self):
        # read file content and process it accordingly
        # display alert for common errors
        _data = ""
        try:
            with open(self.inputFile, "r") as f:
                _data = f.read()
        except FileNotFoundError:
            print(f'Skipping non-existing file "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            _data = ""
            self.err = "notfound"
        except PermissionError:
            print(f'Skipping read-protected file "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            _data = ""
            self.err = "read"
        except IsADirectoryError:
            print(f'Skipping directory "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            _data = ""
            self.err = "directory"
        except UnicodeDecodeError:
            print(f'Skipping binary file "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            _data = ""
            self.err = "binary"
        except BaseException:
            print(f'Skipping file "{self.inputFile}"', file=sys.stderr) if self.err is None else None
            _data = ""
            self.err = "unknownr"
        finally:
            return _data
