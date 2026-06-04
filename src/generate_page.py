import os

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType
from clean_copy import get_files

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        #print(type)
        if type == BlockType.HEADING:
            syntax, text = block.split(" ", 1)
            if syntax == "#":
                return text.strip()
    raise Exception("There is no 'h1' header in the markdown text:")

def generate_page(from_path, template_path, dest_path, basepath):
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
    html_template = html_template.replace('href="/', f'href="{basepath}')
    html_template = html_template.replace('src="/', f'src="{basepath}')
    #print(content, "\n", title, "\n", html_template)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(html_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    #print(dir_path_content)
    files, x = get_files(os.path.abspath(dir_path_content), [], [])
    for file in files:
        relative_path = os.path.relpath(file, start="content")
        dir_name = os.path.dirname(relative_path)
        file_name = file.split("/")[-1].replace(".md", ".html")
        dest_path = os.path.join(dest_dir_path, dir_name, file_name)
        #print(dir_name, ":", file_name, "->", dest_path)
        generate_page(file, template_path, dest_path, basepath)
    pass