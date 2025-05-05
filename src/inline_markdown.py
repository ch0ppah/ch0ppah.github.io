from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        split_nodes = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError("invalid markdown, unmatched closing delimiter")
        for i in range (len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splits[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(splits[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches