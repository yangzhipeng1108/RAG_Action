from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "xxx.xxx.xxx.xxx", "port": xxxx}])

#有密码
es = Elasticsearch(['10.10.13.12'], http_auth=('xiao', '123456'), timeout=3600)

query = 'The dog is barking'

body ={
     'from':0,
     'query':{    # 查询命令
          'match':{ # 查询方法：模糊查询
               'content':query  #content为字段名称，match这个查询方法只支持查找一个字段
          }
     }
}

filter_path=['hits.hits._source.title',  # 字段1
             'hits.hits._source.content']  # 字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_Subdocument_store',filter_path=filter_path,body=body))


print(es.search(index='es_document_store',filter_path=filter_path,body=body))


query = 'The dog is barking'



body ={
     'from':0,
     'query':{    # 查询命令
          'match':{ # 查询方法：模糊查询
               'content':query  #content为字段名称，match这个查询方法只支持查找一个字段
          }
     }
}

filter_path=['hits.hits._source.title',  # 字段1
             'hits.hits._source.content']  # 字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_Subdocument_store',filter_path=filter_path,body=body))


print(es.search(index='es_document_store',filter_path=filter_path,body=body))



##关键字查询
import os
import getpass
from langchain.chat_models import ChatOpenAI
os.environ['OPENAI_API_KEY'] = ''
llm=ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)

from keybert import KeyLLM, KeyBERT

# Load it in KeyLLM
kw_model = KeyBERT(llm=llm, model='BAAI/bge-large-zh-v1.5')
# Extract keywords
keywords = kw_model.extract_keywords(query, threshold=0.5)

prompt = f"""
我有以下文档:
- {query}

请提供本文档中出现的5个关键字，并用逗号分隔它们。
确保只返回关键字，不说其他内容。 例如，不要说：
"以下是文档中出现的关键字"
"""
response = llm(prompt)
print(response)


body ={
     'from':0,
     'query':{    # 查询命令
          'match':{ # 查询方法：模糊查询
               'content':response  #content为字段名称，match这个查询方法只支持查找一个字段
          }
     }
}

filter_path=['hits.hits._source.tile',  # 字段1
             'hits.hits._source.content']  # 字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_Subdocument_store',filter_path=filter_path,body=body))


print(es.search(index='es_document_store',filter_path=filter_path,body=body))