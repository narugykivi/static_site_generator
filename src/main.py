import sys

from textnode import TextNode, TextType
from clean_copy import copy_all
from generate_page import generate_pages_recursive

def main():
    basepath = sys.argv[1] or "/"
    copy_all("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()