import unittest
from toc.toc import Toc

class TestToc(unittest.TestCase):
    def test_set_character(self):
        test_cases = [
            ("file.c", "//"),
            ("file.ini", ";"),
            ("file.tex", "%"),
            ("file.sql", "--"),
            ("file.unknown", "#"),
        ]

        for file, expected_character in test_cases:
            with self.subTest(file=file, expected_character=expected_character):
                toc = Toc(file=file)
                character = toc.set_character()
                self.assertEqual(character, expected_character)

if __name__ == "__main__":
    unittest.main()
