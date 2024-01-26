# Detailed TOC usage

The scenarios below show different features.

- [Detailed TOC usage](#detailed-toc-usage)
   - [Read the table of contents](#read-the-table-of-contents)
   - [Embed the table of contents in the original file](#embed-the-table-of-contents-in-the-original-file)
   - [Set a custom comment character](#set-a-custom-comment-character)
   - [Show line numbers](#show-line-numbers)
   - [Process multiple files](#process-multiple-files)
   - [Exceptional file types](#exceptional-file-types)
      - [Markdown](#markdown)
      - [Beancount](#beancount)
      - [CSS](#css)
      - [HTML](#html)
      - [OCaml](#ocaml)

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
// │ Contents of USAGE.md                                          │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Detailed TOC usage
// │  ├── Read the table of contents
// │  ├── Embed the table of contents in the original file
// │  ├── Set a custom comment character
// │  ├── Show line numbers
// │  ├── Process multiple files
// │  └──┐Exceptional file types
// │     ├── Markdown
// │     ├── Beancount
// │     ├── CSS
// │     ├── HTML
// │     └── OCaml
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

## Set a custom comment character

But how could `toc` recognize that `//` is the proper comment character for that file?
Well, thanks to AI[^1] `toc` supports most programming and markup languages, from COBOL to Carbon.
In case it doesn't work as expected, you can force the behavior by running `toc -c "//" example.xyz`.

## Show line numbers

For very long files, it may come in handy to run `toc -n example.js` to see the line number of each section, similar to the page numbers in the table of contents of a book:

```
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

## Process multiple files

If you feel brave enough, you can run `toc` over your entire code base, as its AI[^2] will make it:

- skip directories (see `.` below)
- skip non-text files (see `toc.cpython-311.pyc` below)
- skip non-existing files
- skip non-readable files
- skip non-writable files
- skip files that don't have suitable "section" comments (see `__init__.py` below)
- skip files whose toc is already up-to-date (see `toc.py` below)
- only edit files whose toc can be added or updated safely[^3] (see `cli.py` below)
- preserve shebangs of edited files

```
Skipping directory .
Skipping empty "#" toc for ./__init__.py
Skipping directory ./__pycache__
Skipping binary file ./__pycache__/toc.cpython-311.pyc
Skipping replacing same toc in file ./toc.py
Updating toc in file ./cli.py
Skipping replacing same toc in file ./example.js
```

Additionally, you can run `toc -h` for usage info and `toc -v` to read the current version

## Exceptional file types
### No comments needed

#### Markdown

For Markdown files, you don't need to write comments, just organize your sections with one or more `#`:

   # Title
   
   ## Section

#### Beancount

For [Beancount](https://raw.githubusercontent.com/beancount/beancount/master/examples/example.beancount) files, it's the same for Markdown, but you use `*` instead:

```beancount
* Options

; text

* Transactions
** FY2020

; text
```

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

#### HTML

For HTML files, you have to wrap your `//` comments between `<!--` and `-->`:

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
