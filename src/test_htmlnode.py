import unittest

from htmlnode import HTMLNode


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




if __name__ == "__main__":
    unittest.main()