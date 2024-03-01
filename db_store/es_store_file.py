from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=["http://elastic:123456@0.0.0.0:19200/"])
# response = es.cluster.health()

#有密码
# es = Elasticsearch(['10.10.13.12'], http_auth=('xiao', '123456'), timeout=3600)

es.indices.delete(index='es_subdocument_store', ignore=[400, 404])
#
es.indices.create(index="es_subdocument_store",ignore=400)

action = []
def es_store_Subdocument(Subdocument_result_dict,i):
#插入多条数据

    for key in Subdocument_result_dict.keys():
        if len(Subdocument_result_dict[key]) > 1:
            doc_inter = []
            for  context in Subdocument_result_dict[key]:
                doc_inter.append({"_index":"es_subdocument_store","_type":"doc","_id":i,"_source":{"title":key,"content":context}})
                i += 1
            action.extend(doc_inter)
        elif len(Subdocument_result_dict[key]) == 0:
            pass
        else:
            action.append({"_index":"es_subdocument_store","_type":"doc","_id":i,"_source":{"title":key,"content":Subdocument_result_dict[key][0]}})
            i += 1
    return i

f = open("Subdocument_result_dict.txt",encoding='utf-8')
line = f.readlines()
i = 1
for value  in line :
    document_result_dict = eval(value)
    print(document_result_dict)
    i = es_store_Subdocument(document_result_dict,i)
helpers.bulk( es, action )



es.indices.delete(index='es_document_store', ignore=[400, 404])
es.indices.create(index="es_document_store",ignore=400)


# 插入多条数据
action = []
def es_store_document(document_result_dict,i):
    for key in document_result_dict.keys():
        action.append({"_index":"es_document_store","_type":"doc","_id":i,"_source":{"title":key,"content":document_result_dict[key]}})
        i += 1
    return i

f = open("document_result_dict.txt",encoding='utf-8')
line = f.readlines()
i = 1
for value  in line :
    document_result_dict = eval(value)
    print(document_result_dict)
    i = es_store_document(document_result_dict,i)
helpers.bulk( es, action )

