<!--
# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of README.md                                         │
# ├───────────────────────────────────────────────────────────────┘
# │
# │  └── TODO
# ├──┐toc
# │  ├── Requirements
# │  ├──┐Usage
# │  │  ├── Writing the comments
# │  │  └── Generating the table of contents
# │  ├── Contributions
# │  └──┐Changelog
# │     ├── 2.0.0
# │     └── 1.0.0
# │
# └───────────────────────────────────────────────────────────────
-->

## TODO

Rename functions

Update readme

Try deploy on github and testpypi

# toc

toc - Generate a table of contents from the comments of a file

toc will search for a special kind of comments in a file, and will render them as a Table of Contents.
The output can then be pasted back in the original file.

See it in action:
[![asciicast](https://asciinema.org/a/619015.svg)](https://asciinema.org/a/619015)

## Requirements

This tool needs the following programs to be installed:

- python

To run the program from your command line as `toc`, place the "toc" file inside a folder in your path, such as "/usr/bin/" for UNIX-like systems.

## Usage

The generation of a table of contents requires two actions:

1. writing the comments representing the different sections of a file
2. running the `toc` program to turn those comments into a table of contents

### Writing the comments

To write one of these comments:

- Start a new line with the comment character for your document language, such as "#", "//", ";", "%", "--".
- Add a space and a series of 64/32/16/8/4 hash symbols ("#"), according to the desired nesting level (use more hashes for more generic sections, and halve their number for more specific headings)
- Add another space and the title of the section

Example for a $LaTeX$ document:

```latex
% ################################################################ Heading at 1st level

...

% ################################ Heading at 2nd level

...
```

For languages that do not feature in-line comments, such as CSS and HTML, you can use the "#" symbol, 
and write the multi-line comment characters in the lines before and after the comment.

Example for a CSS document:

```css
/*
# ################################################################ Heading at 1st level
*/

...

/*
# ################################ Heading at 2nd level
*/

...
```

For markdown files (.md), just write the headings as you would normally, there is no need for comments.

Example for a Markdown file:

```md
​# Heading at 1st level

...

​## Heading at 2nd level

...
```

### Generating the table of contents

Once the comments have been added to the file, it is possible to run `toc file.ext` to will generate its table of contents.

This operation derives the comment character (e.g. "#", "//", etc.) from the extension of the file.

To specify a comment character, you can use one of the `-b`, `-c`, `-i`, `-l`, `-s` flags, followed by the file name.

In addition, the `-n` flag will output line numbers, similar to the page number in a book's toc.
However, if you copy and paste the generated table of contents back in the original file, the line numbers will not be accurate anymore.
This flag must be specified before the file name.

The current version of the program can be output with the `-v` flag.

The `-h` flag will print a help message with the available flags and some examples.

## Contributions

Do you have an idea or you found an issue? Pull Requests are welcome!

## Changelog

### 2.0.0

`toc` rewritten in python

### 1.0.0

Initial release
