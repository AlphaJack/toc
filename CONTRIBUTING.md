<!--
// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of CONTRIBUTING.md                                   │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Contributing
// │  ├──┐Test
// │  │  └── Test coverage
// │  └──┐Performance
// │     ├── 
// │     ├── Function level
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

### 

To generate a single large file:

```bash
for i in {1..10000}; do printf "# ################ Test Heading $i\n" >> "tests/output/longfile.txt"; done
```

To generate multiple small files:

```bash
mkdir -p "tests/output/multi"
rm -f "tests/output/multi/_list.txt"
for i in {1..10000}; do
 printf "# ################ Test Heading $i\n" > "tests/output/multi/$i.txt"
 printf "tests/output/multi/$i.txt\n" >> "tests/output/multi/_list.txt"
done
```


### Function level


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
