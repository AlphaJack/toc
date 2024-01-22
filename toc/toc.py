#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of toc.py                                            │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
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
# │        │  ├── BEANCOUNT FILES
# │        │  ├── MARKDOWN FILES
# │        │  ├── OTHER FILES
# │        │  └── PRETTIFY CONNECTORS
# │        └── FOOTER
# │
# └───────────────────────────────────────────────────────────────


# ################################################################ LIBRARIES

# regex
import re
# stderr
import sys


# ################################################################ CLASS

class Toc:
    def __init__(self, file: str = "", lineNumbers: bool = False, character: str = ""):
        self.file = file
        self.extension = file.split(".")[-1].lower() if "." in file else ""
        self.character = character
        self.lineNumbers = lineNumbers
        self.err = None
        self.updated = False

# ################################ PUBLIC METHODS

# ################ COMMENT CHARACTER

    def set_character(self):
        # automatically select the comment type from its extension, if not already set
        match self.extension:
            case "c" | "carbon" | "cc" | "coffee" | "cpp" | "cs" | "css" | "d" | "dart" | "go" | "h" | "hpp" | "htm" | "html" | "hxx" | "java" | "js" | "kt" | "md" | "pas" | "php" | "pp" | "proto" | "qs" | "rs" | "scala" | "sc" | "swift" | "ts" | "typ" | "xml" | "zig":
                self.character = "//"
            case "ahk" | "asm" | "beancount" | "cl" | "clj" | "cljs" | "cljc" | "edn" | "fasl" | "ini" | "lisp" | "lsp" | "rkt" | "scm" | "ss":
                self.character = ";"
            case "bib" | "cls" | "erl" | "hrl" | "mat" | "sty" | "tex":
                self.character = "%"
            case "adb" | "ads" | "elm" | "hs" | "lua" | "sql":
                self.character = "--"
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
            case "cob":
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
            print(f'Skipping empty "{self.character}" toc for {self.file}', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            print(_outerToc)

# ######## FILE

    def to_file(self):
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
        self.innerTocBegin = f"{self.character} ┌───────────────────────────────────────────────────────────────┐"
        self.innerTocEnd = f"{self.character} └───────────────────────────────────────────────────────────────"
        if _outerToc == "":
            print(f'Skipping empty "{self.character}" toc for {self.file}', file=sys.stderr) if self.err is None else None
            self.err = "empty"
        else:
            with open(self.file) as f:
                _data = f.read()
                # re.MULTILINE: https://docs.python.org/3/library/re.html#re.M
                if re.search(r'^%s$' % self.innerTocBegin, _data, flags=re.MULTILINE) and re.search(r'^%s$' % self.innerTocEnd, _data, flags=re.MULTILINE):
                    self._update_toc(_innerToc)
                else:
                    self._add_toc(_outerToc)

    def _write_toc(self, data):
        # common function to rewrite file
        if data:
            try:
                with open(self.file, "w") as f:
                    f.write(data)
            except PermissionError:
                print(f"Skipping write-protected file {self.file}", file=sys.stderr)
                self.err = "write"
        elif not self.updated:
            # data should never be empty if self.updated = False, but in case least we prevented cleaning the file
            print(f"Skipping purging file {self.file}", file=sys.stderr)
            self.updated = True
        # elif self.updated: we skipped replacing the same toc

# #### ADD

    def _add_toc(self, outerToc):
        # check for shebang and write output
        _data = self._check_shebang(outerToc)
        self._write_toc(_data)
        print(f"Adding toc to file {self.file}", file=sys.stderr)
        self.updated = True

    def _check_shebang(self, outerToc):
        # if shebang is found, append after first line
        with open(self.file) as f:
            _data = f.read()
            _firstLine = _data.split("\n", 1)[0]
            if re.search(r'^#!/usr', _firstLine):
                # print("adding toc after shebang")
                _firstFewLines = _firstLine + "\n\n" + outerToc
            # else prepend as first line and put everything else after
            else:
                # print("adding toc before content")
                _firstFewLines = outerToc + "\n\n" + _firstLine
            # print(firstFewLines)
            _data = re.sub(_firstLine, _firstFewLines, _data, flags=re.DOTALL)
            return _data

# #### UPDATE

    def _update_toc(self, innerToc):
        # replace existing toc and write output
        _data = self._replace_existing_toc(innerToc)
        self._write_toc(_data)
        if not self.updated:
            print(f"Updating toc in file {self.file}", file=sys.stderr)
            self.updated = True

    def _replace_existing_toc(self, innerToc):
        # replace over multiple lines between two patterns
        with open(self.file) as f:
            _data = f.read()
            # if the new toc is already present in the file, it makes no sense to rewrite the file
            # re.escape to treat dots and other characters literally
            if re.search(re.escape(innerToc), _data, flags=re.MULTILINE):
                self.err = "same"
                _data = None
                if not self.updated:
                    print(f"Skipping replacing same toc in file {self.file}", file=sys.stderr)
                    self.updated = True
            else:
                # use non-greedy regex to only replace the smalles portion of text between innerTocBegin and innerTocEnd
                # use count to only replace the first valid region in file
                _data = re.sub('%s(.*?)%s' % (self.innerTocBegin, self.innerTocEnd), innerToc, _data, count=1, flags=re.DOTALL)
            return _data

# ################ TOC GENERATION

    def _generate_toc(self):
        # run text processors and store outputs
        _tocPrefix, _tocHeader = self._toc_header()
        _tocBody = self._toc_body()
        _tocFooter, _tocSuffix = self._toc_footer()
        # exclude empty body
        if _tocBody == "":
            _innerToc = ""
            _outerToc = ""
        else:
            _innerToc = _tocHeader + "\n" + _tocBody + "\n" + _tocFooter
            # exclude prefix and suffix from innerToc, used for updating toc inline
            _outerToc = _innerToc if _tocPrefix == "" else _tocPrefix + "\n" + _innerToc + "\n" + _tocSuffix
        return _innerToc, _outerToc

# ######## HEADER

    def _toc_header(self):
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocPrefix = "/*"
            case "html" | "md" | "xml":
                _tocPrefix = "<!--"
            case "ml" | "mli" | "scpd" | "scpt":
                _tocPrefix = "(*"
            case _:
                _tocPrefix = ""
        # begin the toc with the file name, truncating it if necessary
        _filename = self.file.split("/")[-1]
        _filename = (_filename[:46] + "...") if len(_filename) > 46 else _filename
        _tocHeader = f"{self.character} ┌───────────────────────────────────────────────────────────────┐\n"
        _tocHeader += f"{self.character} │ Contents of {_filename}{' ' * (50 - len(_filename))}│\n"
        _tocHeader += f"{self.character} ├───────────────────────────────────────────────────────────────┘\n"
        _tocHeader += f"{self.character} │"
        return _tocPrefix, _tocHeader

# ######## BODY

    def _toc_body(self):
        # read file content and process it accordingly
        # display alert for common errors
        try:
            with open(self.file, "r") as f:
                _lines = f.readlines()
                match self.extension:
                    case "beancount":
                        _newtoc = self._process_beancount(_lines)
                    case "md":
                        _newtoc = self._process_markdown(_lines)
                    case _:
                        _newtoc = self._process_other(_lines)
                _tocBody = self._prettify_connectors(_newtoc)
        except FileNotFoundError:
            print(f"Skipping non-existing file {self.file}", file=sys.stderr)
            _tocBody = ""
            self.err = "notfound"
        except PermissionError:
            print(f"Skipping read-protected file {self.file}", file=sys.stderr)
            _tocBody = ""
            self.err = "read"
        except IsADirectoryError:
            print(f"Skipping directory {self.file}", file=sys.stderr)
            _tocBody = ""
            self.err = "directory"
        except UnicodeDecodeError:
            print(f"Skipping binary file {self.file}", file=sys.stderr)
            _tocBody = ""
            self.err = "binary"
        except BaseException:
            print(f"Skipping file {self.file}", file=sys.stderr)
            _tocBody = ""
            self.err = "unknown"
        finally:
            return _tocBody

# #### BEANCOUNT FILES

    def _process_beancount(self, lines):
        # pars beancount files, reusing sections
        _oldtoc, _newtoc = [], []
        if self.lineNumbers:
            _oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if re.match(r'^\*+ .*$', line)]
        else:
            _oldtoc = [line for line in lines if re.match(r'^\*+ .*$', line)]
        _newtoc = [re.sub(r"^\*{6}", "\t│              └──", line.strip()) for line in _oldtoc]
        _newtoc = [re.sub(r"^\*{5}", "\t│           └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^\*{4}", "\t│        └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^\*{3}", "\t│     └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^\*{2}", "\t│  └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^\*", "\t├──", line) for line in _newtoc]
        _newtoc = [line.replace("\t", f"\n{self.character} ") for line in _newtoc]
        return _newtoc

