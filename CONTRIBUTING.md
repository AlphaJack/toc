<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CONTRIBUTING.md                                   │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Contributing
// │  ├── Suggestions
// │  └──┐Contributions
// │     └──┐Tools
// │        ├── Linting
// │        ├── Test coverage
// │        ├──┐Benchmarks
// │        │  ├── Large files
// │        │  └── Multiple files
// │        └── Profiling
// ├── install qcachegrind
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

### Tools

Here is a list of tools that you can use

#### Linting

Linting checks the code conformity to the [PEP 8](https://peps.python.org/pep-0008/) (_pepotto_) style.

Do not use `black` blindly as it will indent section comments.

```bash
pip install flake8
flake8 "toc/" --exit-zero --max-line-length=420 --statistics
flake8 "tests/" --exit-zero --max-line-length=420 --statistics
```

#### Test coverage

A high test coverage checks more code against unexpected behaviors, i.e. bugs

```bash
pip install coverage
coverage run -m unittest
coverage html
firefox "htmlcov/index.html"
```
#### Benchmarks

Running the code against a heavy workload amplifies the effect of unoptimized sections in profiling operations.

##### Large files

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
##### Multiple files

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

#### Profiling

We can use a variety of profiling tools to understand the impact of functions on performance.

The built-in `cProfile` Python module allows for function-level profiling, which can be explored with `snakeviz`

```bash
pip install snakeviz
python -m cProfile -o "tests/output/prof_cprofile.prof" toc/cli.py "tests/output/longfile.txt"
snakeviz "tests/output/prof_cprofile.prof"
```

`pprofile` allows for line-level profiling, which can be explored with a "callgrind" reader like `qcachegrind`

```bash
# install qcachegrind
pip install pprofile
pprofile --exclude-syspath -f callgrind -o "tests/output/prof_callgrind.prof" toc/cli.py "tests/output/longfile.txt"
qcachegrind "tests/output/prof_callgrind.prof"
```

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
