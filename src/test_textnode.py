import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_empty_url(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