# #### MARKDOWN FILES

    def _process_markdown(self, lines):
        # pars markdown files, reusing headings
        _oldtoc, _newtoc = [], []
        if self.lineNumbers:
            _oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if re.match(r'^#+ [^#│├└┌]', line)]
        else:
            _oldtoc = [line for line in lines if re.match(r'^#+ [^#│├└┌]', line)]
        _newtoc = [re.sub(r"^#{6}", "\t│              └──", line.strip()) for line in _oldtoc]
        _newtoc = [re.sub(r"^#{5}", "\t│           └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^#{4}", "\t│        └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^#{3}", "\t│     └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^#{2}", "\t│  └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^#", "\t├──", line) for line in _newtoc]
        _newtoc = [line.replace("\t", f"\n{self.character} ") for line in _newtoc]
        return _newtoc

# #### OTHER FILES

    def _process_other(self, lines):
        # parse all other files types, according to the comment convention
        _oldtoc, _newtoc = [], []
        if self.lineNumbers:
            _oldtoc = [f"{line.strip()} {i+1}" for i, line in enumerate(lines) if line.startswith(self.character) and "####" in line]
        else:
            _oldtoc = [line.strip() for line in lines if line.startswith(self.character) and "####" in line]
        _newtoc = [re.sub(r"^" + re.escape(self.character) + " ################################################################", "\n" + self.character + " ├──", line) for line in _oldtoc]
        _newtoc = [re.sub(r"^" + re.escape(self.character) + " ################################", "\n" + self.character + " │  └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^" + re.escape(self.character) + " ################", "\n" + self.character + " │     └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^" + re.escape(self.character) + " ########", "\n" + self.character + " │        └──", line) for line in _newtoc]
        _newtoc = [re.sub(r"^" + re.escape(self.character) + " ####", "\n" + self.character + " │           └──", line) for line in _newtoc]
        return _newtoc

