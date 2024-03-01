from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain import hub

model = ChatOpenAI(temperature=0)

template = """Answer the users question based only on the following context:

<context>
{context}
</context>

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

search = DuckDuckGoSearchAPIWrapper()  ##DuckDuckGo是一款互联网搜索引擎

###web检索
def retriever(query):
    return search.run(query)

pinecone.init(api_key="...", environment="...")
vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

iter_retgen_chain = (
    {
        "context": {"x": RunnablePassthrough()}  | retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

def iter_retgen(question,iter_number):
    for i in range(iter_number):
        question = iter_retgen_chain.invoke({"question": question})

    return question


question = "was chatgpt around while trump was president?"
iter_number = 2
