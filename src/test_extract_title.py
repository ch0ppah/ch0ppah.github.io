import unittest

from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_first_line(self):
        md = "# Good news!"
        self.assertEqual(extract_title(md), "Good news!")

    def test_extract_title_second_line(self):
        md = "Not the title\n# The title\n Again no"
        self.assertEqual(extract_title(md), "The title")

    def test_no_title(self):
        md = "No title here"
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "h1 header not found")

    def test_empty_title(self):
        md = "# "
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "h1 header is empty")

    def test_empty_title_extra_whitespace(self):
        md = "#     "
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "h1 header is empty")

    def test_h2_header(self):
        md = "## Subtitle"
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "h1 header not found")

    def test_leading_whitespace(self):
        md = " # Not accepted title"
        with self.assertRaises(Exception) as e:
            extract_title(md)
        self.assertEqual(str(e.exception), "h1 header not found")

if __name__ == "__main__":
    unittest.main()