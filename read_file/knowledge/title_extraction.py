from langchain.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from typing import  List, Optional, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from typing import List
import sys
from langchain.text_splitter import HTMLHeaderTextSplitter


path = 'E:/python/yovole/NLP/pre-train/ai_project/yovole/'
#文本加载
loader = TextLoader(path + "source/ai/ai/html/activate.md",encoding='UTF-8')
# loader = UnstructuredMarkdownLoader("source/ai/ai/html/activate.md",encoding='UTF-8')

# loader = TextLoader(path + "source/ai/ai/html/file_storage.md",encoding='UTF-8')
result = loader.load()


#md分割
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)
md_header_splits = markdown_splitter.split_text(result[0].page_content)
print(md_header_splits)

path = 'E:/python/yovole/NLP/pre-train/ai_project/yovole/'
#文本加载
loader = TextLoader(path + "source/ai/ai/html/activate.md",encoding='UTF-8')
# loader = UnstructuredMarkdownLoader("source/ai/ai/html/activate.md",encoding='UTF-8')

# loader = TextLoader(path + "source/ai/ai/html/file_storage.md",encoding='UTF-8')
result = loader.load()

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3")
]

html_header_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

html_header_splits = html_header_splitter.split_text(result[0].page_content)
print(html_header_splits)


##web  提取title 和内容   对应合适网页 也可以设置 h1 h2


