<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CONTRIBUTING.md                                   │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Contributing
// │  ├──┐Test
// │  │  └── Test coverage
// │  └──┐Performance
// │     ├── Function level
// ├── to generate a 10MB file
// ├── to cleanup
// │     ├── Line level
// │     └── Memory allocation
// │
// └───────────────────────────────────────────────────────────────
-->

# Contributing

## Test


### Test coverage


```bash
coverage run -m unittest
coverage html
firefox "htmlcov/index.html"
```

## Performance

### Function level

```bash
# to generate a 10MB file
for i in {1..312500}; do echo "# ################ Test Heading" >> "tests/output/longfile.txt"; done
# to cleanup
rm "tests/output/longfile.txt"
```

```bash
python -m cProfile -o "tests/output/prof_cprofile.prof" toc/cli.py # normal toc flags
snakeviz "tests/output/prof_cprofile.prof"
```

### Line level

```bash
pprofile --exclude-syspath -f callgrind -o "tests/output/callgrind.prof" toc/cli.py # normal toc flags
qcachegrind "tests/output/prof_callgrind.prof"
```

### Memory allocation

```bash
memray run -o "tests/output/memray.bin" toc/cli.py # normal toc flags
memray flamegraph "tests/output/memray.bin"
firefox "tests/output/memray-flamegraph-memray.html"
rm "tests/output/memray.bin" "tests/output/memray-flamegraph-memray.html"
```
