import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(helper_func(node, delimiter, text_type))
    return new_nodes

def helper_func(node, delimiter, text_type):
    new_nodes = []
    #print(delimiter, type(node.text), node.text)
    split = node.text.split(delimiter)
    if (len(split) - 1) % 2 != 0:
        raise Exception(f"Invalid Markdown syntax: {len(split) - 1} delimeter found")
    for i in range(len(split)):
        if split[i] == "":
            continue
        if i % 2 == 0:
            new_nodes.append(TextNode(split[i], TextType.TEXT))
        else:
            new_nodes.append(TextNode(split[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        matches = extract_markdown_images(original_text)
        if node.text_type != TextType.TEXT or len(matches) == 0:
            new_nodes.append(node)
        else:
            for image_alt, image_link in matches:
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        matches = extract_markdown_links(original_text)
        if node.text_type != TextType.TEXT or len(matches) == 0:
            new_nodes.append(node)
        else:
            for link_anchor, link_url in matches:
                sections = original_text.split(f"[{link_anchor}]({link_url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
                if len(sections) == 2:
                    original_text = sections[1]
                else:
                    original_text = ""
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    empty = []
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
        if blocks[i] == "":
            empty.append(i)
    if len(empty) != 0:
        for i in sorted(empty).reverse():
            blocks.pop(i)
    return blocks