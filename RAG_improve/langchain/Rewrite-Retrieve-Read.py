from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain import hub

template = """Answer the users question based only on the following context:

<context>
{context}
</context>

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0)

search = DuckDuckGoSearchAPIWrapper()  ##DuckDuckGo是一款互联网搜索引擎


###web检索
def retriever(query):
    return search.run(query)


###向量数据库
pinecone.init(api_key="...", environment="...")
vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

distracted_query = "man that sam bankman fried trial was crazy! what is langchain?"

###Rewrite-Retrieve-Read Implementation
# template = """Provide a better search query for web search engine to answer the given question, end the queries with ’**’. Question: {x} Answer:"""
# rewrite_prompt = ChatPromptTemplate.from_template(template)


rewrite_prompt = hub.pull("langchain-ai/rewrite")
# print(rewrite_prompt.template)
# Provide a better search query for web search engine to answer the given question, end the queries with ’**’.  Question {x} Answer:
# # Parser to remove the `**`

def _parse(text):
    return text.strip("**")

rewriter = rewrite_prompt | model | StrOutputParser() | _parse
rewriter.invoke({"x": distracted_query})

rewrite_retrieve_read_chain = (
    {
        "context": {"x": RunnablePassthrough()} | rewriter | retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

response = rewrite_retrieve_read_chain.invoke(distracted_query)
print(response)
