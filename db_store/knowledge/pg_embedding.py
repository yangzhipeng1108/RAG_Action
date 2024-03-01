import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")


## Loading Environment Variables
from typing import List, Tuple

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import PGEmbedding
from langchain_openai import OpenAIEmbeddings

os.environ["DATABASE_URL"] = getpass.getpass("Database Url:")


loader = TextLoader("state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
connection_string = os.environ.get("DATABASE_URL")
collection_name = "state_of_the_union"

db = PGEmbedding.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name=collection_name,
    connection_string=connection_string,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score: List[Tuple[Document, float]] = db.similarity_search_with_score(query)

for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)


db = PGEmbedding.from_documents(
    embedding=embeddings,
    documents=docs,
    collection_name=collection_name,
    connection_string=connection_string,
    pre_delete_collection=False,
)

PGEmbedding.create_hnsw_index(
    max_elements=10000, dims=1536, m=8, ef_construction=16, ef_search=16
)

# CREATE INDEX ON vectors USING hnsw(vec) WITH (maxelements=10000, dims=1536, m=3, efconstruction=16, efsearch=16);

store = PGEmbedding(
    connection_string=connection_string,
    embedding_function=embeddings,
    collection_name=collection_name,
)

retriever = store.as_retriever()

db1 = PGEmbedding.from_existing_index(
    embedding=embeddings,
    collection_name=collection_name,
    pre_delete_collection=False,
    connection_string=connection_string,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score: List[Tuple[Document, float]] = db1.similarity_search_with_score(query)


for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)