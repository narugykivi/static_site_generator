from textnode import TextNode, TextType

def main():
    test_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev/lessons/fcb2fe55-e155-4f91-a904-4e266df13952")
    print(test_node)
    
main()