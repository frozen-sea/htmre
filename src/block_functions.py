import re

from blocktype import BlockType

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block:
            blocks.append(block)
    return blocks

def starts_with(needle, haystack):
    l = len(needle)
    if l > len(haystack):
        return False
    return haystack[:l] == needle

def block_to_block_type(markdown):
    heading_pattern = r"^#{1,6} "
    if re.match(heading_pattern, markdown):
        return BlockType.HEADING

    code_pattern = r"^```.*```$"
    if re.match(code_pattern, markdown):
        return BlockType.CODE

    lines = markdown.splitlines()
    
    if all((starts_with(">", l) for l in lines)):
        return BlockType.QUOTE

    if all((starts_with("- ", l) for l in lines)):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    next_num = 1
    for l in lines:
        match = re.match(r"^(\d+)\. ", l)
        if match:
            num = int(match[1])
            if num != next_num:
                is_ordered = False
                break
            else:
                next_num += 1
        else:
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
