<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CHANGELOG.md                                      │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Changelog - toc
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
- Fixed a bug that may lead to multiple tocs being added

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
