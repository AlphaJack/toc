#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of python_black.py                                   │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├──┐My class
# │  ├── INIT
# │  └──┐METHOD 1
# │     └── SET METHOD NAME
# │
# └───────────────────────────────────────────────────────────────

# this file has been formatted with black
# originally the comments were always at line beginning

# ################################################################ My class


class Class:
    # ################################ INIT

    def __init__(self) -> None:
        self.name = "Class"

    # ################################ METHOD 1

    def method_1(self) -> None:
        # ################ SET METHOD NAME
        self.method_name = 1
