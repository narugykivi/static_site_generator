import sys

from textnode import TextNode, TextType
from clean_copy import copy_all
from generate_page import generate_pages_recursive

def main():
    basepath = sys.argv or "/"
    copy_all("static", "public")
    generate_pages_recursive("content", "template.html", "public", basepath)
    
main()