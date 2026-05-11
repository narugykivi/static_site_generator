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