<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CHANGELOG.md                                      │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Changelog - toc
// │  ├──┐[2.4.0] - 2024-02-07
// │  │  ├── Added
// │  │  ├── Changed
// │  │  ├── Documentation
// │  │  ├── Performance
// │  │  └── Testing
// │  ├──┐[2.3.0] - 2024-02-02
// │  │  ├── Added
// │  │  ├── Documentation
// │  │  ├── Fixed
// │  │  ├── Performance
// │  │  └── Testing
// │  ├──┐[2.2.0] - 2024-01-29
// │  │  ├── Added
// │  │  ├── Documentation
// │  │  ├── Fixed
// │  │  └── Testing
// │  ├──┐[2.1.0] - 2024-01-22
// │  │  ├── Added
// │  │  └── Documentation
// │  ├── [2.0.0] - 2024-01-21
// │  └── [1.0.0] - 2023-11-03
// │
// └───────────────────────────────────────────────────────────────
-->

# Changelog - toc

## [2.4.0] - 2024-02-07
### Added

- Native man pages support
- Line numbers to HTML toc
- Stdin support with `-` argument
- Set an arbitrary extension with `-e`, useful for stdin
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

## [2.1.0] - 2024-01-22
### Added

- Support for even more languages
- Added example comments to README.md
- Added PyPI url to README.md

### Documentation

- Added changelog
- Added changelog support through git-cliff

## [2.0.0] - 2024-01-21

- Rewriten `toc` in pure `python`
- Published to PyPI as [`tableofcontents`](https://pypi.org/project/tableofcontents)
- Added feature to prepend the table of contents to files, preserving shebangs

## [1.0.0] - 2023-11-03

- Initial release of `toc` in `bash`, `perl`, `sed` and `awk`
