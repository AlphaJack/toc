#!/usr/bin/env python

# ┌───────────────────────────────────────────────────────────────┐
# │ Contents of test_toc.py                                       │
# ├───────────────────────────────────────────────────────────────┘
# │
# ├── MODULES
# ├──┐TEST CLASSES
# │  ├── SINGLE METHODS
# │  └── FILE PROCESSING
# ├── ENTRYPOINT
# │
# └───────────────────────────────────────────────────────────────

# ################################################################ MODULES

# test
import unittest
# clean output path if existing
import shutil

# current directory
from pathlib import Path

# load local module rather than system installed version
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, project_root)

# module to test
from toc.toc import Toc

# ################################################################ TEST CLASSES
# ################################ SINGLE METHODS


# example test
class TestTocMethods(unittest.TestCase):
    def test_set_extension(self):
        test_cases = [
            ("file.c", "c"),
            ("file.ini", "ini"),
            (".", ""),
            ("./../", "/"),
            ("file.unknown", "unknown"),
            ("file.", ""),
        ]
        for input_file, expected_extension in test_cases:
            with self.subTest(input_file=input_file, expected_extension=expected_extension):
                t = Toc(input_file)
                actual_extension = t.extension
                self.assertEqual(actual_extension, expected_extension, f'Unexpected extension "{actual_extension}" for file "{input_file}"')

    def test_set_character(self):
        test_cases = [
            ("file.c", "//"),
            ("file.ini", ";"),
            ("file.tex", "%"),
            ("file.sql", "--"),
            ("file.unknown", "#"),
            ("file.", "#"),
            ("file", "#"),
        ]
        for input_file, expected_character in test_cases:
            with self.subTest(input_file=input_file, expected_character=expected_character):
                t = Toc(input_file)
                actual_character = t.set_character()
                self.assertEqual(actual_character, expected_character, f'Unexpected comment character "{actual_character}" for file "{input_file}"')


# ################################ FILE PROCESSING


class TestTocFiles(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.t = project_root / "tests"
        # project folder
        cls.p = cls.t.parent
        cls.input_dir = cls.t / "input"
        cls.output_dir = cls.t / "output"
        cls.reference_dir = cls.t / "reference"
        try:
            shutil.rmtree(cls.output_dir)
        except OSError:
            pass
        Path.mkdir(cls.output_dir, parents=True, exist_ok=True)

    def test_all_files(self):
        # process each file in the input_dir
        for file in Path.iterdir(self.input_dir):
            print(f"\nProcessing {file.name}")
            input_file = self.input_dir / file.name
            output_file = self.output_dir / file.name
            reference_file = self.reference_dir / file.name
            # print("input_file: " + str(input_file))
            # print("output_file: " + str(output_file))
            # print("reference_file: " + str(reference_file))
            t = Toc(input_file)
            t.set_character()
            t.lineNumbers = True if file.name == "latex_linenumbers.tex" else False
            t.to_file(output_file)
            if output_file.is_file() and reference_file.is_file():
                with open(output_file, "r") as output, open(reference_file, "r") as reference:
                    output_content, reference_content = output.read(), reference.read()
                    comparison = True if output_content == reference_content else False
                    with self.subTest(comparison=comparison):
                        self.assertTrue(comparison, f'Unexpected output processing "{file.name}", please check "{self.output_dir}"')
            elif reference_file.is_file():
                comparison = False
                with self.subTest(comparison=comparison):
                    self.assertTrue(comparison, f'Unexpected empty output processing "{file.name}", please check "{self.output_dir}"')
            else:
                comparison = True
                with self.subTest(comparison=comparison):
                    self.assertTrue(comparison, f'Expected empty output processing "{file.name}"')

    # @classmethod
    # def tearDownClass(cls):
    #     try:
    #         Path.rmdir(cls.output_dir)
    #     except OSError:
    #         pass


# ################################################################ ENTRYPOINT

if __name__ == "__main__":
    unittest.main()