# #### PRETTIFY CONNECTORS

    def _prettify_connectors(self, newtoc):
        # improves nested appearance adding ┐ and │ where needed
        _newtoc = "".join(newtoc)
        # split the input string into lines and reverse it
        _lines = _newtoc.split('\n')[::-1]
        # initialize a large list of zeros
        _flags = [0] * 1000
        # iterate over the lines
        for index, line in enumerate(_lines):
            # if the line contains either '└' or '├'
            if re.search("[└├]", line):
                # find the position of the match
                i = re.search("[└├]", line).start()
                # if the flag at position i is set, replace the character at position i with '├'
                if _flags[i] == 1:
                    line = line[:i] + "├" + line[i + 1:]
                # set the flag at position i
                _flags[i] = 1
                # Find the position of the nested children
                j = i + 3
                # if the flag at position j is set, replace the character at position j with '┐'
                if _flags[j] == 1:
                    line = line[:j] + "┐" + line[j + 1:]
                # reset the flag at position j
                _flags[j] = 0
                # for all positions less than i
                while i > 0:
                    i -= 1
                    # if the flag at position i is set, replace the character at position i with '│'
                    if _flags[i] == 1:
                        line = line[:i] + "│" + line[i + 1:]
                # update the line in the list
                _lines[index] = line
        # reverse the lines and join them into a single string with newline characters
        _tocBody = '\n'.join(_lines[::-1])
        # print lines that are not empty
        _tocBody = '\n'.join([line for line in _tocBody.split('\n') if line.strip() != ''])
        return _tocBody

# ######## FOOTER

    def _toc_footer(self):
        # end the toc with an horizontal line
        _tocFooter = f"{self.character} │\n"
        _tocFooter = _tocFooter + f"{self.character} └───────────────────────────────────────────────────────────────"
        # print a multi-line comment delimiter if needed
        match self.extension:
            case "css":
                _tocSuffix = "*/"
            case "html" | "md" | "xml":
                _tocSuffix = "-->"
            case "ml" | "mli" | "scpd" | "scpt":
                _tocSuffix = "*)"
            case _:
                _tocSuffix = ""
        return _tocFooter, _tocSuffix
