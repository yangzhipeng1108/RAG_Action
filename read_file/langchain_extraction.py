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
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser,JsonOutputFunctionsParser


model = ChatOpenAI(temperature=0)

page_content = ''

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")

#创建prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])

def summary_keywords(page_content):
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

    #创建chain
    tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()
    #调用chain
    return  tagging_chain.invoke({"input": page_content})

# {"summary":'','language':'zh','keyword':''}


Subdocument_result_dict = {'文件存储': ['银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。', '文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。'],

 '文件存储 目录结构': ['目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。',
 '目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。',
 '目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。', '目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。',
 '目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。']}


document_result_dict = {'文件存储': '银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。',
               '文件存储 目录结构': '目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。 目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。 目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。 目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。 目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。'}


document_keyword_dict = {}
Subdocument_keyword_dict = {}

document_summary_dict = {}

for key,value in document_result_dict.items():
    extraction_result = summary_keywords(value)
    document_keyword_dict[key] = extraction_result['keyword']
    if len(value) > 200:
        document_summary_dict[key] = extraction_result['summary']
    else:
        document_summary_dict[key] = ''

for key,values in Subdocument_result_dict.items():
    Subdocument_keyword_dict[key] = []
    for value in values:
        Subdocument_keyword_dict[key].append(summary_keywords(value)['keyword'])

class News(BaseModel):
    """Information about news mentioned."""
    title: str
    author: Optional[str]


class Info(BaseModel):
    """Information to extract"""
    news: List[News]

def title(page_content):
    # 创建函数描述变量
    news_extraction_function = [
        convert_pydantic_to_openai_function(Info)
    ]

    # 绑定函数描述变量
    extraction_model = model.bind(
        functions=news_extraction_function,
        function_call={"name": "Info"}
    )
    # 创建chain
    extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="news")
    # 调用chain
    return extraction_chain.invoke({"input": page_content})

# {"title":'','author':'zh'}