from blocks import markdown_to_blocks, block_to_block_type, BlockType

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
    pass