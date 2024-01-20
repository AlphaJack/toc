import unittest
from toc import Toc

class Toc(unittest.TestCase):
    def setUp(self):
        self.t = Toc("testfile.tex", True)

    def test_get_extension(self):
        self.assertEqual(self.t.extension, "tex")

    def test_get_character(self):
        self.assertEqual(self.t.set_character(), "%%")



if __name__ == "__main__":
    unittest.main()
