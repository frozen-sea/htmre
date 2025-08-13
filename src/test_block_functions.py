import unittest

from block_functions import *

class TestBlockFunctions(unittest.TestCase):
    def test_heading(self):
        result = block_to_block_type("### Heading 3")
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        result = block_to_block_type("```This is a code block```")
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        result = block_to_block_type(">this\n>is\n>a\n>quote")
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered(self):
        result = block_to_block_type("- foo\n- bar\n- baz")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered(self):
        result = block_to_block_type("1. here\n2. is\n3. an\n4. ordered\n5. one")
        self.assertEqual(result, BlockType.ORDERED_LIST)

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
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
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
            "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
