class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props = self.props or {}
        return "".join(f" {k}=\"{v}\"" for (k, v) in props.items())

    def __repr__(self):
        children = "".join(self.children or [])
        props = self.props_to_html().strip()
        inner = f"{self.tag}, \"{self.value}\""
        if children:
            inner = inner + ", " + children
        if props:
            inner = inner + ", " + props
        return f"HTMLNode({inner})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("no value")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("no tag")
        elif self.children == None:
            raise ValueError("no children")
        else:
            return f"<{self.tag}{self.props_to_html()}>{"".join(c.to_html() for c in self.children)}</{self.tag}>"
