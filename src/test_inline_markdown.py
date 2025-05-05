import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-diamond-version/5/5e/Natu.jpg)"
        )
        self.assertListEqual([("image", "https://oyster.ignimgs.com/mediawiki/apis.ign.com/pokemon-diamond-version/5/5e/Natu.jpg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://www.youtube.com/)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://www.youtube.com/")
            ],
            matches,
        )

if __name__ == "__main__":
    unittest.main()