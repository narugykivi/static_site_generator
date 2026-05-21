import unittest

from inline_markdown import(
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )




class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_invalid_syntax(self):
        node = TextNode("This is text with a **bold word", TextType.TEXT)
        expected = "Invalid Markdown syntax:"
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue(expected in str(cm.exception))

class TestExtractMarkdownWithRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_images_with_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_link_single(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_markdown_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_text_nodes_syntax_error(self):
        text = "This is **text* with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = "Invalid Markdown syntax:"
        with self.assertRaises(Exception) as cm:
            text_to_textnodes(text)
        self.assertTrue(expected in str(cm.exception))

    def test_markdown_to_text_nodes_without_markdown(self):
        text = "This is text without an italic word and a code block and an obi wan image and a link"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text without an italic word and a code block and an obi wan image and a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_more_whitespace(self):
        md = """
         This is **bolded** paragraph              

       This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line                     

          - This is a list
- with items      
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockTypes(unittest.TestCase):
    def test_paragraph(self):
        paragraph = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        result = block_to_block_type(paragraph)
        expected = BlockType.PARAGRAPH
        self.assertEqual(result, expected)

    def test_heading(self):
        heading1 = "# This is a heading"
        heading2 = "## This is a heading"
        heading3 = "### This is a heading"
        heading4 = "#### This is a heading"
        heading5 = "##### This is a heading"
        heading6 = "###### This is a heading"
        not_heading = "####### This is a heading"
        result1 = block_to_block_type(heading1)
        result2 = block_to_block_type(heading2)
        result3 = block_to_block_type(heading3)
        result4 = block_to_block_type(heading4)
        result5 = block_to_block_type(heading5)
        result6 = block_to_block_type(heading6)
        result7 = block_to_block_type(not_heading)
        expected1 = BlockType.HEADING
        expected2 = BlockType.PARAGRAPH
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected1)
        self.assertEqual(result3, expected1)
        self.assertEqual(result4, expected1)
        self.assertEqual(result5, expected1)
        self.assertEqual(result6, expected1)
        self.assertNotEqual(result7, expected1)
        self.assertEqual(result7, expected2)

    def test_code(self):
        code1 = "```\nThis is a code block\n```"
        code2 = "```\nThis is a code block\nWith multiple lines\n```"
        result1 = block_to_block_type(code1)
        result2 = block_to_block_type(code2)
        expected = BlockType.CODE
        self.assertEqual(result1, expected)
        self.assertEqual(result2, expected)

    def test_quote(self):
        quote1 = ">This is a quote"
        quote2 = ">This is a quote\n> This is a quote too"
        result1 = block_to_block_type(quote1)
        result2 = block_to_block_type(quote2)
        expected = BlockType.QUOTE
        self.assertEqual(result1, expected)
        self.assertEqual(result2, expected)

    def test_unord_list(self):
        unord_list1 = "- This is the first list item in a list block"
        unord_list2 = "- This is the first list item in a list block\n- This is a list item"
        unord_list3 = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        result1 = block_to_block_type(unord_list1)
        result2 = block_to_block_type(unord_list2)
        result3 = block_to_block_type(unord_list3)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(result1, expected)
        self.assertEqual(result2, expected)
        self.assertEqual(result3, expected)

    def test_ord_list(self):
        ord_list1 = "1. This is an ordered list item in the list block"
        ord_list2 = "1. This is an ordered list item in the list block\n2. This is a second item"
        result1 = block_to_block_type(ord_list1)
        result2 = block_to_block_type(ord_list2)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(result1, expected)
        self.assertEqual(result2, expected)

class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()