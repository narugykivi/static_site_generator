import os

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        #print(type)
        if type == BlockType.HEADING:
            syntax, text = block.split(" ", 1)
            if syntax == "#":
                return text.strip()
    raise Exception("There is no 'h1' header in the markdown text")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    html_template = None
    raw_markdown = None
    with open(from_path, 'r', encoding="utf-8") as f:
        raw_markdown = f.read()
    with open(template_path, 'r', encoding="utf-8") as f:
        html_template = f.read()
    content = markdown_to_html_node(raw_markdown).to_html()
    title = extract_title(raw_markdown)
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", content)
    print(content, "\n", title, "\n", html_template)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(dest_path)
    with open(dest_path, "w") as f:
        f.write(html_template)
