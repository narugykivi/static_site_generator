import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "link",
            "Boot.dev",
            None,
            { "href": "https://www.google.com", "target": "_blank",}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "Hello world!"
        )
        self.assertEqual(
            node.tag,
            "div"
        )
        self.assertEqual(
            node.value,
            "Hello world!"
            )
        self.assertEqual(
            node.children,
            None
            )
        self.assertEqual(
            node.props,
            None
            )

    def test_repr(self):
        node = HTMLNode(
            "link",
            "Boot.dev",
            None,
            {"href": "https://www.google.com", "target": "_blank",}
        )
        self.assertEqual(
            "HTMLNode(link, Boot.dev, children:None, {'href': 'https://www.google.com', 'target': '_blank'})",
            repr(node)
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")




if __name__ == "__main__":
    unittest.main()