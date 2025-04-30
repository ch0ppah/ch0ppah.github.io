import unittest

from htmlnode import HTMLNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
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

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_image(self):
        node = TextNode("this is an image node", TextType.IMAGE, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com", "alt": "this is an image node"})


if __name__ == "__main__":
    unittest.main()