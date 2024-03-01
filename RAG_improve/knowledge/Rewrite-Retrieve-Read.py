
###Baseline
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
template = """Answer the users question based only on the following context:

<context>
{context}
</context>

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0)

search = DuckDuckGoSearchAPIWrapper()  ##DuckDuckGo是一款互联网搜索引擎



# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
# from langchain.tools import DuckDuckGoSearchResults
# wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
#
# search = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")
#
# search.run("Obama")


def retriever(query):
    return search.run(query)

'''这里提示的输入应该是一个带有“context”和“question”键的地图。 用户输入只是问题。 因此，我们需要使用检索器获取上下文，并通过“question”键下的用户输入。
 在这种情况下，RunnablePassthrough 允许我们将用户的问题传递给提示和模型。'''
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
simple_query = "what is langchain?"
chain.invoke(simple_query)

distracted_query = "man that sam bankman fried trial was crazy! what is langchain?"
chain.invoke(distracted_query)

print(retriever(distracted_query))


###Rewrite-Retrieve-Read Implementation
template = """Provide a better search query for web search engine to answer the given question, end the queries with ’**’. Question: {x} Answer:"""
rewrite_prompt = ChatPromptTemplate.from_template(template)
from langchain import hub

rewrite_prompt = hub.pull("langchain-ai/rewrite")
print(rewrite_prompt.template)
# Provide a better search query for web search engine to answer the given question, end the queries with ’**’.  Question {x} Answer:
# # Parser to remove the `**`


def _parse(text):
    return text.strip("**")

rewriter = rewrite_prompt | ChatOpenAI(temperature=0) | StrOutputParser() | _parse
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
rewrite_retrieve_read_chain.invoke(distracted_query)
