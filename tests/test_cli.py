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
        #cls.o = cls.t / "output"

    def test_no_args(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}"]
        with patch.object(sys, "argv", test_args):
            output = StringIO()
            with redirect_stderr(output):
                main()
                print("output: '" + output.getvalue().strip() + "'")
                self.assertEqual("No files provided\n", output.getvalue())

    # returns SystemExit: 0 from argparse module with "-v"
    #def test_version(self):
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
                #print("output: '" + output.getvalue().strip() + "'")
                self.assertIn('No "//" toc for "', output.getvalue())

    def test_list(self):
        test_args = [f"{self.p / 'toc' / 'cli.py'}", "-l", f"{self.p / '.tocfiles'}"]
        with patch.object(sys, "argv", test_args):
            output = StringIO()
            with redirect_stdout(output):
                main()
                #print("output: '" + output.getvalue() + "'")
                self.assertIn("Contents of README.md", output.getvalue())

"""
    #@patch('builtins.open', new_callable=mock_open, read_data="test\n")
    @patch('toc.cli.parse_args')
    @patch('toc.toc.Toc')
    #def test_main(self, mock_toc, mock_args, mock_files):
    def test_nonexisting_file(self, mock_toc, mock_args):
        f = StringIO()
        with redirect_stderr(f):
            mock_args.return_value = MockArgs()
            #mock_toc.return_value = MockToc(mock_args.files)
            main()
            self.assertTrue(f'Skipping non-existing file empty.py' in f.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="test\n")
    @patch('toc.cli.parse_args')
    @patch('toc.toc.Toc')
    def test_empty_file(self, mock_toc, mock_args, mock_files):
        f = StringIO()
        with redirect_stderr(f):
            mock_args.return_value = MockArgs()
            main()
            print(f.getvalue())
            # if main() has run without errors, this will pass
            #self.assertTrue(True)
            self.assertTrue(f'Skipping empty "#" toc for empty.py' in f.getvalue())

    def test_nonexisting_list(self):
        with patch("sys.argv", ["-l", "empty.list"]):
            #print(sys.argv)
            f = StringIO()
            with contextlib.redirect_stderr(f):
                args = parse_args()
                main()
                self.assertTrue(f'No files provided' in f.getvalue())

    #@patch('builtins.open', new_callable=mock_open, read_data="test\n")
    #@patch('toc.cli.parse_args')
    #@patch('toc.toc.Toc')
    #def test_empty_list(self):
    #    with patch("sys.argv", ["-l", "empty.list"]):
    #        #print(sys.argv)
    #        f = StringIO()
    #        with contextlib.redirect_stderr(f):
    #            mock_args.return_value = MockArgs()
    #            main()
    #            self.assertTrue(f'No files provided' in f.getvalue())

"""
# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    unittest.main(buffer=True)
