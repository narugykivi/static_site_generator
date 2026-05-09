import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html(self):
        node = HTMLNode(
            "link",
            "Boot.dev",
            None,
            { "href": "https://www.google.com", "target": "_blank",}
        )
        with self.assertRaises(NotImplementedError) as cm:
            node.to_html()
        self.assertTrue("The 'to_html()' method is not implemented yet." in str(cm.exception))

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertTrue("All leaf nodes must have a value" in str(cm.exception))

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_whitout_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertTrue("HTMLParent missing a children attribute" in str(cm.exception))

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(Exception) as cm:
            parent_node.to_html()
        self.assertTrue("HTMLParent missing a tag attribute" in str(cm.exception))

    def test_to_html_with_props(self):
        grandchild_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com">Click me!</a></span></div>',
        )


if __name__ == "__main__":
    unittest.main()