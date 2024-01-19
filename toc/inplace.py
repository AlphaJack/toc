# inplace.py
import re

file = "source.txt"

c = "#" 

newtoc = """# ┌───────────────────────────────────────────────────────────────┐
# │ NEW CONTENTS OF toc.py                                        │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐CLASS
# │  └──┐TOC GENERATION
# │     ├──┐BODY
# │     │  └── MARKDOWN TYPE
# │     └── FOOTER
# │
# └───────────────────────────────────────────────────────────────"""

c = "#"

begin = "BEGIN"
begin =  "^# ┌───────────────────────────────────────────────────────────────┐"
begin = f"{c} ┌───────────────────────────────────────────────────────────────┐"

end = "END"
end = f"{c} └───────────────────────────────────────────────────────────────"

source = """
#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ OLD CONTENTS OF toc.py                                        │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── LIBRARIES
# ├──┐CLASS
# │  ├── EVALUATORS
# │  └──┐TOC GENERATION
# │     ├── HEADER
# │     ├──┐BODY
# │     │  ├── MARKDOWN TYPE
# │     │  ├── OTHER TYPES
# │     │  └── PRETTIFY OUTPUT
# │     └── FOOTER
# │
# └───────────────────────────────────────────────────────────────

"""

#print(source)

new = re.sub('%s(.*?)%s' % (begin, end), newtoc, source, flags=re.DOTALL)
#print(new)

lineNumbers = True
updateToc = True

def add_or_update_toc():
    with open(file) as f:
        data = f.read()
        # https://stackoverflow.com/a/52921874/13448666
        if re.search(r'^%s$' % begin, data, re.M):
            print("updating existing toc")
            update_toc()
        else:
            print("adding new toc")
            add_toc()

def update_toc():
    data = replace_multiline_multipattern()
    write_newtoc(data)

def replace_multiline_multipattern():
    with open(file) as f:
        data = f.read()
        data = re.sub('%s(.*?)%s' % (begin, end), newtoc, data, flags=re.DOTALL)
        return data

def add_toc():
    data = add_toc_after_shebang()
    write_newtoc(data)

def add_toc_after_shebang():
    with open(file) as f:
        # if shebang is found, append after first line
        data = f.read()
        firstline = data.split("\n", 1)[0]
        if re.search(r'^#!/usr', firstline):
            print("adding toc after shebang")
            newheading = firstline + "\n\n" + newtoc
        # else prepend as first line and put everything else after
        else:
            print("adding toc before content")
            newheading = newtoc + "\n\n" + firstline
        #print(newheading)
        data = re.sub(firstline, newheading, data, flags=re.DOTALL)
        return data

def write_newtoc(data):
    with open(file, "w") as f:
        f.write(data)

if updateToc:
    if lineNumbers:
        # run twice because updating the toc may shift everything down
        print("using line numbers")
        for i in range(2):
            add_or_update_toc()
    else:
        add_or_update_toc()
