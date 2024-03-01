# https://zhuanlan.zhihu.com/p/670480082

# pip install -U python-dotenv

import os
import openai

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI


# 定义pydantic类用以生成openai的函数描述变量
class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: str = Field(description="sentiment of text, should be `pos`, `neg`, or `neutral`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")

tagging_functions = [convert_pydantic_to_openai_function(Tagging)]
print(tagging_functions)

# 根据模板创建prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

# 创建llm
model = ChatOpenAI(temperature=0)
# 绑定函数描述变量，指定函数名(意味着强制调用)
model_with_functions = model.bind(
    functions=tagging_functions,
    function_call={"name": "Tagging"}
)
# 创建chain
tagging_chain = prompt | model_with_functions
# 调用chain
tagging_chain.invoke({"input": "I love shanghai"})

tagging_chain.invoke({"input": "这家饭店的菜真难吃"})


class Person(BaseModel):
    """Information about a person."""
    name: str = Field(description="person's name")
    age: Optional[int] = Field(description="person's age")


class Information(BaseModel):
    """Information to extract."""
    people: List[Person] = Field(description="List of info about people")

print(convert_pydantic_to_openai_function(Information))

# 创建函数描述变量
extraction_functions = [convert_pydantic_to_openai_function(Information)]

# 绑定函数描述变量
extraction_model = model.bind(functions=extraction_functions,
                              function_call={"name": "Information"})

# llm调用
extraction_model.invoke("小明今年15岁，他的妈妈是张丽丽")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])

# 创建函数描述变量
extraction_functions = [convert_pydantic_to_openai_function(Information)]

# 绑定函数描述变量
extraction_model = model.bind(functions=extraction_functions,
                              function_call={"name": "Information"})
# 创建chain
extraction_chain = prompt | extraction_model
# 调用chain
extraction_chain.invoke({"input": "小明今年15岁，他的妈妈是张丽丽"})

from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser,JsonOutputFunctionsParser

# 创建chain
extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="people")

# 调用chain
extraction_chain.invoke({"input": "小明今年15岁，他的妈妈是张丽丽"})

from langchain.document_loaders import WebBaseLoader

# 创建loader,获取网页数据
loader = WebBaseLoader("https://tech.ifeng.com/c/8VEctgVlwbk")
documents = loader.load()

# 查看网页内容
doc = documents[0]
page_content = doc.page_content[:3000]
print(page_content)

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")

#创建openai函数描述变量
overview_tagging_function = [
    convert_pydantic_to_openai_function(Overview)
]
#创建llm
tagging_model = model.bind(
    functions=overview_tagging_function,
    function_call={"name":"Overview"}
)
#创建prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])
#创建chain
tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()
#调用chain
tagging_chain.invoke({"input": page_content})


class News(BaseModel):
    """Information about news mentioned."""
    title: str
    author: Optional[str]


class Info(BaseModel):
    """Information to extract"""
    news: List[News]

# 创建函数描述变量
news_extraction_function = [
    convert_pydantic_to_openai_function(Info)
]

# 创建llm
model = ChatOpenAI(temperature=0)
# 绑定函数描述变量
extraction_model = model.bind(
    functions=news_extraction_function,
    function_call={"name": "Info"}
)
# 创建chain
extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="news")
# 调用chain
extraction_chain.invoke({"input": page_content})

#加载论文
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
documents = loader.load()
doc = documents[0]
page_content = doc.page_content[:10000]
print(page_content)


# 创建paper类
class Paper(BaseModel):
    """Information about papers mentioned."""
    title: str
    author: Optional[str]


# 创建Info类
class Info(BaseModel):
    """Information to extract"""
    papers: List[Paper]


# 创建函数描述变量
paper_extraction_function = [
    convert_pydantic_to_openai_function(Info)
]
# 将函数描述变量绑定llm
extraction_model = model.bind(
    functions=paper_extraction_function,
    function_call={"name": "Info"}
)

