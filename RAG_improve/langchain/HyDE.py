from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain, HypotheticalDocumentEmbedder
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
import pinecone
from langchain_community.vectorstores import Pinecone



pinecone.init(api_key="...", environment="...")

###自己prompt
base_embeddings = OpenAIEmbeddings()
llm = OpenAI()

prompt_template = """Please answer the user's question about the most recent state of the union address
Question: {question}
Answer:"""
prompt = PromptTemplate(input_variables=["question"], template=prompt_template)

llm_chain = LLMChain(llm=llm, prompt=prompt)
embeddings = HypotheticalDocumentEmbedder(llm_chain=llm_chain, base_embeddings=base_embeddings)

with open("../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
docsearch = Pinecone.from_texts(texts, embeddings, index_name="Pinecone-documents")

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
print(docs[0].page_content)



###web_search
# Load with `web_search` prompt
embeddings = HypotheticalDocumentEmbedder.from_llm(llm, base_embeddings, "web_search")

with open("../../state_of_the_union.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
docsearch = Pinecone.from_texts(texts, embeddings, index_name="Pinecone-documents")

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)
print(docs[0].page_content)

