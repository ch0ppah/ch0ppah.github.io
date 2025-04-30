import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank"
        }

        node = HTMLNode("tag", "value", "children", props)
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_unequal(self):
        props = {
            "href": "https://www.yahoo.com", 
            "target": "_blank"
        }
        node = HTMLNode("tag", "value", "children", props)
        expected = " href=\"https://www.google.com\" target=\"_blank"
        self.assertNotEqual(node.props_to_html(), expected)

    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("tag", "value", "children", "props")
        expected = "HTMLNode(tag, value, children, props)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()