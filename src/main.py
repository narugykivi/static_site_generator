from textnode import TextNode, TextType
from clean_copy import copy_all
from generate_page import generate_page

def main():
    copy_all()
    generate_page("content/index.md", "template.html", "public/index.html")
    
main()