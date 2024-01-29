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
import io
import contextlib

# current directory
from pathlib import Path
# load local module rather than system installed version
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, project_root)

# module to test
from toc.toc import Toc
from toc.cli import main, parse_args

# ################################################################ TEST CLASSES

"""

# ################################ MOCK SETUP

class MockArgs():
    def __init__(self):
        self.from_list = False
        self.output_file = None
        self.files = ['empty.py']
        self.character = None
        self.line_numbers = False
        self.to_file = False

# ################################ CLI TESTS

class TestCli(unittest.TestCase):
    #@patch('builtins.open', new_callable=mock_open, read_data="test\n")
    @patch('toc.cli.parse_args')
    @patch('toc.toc.Toc')
    #def test_main(self, mock_toc, mock_args, mock_files):
    def test_nonexisting_file(self, mock_toc, mock_args):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            mock_args.return_value = MockArgs()
            #mock_toc.return_value = MockToc(mock_args.files)
            main()
            self.assertTrue(f'Skipping non-existing file empty.py' in f.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="test\n")
    @patch('toc.cli.parse_args')
    @patch('toc.toc.Toc')
    def test_empty_file(self, mock_toc, mock_args, mock_files):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            mock_args.return_value = MockArgs()
            main()
            # if main() has run without errors, this will pass
            #self.assertTrue(True)
            self.assertTrue(f'Skipping empty "#" toc for empty.py' in f.getvalue())

    def test_nonexisting_list(self):
        with patch("sys.argv", ["-l", "empty.list"]):
            #print(sys.argv)
            f = io.StringIO()
            with contextlib.redirect_stderr(f):
                args = parse_args()
                main()
                self.assertTrue(f'No files provided' in f.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data="test\n")
    @patch('toc.cli.parse_args')
    @patch('toc.toc.Toc')
    def test_empty_list(self):
        with patch("sys.argv", ["-l", "empty.list"]):
            #print(sys.argv)
            f = io.StringIO()
            with contextlib.redirect_stderr(f):
                mock_args.return_value = MockArgs()
                main()
                self.assertTrue(f'No files provided' in f.getvalue())
"""

# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    unittest.main()

