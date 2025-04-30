from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if not isinstance(value, str) or not value:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not isinstance(value, str) or not value:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        
        #generates opening tag
        opening_tag = f"<{tag}"
        
        #adds properties to tag (if there are any)
        for key, value in self.props.items():
            opening_tag += f" {key}=\"{value}\""
        opening_tag += ">"

        #returns final html string output
        return opening_tag + self.value + f"</{tag}>"