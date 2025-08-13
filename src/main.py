from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(tn)
    p = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    hn = HTMLNode("a", "Click here", None, p)
    print(hn)

main()
