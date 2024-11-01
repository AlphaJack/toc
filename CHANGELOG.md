# Changelog - toc

## [2.7.3] - 2024-11-01
### Added

- Added latex support
- Added typst support

### Performance

- Using dictionaries instead of match case when it makes sense

## [2.7.2] - 2024-10-27
### Added

- Added magic comment support for LaTeX

## [2.7.1] - 2024-08-19
### Added

- Placing TOC after module docstring in python files

### Changed

- Updating file name in TOC in case file has been renamed
- Using pathlib to reference files

### Fixed

- Docstring matching
- HTML headings that span across multiple lines are now matched

### Testing

- Added man and line numbers tests
- Added HTML tests

## [2.6.0] - 2024-03-16
### Added

- Set maximum toc depth with `--depth int`
- Using importlib.metadata.version() for `--version`
- Static type checking

### Changed

- Support for comments that start after spaces or tabs
- To run without being installed, `python -m toc.cli` must be used instead of `./toc/cli.py`

### Documentation

- Highlighted support for markup languages

### Testing

- Added tests for files formatted by python-black

## [2.5.0] - 2024-02-23
### Added

- Native reStructuredText support
- Native AsciiDoc support

### Testing

- Added AsciiDoc and reStructuredText tests

## [2.4.0] - 2024-02-07
### Added

- Native man pages support
- Line numbers to HTML toc
- Stdin support with "-" argument
- Set an arbitrary extension with "-e", useful for stdin
- Native HTML support

### Changed

- Moved prefix and suffix to dedicated function

### Documentation

- Documented HTML and stdin support

### Performance

- Avoiding replacing original match when writing toc

### Testing

- Added stdin and ouput tests for cli script
- Added cli testing

### Various

- Optimized range in _prettify_connectors()
- Using single source for package version

## [2.3.0] - 2024-02-02
### Added

- If `-o outputFile` is specified, toc will write there even if the inputFile's toc is already up-to-date
- Drastic performance improvements by reducing regex and list iterations
- Support for rstudio foldable sections

### Documentation

- Added useful tools to CONTRIBUTING.md
- Explaining better what _prettify_connector() does
- Added code snippets to CONTRIBUTING.md

### Fixed

- Not stripping lines to preserve cobol indentation
- Avoiding printing twice the same error or warning message

### Performance

- Simplified and explained _prettify_connectors()
- Unified comment replacement in _replace_comment()
- Defining toc multiline regex pattern once
- Centralized file opening function
- Storing toc pieces in lists until _generate_toc()

### Testing

- Added complex toc nexting
- Added more unit tests to toc.py
- Added check for missing reference file

### Various

- Avoiding replacing builtins like "file", "input" and "list"

## [2.2.0] - 2024-01-29
### Added

- Glob expansion support when parsing lists of files
- Read files from lists with `-l`
- Man pages support (groff/mdoc)
- Native perl pod support
- Specify arbitrary output with `-o output_file`
- Respect xml, doctype, vim and emacs directives
- Respect markdown frontmatters

### Documentation

- Split README.md in USAGE.md
- Updated changelog
- Renamed first example to file.c

### Fixed

- Limiting re.sub to 1 also if toc needs to be added
- Avoid re.sub if first line is empty
- Sanitizing input file type to str
- Fixed a bug thay may lead to multiple tocs being added

### Testing

- Added new cases to test toc with empty or repeated first line of file
- Testing also cli script
- Not committing local test coverage
- Not considering files under tests/output
- Added input and reference test for testing

### Various

- Using re.search() instead of re.match(), removed re flags= where not needed

## [2.1.0] - 2024-01-22
### Added

- Support for even more languages
- Added example comments to README.md
- Added PyPI url to README.md

### Documentation

- Added changelog
- Added changelog support through git-cliff

### Various

- Set PyPI project name to tableofcontents, added GH workflow for PyPI

## [2.0.0] - 2024-01-21

- Rewriten `toc` in pure `python`
- Published to PyPI as [`tableofcontents`](https://pypi.org/project/tableofcontents)
- Added feature to prepend the table of contents to files, preserving shebangs

## [1.0.0] - 2023-11-03

- Initial release of `toc` in `bash`, `perl`, `sed` and `awk`
