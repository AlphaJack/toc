<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of README.md                                         │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐toc
// │  ├── What is it?
// │  ├── Why should I use it?
// │  ├── How does it work?
// │  ├── Are there exceptions?
// │  ├── How can I contribute?
// │  └──┐What changed from previous versions?
// │     ├── 2.0.0
// │     └── 1.0.0
// │
// └───────────────────────────────────────────────────────────────
-->

# toc

toc - Generate a table of contents from the comments of a file

![Example table of contents generated by toc](example-toc.png)

## What is it?

`toc` is a command line utility that generates the table of contents of a file from a special kind of comments.

Think it as a [`tree`](https://en.wikipedia.org/wiki/Tree_%28command%29) for the contents of a file, instead of a directory.

As a Python package, you can install it by running:

```bash
pip install tableofcontents
```

If you are using Arch or Manjaro Linux, you can install [toc](https://aur.archlinux.org/packages/toc) directly from the AUR.

## Why should I use it?

Few reasons that you may consider:

- it can make your files understandable in seconds, even if you haven't touched them for a while
- you can jump directly to the section you need to edit, because you know where it's located
- it makes you reflect about the structure of your file, making it more logical
- for software developers, it makes your code base more readable to others

## How does it work?

First, you have to write the comments representing the different sections of a file. Second, you run `toc` on that file to turn those comments into a table of contents.

Let's say you want to structure your javascript file "example.js".
Single line comments in this language start with "//".
You open your file and add these comments where you need them:

<details>
 <summary>example.js</summary>
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

</details>

If you run `toc example.js`, the program will output the following (stdout):

```
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of README.md                                         │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐toc
// │  ├── What is it?
// │  ├── Why should I use it?
// │  ├── How does it work?
// │  ├── Are there exceptions?
// │  ├── How can I contribute?
// │  └──┐What changed from previous versions?
// │     ├── 2.0.0
// │     └── 1.0.0
// │
// └───────────────────────────────────────────────────────────────
```

If you want to output the toc we just saw to the file, you should run `toc -f example.js` and get (stderr):

```
Adding toc to file example.js
```

By opening "example.js", the file content will be:

<details>
 <summary>example.js</summary>

```js
#!/usr/bin/env node

// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of README.md                                         │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐toc
// │  ├── What is it?
// │  ├── Why should I use it?
// │  ├── How does it work?
// │  ├── Are there exceptions?
// │  ├── How can I contribute?
// │  └──┐What changed from previous versions?
// │     ├── 2.0.0
// │     └── 1.0.0
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

However, if you add new sections to the file, it will update the file accordingly:

```
Updating toc in file example.js
```

<details>
 <summary>Modified example.js</summary>

```js
#!/usr/bin/env node

// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of README.md                                         │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐toc
// │  ├── What is it?
// │  ├── Why should I use it?
// │  ├── How does it work?
// │  ├── Are there exceptions?
// │  ├── How can I contribute?
// │  └──┐What changed from previous versions?
// │     ├── 2.0.0
// │     └── 1.0.0
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

But how could `toc` recognize that "//" is the proper comment character for that file?
Well, thanks to AI[^1] `toc` supports most programming and markup languages, including FORTRAN and Zig.
In case it doesn't work as expected, you can force the behavior by running `toc -c "//" example.xyz`.

For very long files, it may come in handy to run `toc -n example.js` to see the line number of each section, similar to the page numbers in the table of contents of a book:

```
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of README.md                                         │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐toc
// │  ├── What is it?
// │  ├── Why should I use it?
// │  ├── How does it work?
// │  ├── Are there exceptions?
// │  ├── How can I contribute?
// │  └──┐What changed from previous versions?
// │     ├── 2.0.0
// │     └── 1.0.0
// │
// └───────────────────────────────────────────────────────────────
```

If you feel brave enough, you can run `toc` over your entire code base, as its AI[^2] will make it:

- skip directories (`.` below)
- skip non-text files (`toc.cpython-311.pyc` below)
- skip non-existing files
- skip non-readable files
- skip non-writable files
- skip files that don't have suitable "section" comments (`__init__.py` below)
- skip files whose toc is already up-to-date (`toc.py` below)

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

## Are there exceptions?

For Markdown files, you don't need to write comments, just organize your sections with one or more "#".

For [Beancount](https://raw.githubusercontent.com/beancount/beancount/master/examples/example.beancount) files, it's the same for Markdown, but you use "*" instead.

For CSS files, you have to wrap your "//" comments between `/*` and `*/`:

<details>
 <summary>example.css</summary>

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

For HTML files, you have to wrap your "//" comments between `<!--` and `-->`:

<details>
 <summary>example.html</summary>

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


## How can I contribute?

If you have a suggestion or you found an issue, you can use GitHub issues and pull requests to contribute. 

## What changed from previous versions?

### 2.0.0

- rewritten in pure `python`
- published to PyPI as `tableofcontents`
- added feature to prepend the table of contents to files, preserving shebangs

### 1.0.0

- initial release of `toc` in `bash`, `perl`, `sed` and `awk`

---

[1]: No, not really, it's just a match-case statement using the file extension, defaulting to "#"
[2]: Not even, it's just a bunch of if-else and try-excepts statement that may prevent catastrophic damages
