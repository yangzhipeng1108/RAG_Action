from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Few Shot Examples
examples = [
    {
        "input": "Could the members of The Police perform lawful arrests?",
        "output": "what can the members of The Police do?",
    },
    {
        "input": "Jan Sindel’s was born in what country?",
        "output": "what is Jan Sindel’s personal history?",
    },
]
# We now transform these to example messages
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. Here are a few examples:""",
        ),
        # Few shot examples
        few_shot_prompt,
        # New question
        ("user", "{question}"),
    ]
)

question_gen = prompt | ChatOpenAI(temperature=0) | StrOutputParser()

question = "was chatgpt around while trump was president?"

question_gen.invoke({"question": question})


search = DuckDuckGoSearchAPIWrapper(max_results=4)

###web检索
def retriever(query):
    return search.run(query)


###向量数据库
pinecone.init(api_key="...", environment="...")
vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

from langchain import hub

response_prompt = hub.pull("langchain-ai/stepback-answer")

chain = (
    {
        # Retrieve context using the normal question
        "normal_context": RunnableLambda(lambda x: x["question"]) | retriever,
        # Retrieve context using the step-back question
        "step_back_context": question_gen | retriever,
        # Pass on the question
        "question": lambda x: x["question"],
    }
    | response_prompt
    | ChatOpenAI(temperature=0)
    | StrOutputParser()
)

response = chain.invoke({"question": question})
print(response)