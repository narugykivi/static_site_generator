import re
from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

__heading_regex = r"(^#{1,6} )"
__ord_list_regex = r"(^\d\. )"
__unord_list_regex = r"(^- )"
__quote_regex = r"(^>)"
__code_regex = r"(^```\n[\s\S]*?```)"
__regex_flags = re.RegexFlag.MULTILINE

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    empty = []
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == "":
            empty.append(i)
    if len(empty) != 0:
        sorted_empty = sorted(empty, reverse=True)
        #print(type(empty), empty, type(sorted_empty), sorted_empty, blocks)
        for i in sorted_empty:
            blocks.pop(i)
    return blocks

def block_to_block_type(block):
    leading_chars, rest_of_the_text = block.split(" ", 1)
    lines = block.split("/n")
    if leading_chars in "######" and rest_of_the_text != "":
        return BlockType.HEADING
    #print("Not heading:", leading_chars)
    if [] != re.findall(__code_regex, block, __regex_flags):
        return BlockType.CODE
    #print("Not code:", leading_chars, rest_of_the_text[-3:])
    is_quote = True
    is_unord = True
    is_ord = True
    for line in lines:
        if line[0] != ">":
            #print("Not quote:", line)
            is_quote = False
        if line[0:2] != "- ":
            #print("Not unordered list:", line, "First two char:", line[:2])
            is_unord = False
        if [] == re.findall(__ord_list_regex, line):
            #print("Not ordered list:", line)
            is_ord = False
    #print("Is quote?", is_quote)
    #print("Is unordered list?", is_unord)
    #print("Is ordered list?", is_ord)
    if is_quote:
        return BlockType.QUOTE
    if is_unord:
        return BlockType.UNORDERED_LIST
    if is_ord:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        html_nodes.append(node)

    #print("This is i looking for:", html_nodes)
    result = ParentNode("div", html_nodes)
    #print("This is the result:\n", result.to_html(), "\n")
    return result

def block_to_html_node(block, block_type):
    match(block_type):
        case BlockType.QUOTE:
            lines = block.split("\n")
            edited_lines = []
            for line in lines:
                line = line.replace(">", "")
                line = line.strip()
                if line == "":
                    continue
                edited_lines.append(line)
            text = " ".join(edited_lines)
            return ParentNode("blockquote", text_to_children(text))
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                line = line.replace("-", "")
                line = line.strip()
                children.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children = []
            for line in lines:
                line = line[2:]
                line = line.strip()
                children.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ol", children)
        case BlockType.CODE:
            return ParentNode("pre", [text_node_to_html_node(TextNode(block[4:-3], TextType.CODE))])
        case BlockType.HEADING:
            heading, text = block.split(" ", 1)
            return ParentNode(f"h{len(heading)}", text_to_children(text))
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            return ParentNode("p", text_to_children(text))
        case _:
            raise ValueError("Block type is not correct:", block_type)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
