from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=["http://elastic:123456@0.0.0.0:19200/"])
# response = es.cluster.health()

query = '银汉智算平台采用是什么存储系统'

body ={
     'from':0,
     'query':{    # 查询命令
          'match':{ # 查询方法：模糊查询
               'answer':query  #content为字段名称，match这个查询方法只支持查找一个字段
          }
     }
}

filter_path=['hits.hits._source.question',  # 字段1
             'hits.hits._source.answer']  # 字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_qa_store',filter_path=filter_path,body=body))
