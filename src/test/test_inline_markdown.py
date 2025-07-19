import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "A **bold phrase** followed by _italics_ and `some code` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("A ", TextType.NORMAL),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" followed by ", TextType.NORMAL),
                TextNode("italics", TextType.ITALIC),
                TextNode(" and ", TextType.NORMAL),
                TextNode("some code", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()