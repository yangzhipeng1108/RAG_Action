# !pip install  pgvector

# 我们想使用OpenAIEmbeddings，因此必须获取OpenAI  API密钥。

import os
import getpass

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API密钥：')

## 加载环境变量
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

# False

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import TextLoader
from langchain.docstore.document import Document

loader = TextLoader('../../../state_of_the_union.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

## PGVector需要数据库的连接字符串。
## 我们将从环境变量中加载它。
import os

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "localhost"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
    user=os.environ.get("PGVECTOR_USER", "postgres"),
    password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
)

## 示例
# postgresql+psycopg2://username:password@localhost:5432/database_name


# 带分数的相似性搜索  #
# 使用欧几里得距离进行相似性搜索（默认)  #
# PGVector模块将尝试使用集合名称创建表。因此，请确保集合名称唯一且用户有
# 权限创建表。

db = PGVector.from_documents(
embedding = embeddings,
documents = docs,
collection_name = "state_of_the_union",
connection_string = CONNECTION_STRING,
)