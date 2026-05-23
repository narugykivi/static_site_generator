import unittest

from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")


    def test_extract_title_error(self):
        md = "Hello"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertTrue("There is no 'h1' header" in str(cm.exception))
        
    def test_extract_title_error2(self):
        md = "## Hello"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertTrue("There is no 'h1' header" in str(cm.exception))

if __name__ == "__main__":
    unittest.main()