template = """A article will be passed to you. Extract from it all papers that are mentioned by this article. 
Do not extract the name of the article itself. If no papers are mentioned that's fine - you don't need to extract any! Just return an empty list.
Do not make up or guess ANY extra information. Only extract what exactly is in the text."""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="papers")
extraction_chain.invoke({"input": page_content})

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnableLambda

text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)

prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

response = prep.invoke(doc.page_content)
print(response)
print(len(response))


# 定义矩阵展开函数
def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


# 测试展开函数
flatten([[1, 2], [3, 4]])
# 创建chain
chain = prep | extraction_chain.map() | flatten

# 调用chain
chain.invoke(doc.page_content)



##################################################################

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAIChat
from langchain.chains import LLMChain
import os
#你申请的openai的api key
os.environ['OPENAI_API_KEY'] = 'xxxxxxxx'

text = "阿尔茨海默病(Alzheimer's disease, AD),俗称老年痴呆症,是一种全身性神经退行性疾病，它是由大脑神经退行性变性引起的，\
主要表现为记忆力减退、思维能力减退、行为变化等。阿尔茨海默病的原因尚不十分清楚，但是研究表明，阿尔茨海默病可能与遗传因素、环境因素、\
营养不良、压力过大、不良生活习惯等有关。根据世界卫生组织的统计数据，全球有超过4700万人患有阿尔茨海默病，其中美国有超过600万人患有阿尔茨海默病，\
欧洲有超过1000万人患有阿尔茨海默病，亚洲有超过2500万人患有阿尔茨海默病，其中中国有超过1000万人患有阿尔茨海默病。阿尔茨海默病的发病率与年龄有关，\
随着年龄的增长而增加，65岁以上的人群为主要受害群体，占比高达80%，其中45-65岁的人群占比为15%，20-45岁的人群占比为5%。65岁以上的人群发病率约为10%，\
75岁以上的人群发病率约为20%，85岁以上的人群发病率约为30%。根据统计，男性患病率高于女性，男性患病比例为1.4：1，即男性患病率比女性高出40%。\
根据统计，阿尔茨海默病在不同的人种中分布情况也有所不同。白人患病率最高，占总患病率的70%，黑人患病率次之，占总患病率的20%，\
其他少数民族患病率最低，占总患病率的10%。阿尔茨海默病在不同的饮食习惯中分布情况也有所不同。维生素B12缺乏的人群患病率更高，\
而均衡膳食的人群患病率较低。阿尔茨海默病不仅会给患者带来记忆力减退、思维能力减退、行为变化等症状，还会给患者的家庭带来巨大的心理负担。\
因此，患者应尽快就医，及时进行治疗。治疗阿尔茨海默病的方法有药物治疗、行为治疗、认知行为治疗等，具体治疗方案要根据患者的具体情况而定。"

# 加载openai的llm
llm = OpenAIChat(model_name="gpt-3.5-turbo")

# 创建模板
fact_extraction_prompt = PromptTemplate(
    input_variables=["text_input"],
    template="从下面的本文中提取关键事实。尽量使用文本中的统计数据来说明事实:\n\n {text_input}"
)

# 定义chain
fact_extraction_chain = LLMChain(llm=llm, prompt=fact_extraction_prompt)
facts = fact_extraction_chain.run(text)
print(facts)

doctor_prompt = PromptTemplate(
    input_variables=["facts"],
    template="你是神经内科医生。根据以下阿尔茨海默病的事实统计列表，为您的病人写一个简短的预防阿尔茨海默病的建议。 不要遗漏关键信息：\n\n {facts}"
)

# 定义chain
doctor_chain = LLMChain(llm=llm, prompt=doctor_prompt)
doctor_suggest = doctor_chain.run(facts)
print(doctor_suggest)

from langchain.chains import SimpleSequentialChain, SequentialChain
#定义SimpleSequentialChain
full_chain = SimpleSequentialChain(chains=[fact_extraction_chain, doctor_chain],
                                   verbose=True)
response = full_chain.run(text)