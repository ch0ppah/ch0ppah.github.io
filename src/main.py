from textnode import TextNode, TextType
from htmlnode import HTMLNode
def main():
    props = {
        "href": "https://www.google.com", 
        "target": "_blank"
     }

    node = HTMLNode("tag", "value", "children", props)
    print("EXPECTED:")
    print(" href=\"https://www.google.com\" target=\"_blank\"")
    print("PROPS TO HTML:")
    print(node.props_to_html())
    print()

main()