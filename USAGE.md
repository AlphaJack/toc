<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of USAGE.md                                          │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Detailed TOC usage
// │  ├── Read the table of contents
// │  ├── Embed the table of contents in the original file
// │  └── Process multiple files
// ├── ignore-this-file.txt
// ├──┐glob expansion
// │  ├── Show line numbers
// │  ├── Set a custom comment character
// │  ├── Redirect output to another file
// │  ├── Other commands
// │  └──┐Exceptional file types
// │     ├──┐No comments needed
// │     │  ├── Markdown
// │     │  ├── Beancount
// │     │  └── Perl
// │     ├──┐Wrap around comments needed
// │     │  ├── CSS
// │     │  ├── HTML and Quarto
// │     │  └── OCaml
// │     └──┐Compatibility with third-party editors
// │        ├── Vim and Emacs
// │        └── RStudio
// │
// └───────────────────────────────────────────────────────────────
-->

# Detailed TOC usage

The scenarios below show different features of `toc`

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Detailed TOC usage](#detailed-toc-usage)
   * [Read the table of contents](#read-the-table-of-contents)
   * [Embed the table of contents in the original file](#embed-the-table-of-contents-in-the-original-file)
   * [Process multiple files](#process-multiple-files)
   * [Show line numbers](#show-line-numbers)
   * [Set a custom comment character](#set-a-custom-comment-character)
   * [Redirect output to another file](#redirect-output-to-another-file)
   * [Other commands](#other-commands)
   * [Exceptional file types](#exceptional-file-types)
      + [No comments needed](#no-comments-needed)
         - [Markdown](#markdown)
         - [Beancount](#beancount)
         - [Perl](#perl)
      + [Wrap around comments needed](#wrap-around-comments-needed)
         - [CSS](#css)
         - [HTML and Quarto](#html-and-quarto)
         - [OCaml](#ocaml)
      + [Compatibility with third-party editors](#compatibility-with-third-party-editors)
         - [Vim and Emacs](#vim-and-emacs)
         - [RStudio](#rstudio)

<!-- TOC end -->

## Read the table of contents

Let's say you want to structure your javascript file "example.js".
Single line comments in this language start with `//`.
You open your file and add these comments where you need them:

```js
#!/usr/bin/env node

// ################################################################ Main section

let Section1 = "Write //, 64 hash characters and the name of section"

// ################################ Nested section

let Section2 = "Write //, 32 hash characters and the name of section"

// ################ Nested section

let Section3 = "Write //, 16 hash characters and the name of section"

// ######## Nested section

let Section4 = "Write //, 8 hash characters and the name of section"

// #### Nested section

let Section5 = "Write //, 4 hash characters and the name of section"
```

If you run `toc example.js`, the program will output the following (stdout):

```js
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of example.js                                        │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Main section
// │  └──┐Nested section
// │     └──┐Nested section
// │        └──┐Nested section
// │           └── Nested section
// │
// └───────────────────────────────────────────────────────────────
```

## Embed the table of contents in the original file

If you want to output the toc we just saw to the file, you should run `toc -f example.js` and get (stderr):

```
Adding toc to file example.js
```

By opening "example.js", the file content will be:

<details>
 <summary>Click to view the original `example.js` with toc</summary>

```js
#!/usr/bin/env node

// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of example.js                                        │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Main section
// │  └──┐Nested section
// │     └──┐Nested section
// │        └──┐Nested section
// │           └── Nested section
// │
// └───────────────────────────────────────────────────────────────

// ################################################################ Main section

let Section1 = "Write //, 64 hash characters and the name of section"

// ################################ Nested section

let Section2 = "Write //, 32 hash characters and the name of section"

// ################ Nested section

let Section3 = "Write //, 16 hash characters and the name of section"

// ######## Nested section

let Section4 = "Write //, 8 hash characters and the name of section"

// #### Nested section

let Section5 = "Write //, 4 hash characters and the name of section"
```

</details>

Notice how `toc` recognized the shebang for `node` and added the table of contents after it.
If you run again `toc -f example.js`, it recognizes that there is no need to update the toc, as no changes have been made.

However, if you add new sections to the file and run again `toc -f example.js`, it will update the file accordingly:

```
Updating toc in file example.js
```

<details>
 <summary>Click to view the modified `example.js` with toc</summary>

```js
#!/usr/bin/env node

// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of example.js                                        │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Main section
// │  ├──┐New section
// │  │  └── Also New section
// │  ├──┐New section
// │  │  └── Also New section
// │  └──┐Nested section
// │     └──┐Nested section
// │        └──┐Nested section
// │           └── Nested section
// │
// └───────────────────────────────────────────────────────────────

// ################################################################ Main section

let Section_1 = "Write //, 64 hash characters and the name of section"

// ################################ New section

let Section_1_1 = "Write //, 32 hash characters and the name of section"

// ################ Also New section

let Section_1_1_1 = "Write //, 32 hash characters and the name of section"

// ################################ New section

let Section_1_1 = "Write //, 32 hash characters and the name of section"

// ################ Also New section

let Section_1_1_1 = "Write //, 32 hash characters and the name of section"

// ################################ Nested section

let Section_1_2 = "Write //, 32 hash characters and the name of section"

// ################ Nested section

let Section_1_2_3 = "Write //, 16 hash characters and the name of section"

// ######## Nested section

let Section_1_2_4 = "Write //, 8 hash characters and the name of section"

// #### Nested section

let Section_1_2_5 = "Write //, 4 hash characters and the name of section"
```

</details>

## Process multiple files

You can alternatively write the files you want to keep updated in a simple text list:

<details>
 <summary>Click to view `tocfiles.txt`</summary>

```python
# ignore-this-file.txt
README.md
USAGE.md
CHANGELOG.md
toc/cli.py
toc/toc.py
# glob expansion
tests/test*.py
```
</details>

To keep these files up-to-date, you just need to run `toc -l -f tocfiles.txt`:

```
Skipping replacing same toc in file "README.md"
Updating toc in file "USAGE.md"
Adding toc to file "CHANGELOG.md"
Updating toc in file "toc/cli.py"
Updating toc in file "toc/toc.py"
Skipping replacing same toc in file "tests/test_cli.py"
Skipping replacing same toc in file "tests/test_toc.py"
```

Note that more than one list can be passed in a single command, lines starting with "#" are ignored, and there is support for glob expansion.

If you feel brave enough, you can run `toc *` over your entire code base, as its AI[^2] will:

- skip directories
- skip non-text files
- skip non-existing files
- skip non-readable files
- skip non-writable files
- skip files that don't have suitable "section" comments
- skip files whose toc is already up-to-date
- only edit files whose toc can be added or updated safely[^3]
- preserve shebangs, markdown frontmatters and other declarations of edited files

## Show line numbers

For very long files, it may come in handy to run `toc -n example.js` to see the line number of each section, similar to the page numbers in the table of contents of a book:

```js
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of example.js                                        │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Main section 19
// │  ├──┐New section 23
// │  │  └── Also New section 27
// │  ├──┐New section 31
// │  │  └── Also New section 35
// │  └──┐Nested section 39
// │     └──┐Nested section 43
// │        └──┐Nested section 47
// │           └── Nested section 51
// │
// └───────────────────────────────────────────────────────────────
```

## Set a custom comment character

But how could `toc` recognize that `//` is the proper comment character for that file?
Well, thanks to AI[^1] `toc` supports most programming and markup languages, from COBOL to Carbon.
In case it doesn't work as expected, you can force the behavior by running `toc -c "//" example.xyz`.

## Redirect output to another file

For testing purposes, you can run `toc -o output.py input.py` to choose a different output file.

Note that this option does nothing if the toc in "input.py" is already up-to-date.

The `-o` flag is incompatible with the `-l` one.

## Other commands

You can run `toc -h` for usage info and `toc -v` to read the current version

## Exceptional file types
### No comments needed

#### Markdown

For Markdown files, you don't need to write comments, just organize your sections with one or more `#`:

    # Title
       
    ## Section

#### Beancount

For [Beancount](https://raw.githubusercontent.com/beancount/beancount/master/examples/example.beancount) files, it's the same for Markdown, but you use `*` instead:

<details>
 <summary>Click to view `example.beancount`</summary>

```ini
* Options

; comment

* Transactions
** FY2020

2020-04-20 * "Food"
 Assets:Bank                                          -20.00 EUR
 Expenses:Groceries
```

</details>

#### Perl

For Perl files, use the default [Pod](https://perldoc.perl.org/perlpod) heading style:

<details>
 <summary>Click to view `example.ml`</summary>

```pod
=pod
=encoding utf8

=head1 Title

=head2 Section

=for comment
Text

=cut
```

</details>


### Wrap around comments needed

These languages do not support single line comments, and thus every comment should be wrapped by a multi line comment separator

#### CSS

For CSS files, you have to wrap your `//` comments between `/*` and `*/`:

<details>
 <summary>Click to view `example.css`</summary>

```css
/*
// ################################################################ Landscape touchscreen
*/

@media (orientation: landscape) and (hover: none) and (pointer: coarse) {

/*
// ################################ Element selectors
*/

 body {
  background-color: blue;
 }

} /* end Landscape touchscreen */

```

</details>

#### HTML and Quarto

For HTML and Quarto files, you have to wrap your `//` comments between `<!--` and `-->`:

<details>
 <summary>Click to view `example.html`</summary>

```html
<!doctype html>
<html lang="en">

<!--
// ################################################################ Head
-->

 <head>
  <link rel="stylesheet" href="/assets/css/example.css"/>
  <script src="/assets/js/example.js"></script>
 </head>

<!--
// ################################################################ Body
-->

 <body>
  <h1>Title</h1>
 </body>
</html>
```

</details>

#### OCaml

For OCaml files, you have to wrap your `*` comments between `(*` and `*)`:

<details>
 <summary>Click to view `example.ml`</summary>

```ocaml
(*
* ################################################################ Unique section
*)

let () = print_endline "Hello, World!"
```

</details>


### Compatibility with third-party editors

#### Vim and Emacs

If you place your Vim Modeline / Emacs mode as the first line, the toc will be appended after


#### RStudio

If you are using RStudio, you may want to end your comments with at least 4 `-`, `=` or `#`.
This marks the comment as a foldable sections:

<details>
 <summary>Click to view `example.R`</summary>

```r
# ################################################################ Foldable section 1 ----

print("Collapse me!")

# ################################ Foldable section 2 ####

print("Collapse me!")

# ################################ Foldable section 3 ====

print("Collapse me!")
```

</details>





[^1]: No, not really, it's just a match-case statement using the file extension, defaulting to "#"
[^2]: Not even, it's just a bunch of if-else and try-excepts statement that may prevent catastrophic damage
[^3]: The outdated toc to be replaced is defined as the the first match of a non-greedy regex
