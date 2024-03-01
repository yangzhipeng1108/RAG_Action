from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import ChatGLM

# import os

template = """{question}"""
prompt = PromptTemplate.from_template(template)

# default endpoint_url for a local deployed ChatGLM api server
endpoint_url = "http://127.0.0.1:8000"

# direct access endpoint in a proxied environment
# os.environ['NO_PROXY'] = '127.0.0.1'

llm = ChatGLM(
    endpoint_url=endpoint_url,
    max_token=80000,
    history=[
        ["我将从美国到中国来旅游，出行前希望了解中国的城市", "欢迎问我任何问题。"]
    ],
    top_p=0.9,
    model_kwargs={"sample_model_args": False},
)

# turn on with_history only when you want the LLM object to keep track of the conversation history
# and send the accumulated context to the backend model api, which make it stateful. By default it is stateless.
# llm.with_history = True


llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "北京和上海两座城市有什么不同？"

llm_chain.run(question)



from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.messages import AIMessage
from langchain_community.llms.chatglm3 import ChatGLM3

template = """{question}"""
prompt = PromptTemplate.from_template(template)

endpoint_url = "http://127.0.0.1:8000/v1/chat/completions"

messages = [
    AIMessage(content="我将从美国到中国来旅游，出行前希望了解中国的城市"),
    AIMessage(content="欢迎问我任何问题。"),
]

llm = ChatGLM3(
    endpoint_url=endpoint_url,
    max_tokens=80000,
    prefix_messages=messages,
    top_p=0.9,
)

llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "北京和上海两座城市有什么不同？"

llm_chain.run(question)