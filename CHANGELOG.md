# Changelog - toc

## Work in progress
### Added

- Specify arbitrary output with `-o output_file`
- Respect xml, doctype, vim and emacs directives
- Respect markdown frontmatters

### Documentation

- Renamed first example to file.c

### Fixed

- Sanitizing input file type to str
- Fixed a bug thay may lead to multiple tocs being added

### Testing

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
