class HTMLNode():
    def __init__(self, tag=None, value=None, children= None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("The 'to_html()' method is not implemented yet.")
    
    def props_to_html(self):
        attributes = ""
        for attribute in self.props:
            attributes += f" {attribute}=\"{self.props[attribute]}\""
        return attributes
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children:{self.children}, {self.props})"
node = HTMLNode(
            "link",
            "Boot.dev",
            None,
            { "href": "https://www.google.com", "target": "_blank",}
        )   
print(node)