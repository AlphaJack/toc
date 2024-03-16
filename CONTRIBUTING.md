<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CONTRIBUTING.md                                   │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Contributing
// │  ├── Suggestions
// │  ├── Contributions
// │  └──┐Tools
// │     ├── Type checking
// │     ├── Code linting
// │     ├── Test coverage
// │     ├── Virtual environment
// │     ├──┐Benchmarks
// │     │  ├── Large files
// │     │  └── Multiple files
// │     ├──┐Profiling
// │     │  ├── Function-level time
// │     │  ├── Line-level time
// │     │  └── Memory allocation
// │     ├── Launching without installing
// │     └── Release
// │
// └───────────────────────────────────────────────────────────────
-->

# Contributing

## Suggestions

If you have feedback, a suggestion or you simply found a bug, feel free to submit an [issue](https://github.com/AlphaJack/toc/issues).

## Contributions

If you would like to submit a [pull request](https://github.com/AlphaJack/toc/pulls), consider the following:

- do not sacrifice readability for performance, `toc` is already fast enough for its use case
- add comments to explain complex part of your function
- add a dedicate unit test if you implemented a new function
- make sure that all tests pass before committing
- contributions are licensed according to the open-source [LICENSE](./LICENSE)

## Tools

Here is a list of tools that you can use to improve code quality.

### Type checking

Assigning a specific type (str, list, etc.) to variables and function outputs makes the code less prone to errors.
Type checking ensures variables consistency and that functions are passed the expected type of input.

```bash
pip install mypy
mypy "toc/"
```

### Code linting

Linting checks the code conformity to the [PEP 8](https://peps.python.org/pep-0008/) (_pepotto_) style.

```bash
pip install black
black .
```

### Test coverage

A high test coverage checks more code against unexpected behaviors, i.e. bugs.

```bash
pip install coverage
coverage run -m unittest
coverage html
firefox "htmlcov/index.html"
```

### Virtual environment

Before running benchmarks, it is suggested to install `toc` in a virtual environment.
"(venv)" will be prepended to the shell prompt to indicate that every python/pip operation
is run in the "venv/" folder, without impacting the system.

```bash
python -m venv "venv/"
source venv/bin/activate
pip install -e .
```
### Benchmarks

Running the code against a heavy workload amplifies the effect of inefficient sections in profiling operations.

#### Large files

To generate a single large file (use `toc/cli.py tests/output/longfile.txt`):

```bash
rm -f tests/output/longfile.txt
for i in {1..100000}; do
 {
  printf "# ################################################################ Test H1 $i\n"
  printf "# ################################ Test H2 $i\n"
 } >> tests/output/longfile.txt
done
```

More complex toc:

```bash
rm -f tests/output/longfile-complex.txt
for i in {1..100000}; do
 {
  printf "# ################################################################ Test H1 $i\n"
  printf "# ################################ Test H2 $i\n"
  printf "# ################ Test H3 $i\n"
  printf "# ################ Test H3 $i\n"
  printf "# ################################ Test H2 $i\n"
 } >> tests/output/longfile-complex.txt
done
```

#### Multiple files

To generate multiple small files (use `toc/cli.py -l tests/output/multi/_list.txt`):

```bash
mkdir -p tests/output/multi
rm -f tests/output/multi/_list.txt
for i in {1..10000}; do
 file=tests/output/multi/$i.txt
 {
  printf "# ################################################################ Test H1 $i\n"
  printf "# ################################ Test H2 $i\n"
 } > $file
 printf "$file\n" >> tests/output/multi/_list.txt
done
```

More complex toc:

```bash
mkdir -p tests/output/multi
rm -f tests/output/multi/_list-complex.txt
for i in {1..10000}; do
 file=tests/output/multi/$i-complex.txt
 {
  printf "# ################################################################ Test H1 $i\n"
  printf "# ################################ Test H2 $i\n"
  printf "# ################ Test H3 $i\n"
  printf "# ################ Test H3 $i\n"
  printf "# ################################ Test H2 $i\n"
 } > $file
 printf "$file\n" >> tests/output/multi/_list-complex.txt
done
```

### Profiling

We can use a variety of profiling tools to understand the impact of functions on performance.
For these tools to work, one line needs to be modified in "cli.py":

```python
#from toc.toc import Toc
from toc import Toc
```

#### Function-level time

The built-in `cProfile` Python module allows for function-level profiling, which can be explored with `snakeviz`

```bash
pip install snakeviz
python -m cProfile -o "tests/output/prof_cprofile.prof" toc/cli.py "tests/output/longfile.txt"
snakeviz "tests/output/prof_cprofile.prof"
```
#### Line-level time

`pprofile` allows for line-level profiling, which can be explored with a "callgrind" reader like `qcachegrind`

```bash
pip install pprofile
pprofile --exclude-syspath -f callgrind -o "tests/output/prof_callgrind.prof" toc/cli.py "tests/output/longfile.txt"
qcachegrind "tests/output/prof_callgrind.prof"
```

#### Memory allocation

`memray` shows how much memory is allocated during code execution

```bash
pip install memray
memray run -o "tests/output/prof_memray.bin" toc/cli.py "tests/output/longfile.txt"
memray summary "tests/output/prof_memray.bin"
memray tree "tests/output/prof_memray.bin"
memray flamegraph "tests/output/prof_memray.bin"
firefox "tests/output/memray-flamegraph-prof_memray.html"
rm "tests/output/memray.bin" "tests/output/memray-flamegraph-prof_memray.html"
```

### Launching without installing

If you really need to launch `toc` without without installing it first, you can run

```bash
python -m toc.cli --version
python -m toc.cli -f "toc/toc.py"
```

### Release

Steps for a new release:

1. Update version in "pyproject.toml"
2. Save changes with `git commit`
3. Add a temporary tag with `git tag v2.6.0` and rewrite the tag name
4. Update the changelog with `git-cliff -c pyproject.toml > CHANGELOG.md`
5. Run `toc -lf .tocfiles`
6. Remove tag with `git tag --delete v2.6.0`
7. Add changelog changes with `git add CHANGELOG.md && git commit -m "minor: updated CHANGELOG.md"`
8. Move tag to the new commit with `git tag -fa  v2.6.0`
9. Upload the new commits and tags with `git push --follow-tags`
10. Update [AUR](https://aur.archlinux.org/packages/toc) version once the new [PyPI](https://pypi.org/project/tableofcontents/) version is online
