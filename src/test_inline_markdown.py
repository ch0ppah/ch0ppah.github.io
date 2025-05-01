import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_text(self):
        node = TextNode("normal text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "?", TextType.NORMAL)
        self.assertListEqual([TextNode("normal text", TextType.NORMAL)], new_nodes)

    def test_bold(self):
        node = TextNode("**bold** unbold", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" unbold", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_bold_multi(self):
        node = TextNode("**two** bold **words**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("two", TextType.BOLD),
                TextNode(" bold ", TextType.NORMAL),
                TextNode("words", TextType.BOLD),
            ],
            new_nodes
        )

    def test_italic(self):
        node = TextNode("_italic_ unitalic", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" unitalic", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_code(self):
        node = TextNode("`code` not", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode(" not", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_all(self):
        node = TextNode("**bold** `code` _italic_ normal", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" normal", TextType.NORMAL)
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()