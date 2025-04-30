from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        props_str =""
        for key, value in self.props.items():
            props_str += f" {key}=\"{value}\""

        return props_str
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("LeafNode must have a value")

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if self.children is None:
            raise ValueError("ParentNode must havechildren")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextType not in enum")