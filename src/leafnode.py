from htmlnode import HTMLNode
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if not isinstance(self.value, str) or not self.value:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if not isinstance(self.value, str) or not self.value:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        
        #generates opening tag
        opening_tag = f"<{self.tag}"
        
        #adds properties to tag (if there are any)
        if self.props:
            for key, value in self.props.items():
                opening_tag += f" {key}=\"{value}\""
        
        opening_tag += ">"

        #returns final html string output
        return opening_tag + self.value + f"</{self.tag}>"