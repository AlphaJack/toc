#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of test_cli.py                                       │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── MODULES
# ├──┐TEST CLASSES
# │  ├── MOCK SETUP
# │  └── CLI TESTS
# ├── ENTRYPOINT
# │
# └───────────────────────────────────────────────────────────────

# ################################################################ MODULES

# test
import unittest

# mimic file opening
from unittest.mock import patch, mock_open

# capture stderr to variable
# https://stackoverflow.com/a/61533524/13448666
from io import StringIO
from contextlib import redirect_stderr
from contextlib import redirect_stdout


# current directory
from pathlib import Path
# load local module rather than system installed version
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, project_root)

# module to test
#from toc.toc import Toc
from toc.toc import Toc
from toc.cli import *
#from toc.__version__ import __version__

# ################################################################ TEST CLASSES

# ################################ MOCK SETUP

#class MockArgs():
#    def __init__(self):
#        self.from_list = False
#        self.output_file = None
#        self.files = ['empty.py']
#        self.character = None
#        self.line_numbers = False
#        self.to_file = False


# ################################ CLI TESTS


class TestCli(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.t = project_root / "tests"
        # project folder
        cls.p = cls.t.parent
        cls.i = cls.t / "input"
        cls.o = cls.t / "output"

    def test_no_args(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}"]
        with patch.object(sys, "argv", test_args):
            output = StringIO()
            with redirect_stderr(output):
                main()
                # print("output: '" + output.getvalue().strip() + "'")
                self.assertEqual("No files provided\n", output.getvalue())

    # returns SystemExit: 0 from argparse module with "-v"
    # def test_version(self):
    #    test_args = ["toc/cli.py", "-v"]
    #    with patch.object(sys, "argv", test_args):
    #        output = StringIO()
    #        with redirect_stdout(output):
    #            main()
    #            print("output: '" + output.getvalue().strip() + "'")
    #            self.assertTrue(f'toc {__version__}' in output.getvalue())

    # fails if not project root
    def test_empty(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}", f"{self.i / 'go_empty.go'}"]
        with patch.object(sys, "argv", test_args):
            output = StringIO()
            with redirect_stderr(output):
                main()
                # print("output: '" + output.getvalue().strip() + "'")
                self.assertIn('Could not generate a "//" toc for "', output.getvalue())

    def test_list(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}", "-l", f"{self.p / '.tocfiles'}"]
        with patch.object(sys, "argv", test_args):
            output = StringIO()
            with redirect_stdout(output):
                main()
                # print("output: '" + output.getvalue() + "'")
                self.assertTrue("Contents of README.md" in output.getvalue() and "Contents of USAGE.md" in output.getvalue())

    def test_stdin(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}", "-e", "html", "-"]
        stdin_content = """
<html>
<html>
<h1>Title</h1>
<h2>Subtitle</h2>
</html>
"""
        with patch('sys.stdin', StringIO(stdin_content)):
            with patch.object(sys, "argv", test_args):
                output = StringIO()
                with redirect_stdout(output):
                    main()
                    print("output: '" + output.getvalue() + "'")
                    self.assertIn("Contents of stdin.html", output.getvalue())

    def test_output(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}", "-o", f"{self.o / 'output.txt'}", f"{self.p / 'README.md'}"]
        with patch.object(sys, "argv", test_args):
            main()
            with open(f"{self.p / 'README.md'}", "r") as f:
                output_content = f.read()
            # print("output: '" + output_content)
            self.assertIn('Contents of README.md', output_content)

# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    unittest.main(buffer=True)
