from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch(hosts=["http://elastic:123456@0.0.0.0:19200/"])
# response = es.cluster.health()

query = '银汉智算平台采用是什么存储系统'

def es_qa_retrieval(query):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'answer': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_qa_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['answer']] = item['_score']

    return query_result

def es_question_retrieval(query):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'question': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_qa_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['answer']] = item['_score']

    return query_result

def es_subdocument_retrieval(query):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'content': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_subdocument_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['content']] = item['_score']

    return query_result


def es_document_retrieval(query,fusion='sum'):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'content': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_subdocument_store', body=body)['hits']['hits']
    title_json = {}
    title_score = {}

    for item in query_json_list:
        if item['_source']['title'] not in title_json:
            title_json[item['_source']['title']] = []
        title_json[item['_source']['title']].append(item['_score'])

    for key,item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    title = list(title_score.keys())

    body = {
        'from': 0,
        'query': {  # 查询命令
            'terms': {  # 查询方法：模糊查询
                'title.keyword': title  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }
    query_json_list = es.search(index='es_document_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['content']] = title_score[item['_source']['title']]

    return query_result

def es_keyword_subdocument_retrieval(query,fusion='sum'):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'keyword': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_subkeyword_store',body=body)['hits']['hits']

    title_json = {}
    title_score = {}

    for item in query_json_list:
        if item['_source']['title'] not in title_json:
            title_json[item['_source']['title']] = []
        title_json[item['_source']['title']].append(item['_score'])

    for key,item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    title = list(title_score.keys())

    body = {
        'from': 0,
        'query': {  # 查询命令
            'terms': {  # 查询方法：模糊查询
                'title.keyword': title  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }
    query_json_list = es.search(index='es_subdocument_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['content']] = title_score[item['_source']['title']]

    return query_result

def es_keyword_document_retrieval(query,fusion='sum'):
    body = {
        'from': 0,
        'query': {  # 查询命令
            'match': {  # 查询方法：模糊查询
                'keyword': query  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }

    query_json_list = es.search(index='es_subkeyword_store',body=body)['hits']['hits']

    title_json = {}
    title_score = {}

    for item in query_json_list:
        if item['_source']['title'] not in title_json:
            title_json[item['_source']['title']] = []
        title_json[item['_source']['title']].append(item['_score'])

    for key, item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    title = list(title_score.keys())

    body = {
        'from': 0,
        'query': {  # 查询命令
            'terms': {  # 查询方法：模糊查询
                'title.keyword': title  # content为字段名称，match这个查询方法只支持查找一个字段
            }
        }
    }
    query_json_list = es.search(index='es_document_store', body=body)['hits']['hits']

    query_result = {}

    for item in query_json_list:
        query_result[item['_source']['content']] = title_score[item['_source']['title']]

    return query_result