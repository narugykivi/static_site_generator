import unittest

from blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node
)

class TestSplitBlocks(unittest.TestCase):
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
    
    def test_quote_block(self):
        md = """
> This is some
>quote text
>          with some extra whitespace
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is some quote text with some extra whitespace</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_all_in_one(self):
        md = '''
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            '''<div><h1>Tolkien Fan Club</h1><p><img src="/images/tolkien.png" alt="JRR Tolkien sitting"></img></p><p>Here's the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here's what <code>elflang</code> looks like (the perfect coding language):</p><pre><code>func main(){
    fmt.Println("Aiya, Ambar!")
}
</code></pre><p>Want to get in touch? <a href="/contact">Contact me here</a>.</p><p>This site was generated with a custom-built <a href="https://www.boot.dev/courses/build-static-site-generator-python">static site generator</a> from the course on <a href="https://www.boot.dev">Boot.dev</a>.</p></div>''',
        )


if __name__ == "__main__":
    unittest.main()