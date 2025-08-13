import re

from blocktype import BlockType
from htmlnode import ParentNode, LeafNode
from textnode import TextType
from inline_functions import text_to_textnodes

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
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING

    if starts_with("```", markdown) and markdown[-3:] == "```":
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

def block_type_to_html_node(block_type, heading_level=None):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", [])
        case BlockType.HEADING:
            return ParentNode("h1", [])
        case BlockType.CODE:
            return ParentNode("pre", [])
        case BlockType.QUOTE:
            return ParentNode("blockquote", [])
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", [])
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", [])

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})

def text_to_inline_html_nodes(block):
    html_nodes = []

    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes

def markdown_to_html_node(markdown):
    div = ParentNode("div", [])

    blocks = markdown_to_blocks(markdown)
    for b in blocks:
        t = block_to_block_type(b)
        node = block_type_to_html_node(t)
        if not t == BlockType.CODE:
            node.children = text_to_inline_html_nodes(b)
        else:
            node.children = [LeafNode("code", b.strip("`"))]
        div.children.append(node)

    return div
