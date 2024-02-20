from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "xxx.xxx.xxx.xxx", "port": xxxx}])

#有密码
es = Elasticsearch(['10.10.13.12'], http_auth=('xiao', '123456'), timeout=3600)

#创建索引（ES中的索引即数据库）
# 创建索引（数据库）
es.indices.create(index="索引名字，字母小写")
es.indices.create(index="es_test",ignore=400)

# 插入数据
body={'keyword':'测试',"content":"这是一个测试数据1"}
es.index(index='es_test',doc_type='_doc',body=body)

#插入多条数据

doc=[{'index':{'_index':'es_zilongtest','_type':'_doc','_id':4}},
     {'keyword':'食物',"content":"我喜欢吃大白菜"},
     {'index': {'_index': 'es_zilongtest', '_type': '_doc', '_id': 5}},
     {'keyword': '食物', "content": "鸡胸肉很好吃"},
     {'index':{'_index':'es_zilongtest','_type':'_doc','_id':6}},
     {'keyword':'食物',"content":"小白菜也好吃"},
     ]
es.bulk(index='es_zilongtest',doc_type='_doc',body=doc)

print(es.search(index='es_zilongtest'))

'''
{'took': 4,
 'timed_out': False, 
 '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
 
 'hits': {'total': {'value': 8, 'relation': 'eq'}, 
          'max_score': 1.0, 
          'hits': [
              {'_index': 'es_zilongtest', '_type': '_doc','_id': 'mTZQK3wBr1SJ1UhpryaJ','_score': 1.0,
               '_source': {'keyword': '测试', 'content': '这是一个测试数据'}},
              
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': 'mjZRK3wBr1SJ1UhpCSZj', '_score': 1.0, 
               '_source': {'keyword': '测试', 'content': '这是一个测试数据1'}},
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '1', '_score': 1.0, 
               '_source': {'keyword': '动物', 'content': '大白把隶属家的小黄咬了'}}, 
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '2', '_score': 1.0, 
               '_source': {'keyword': '动物', 'content': '王博家里买了很多小鸡'}}, 
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '3', '_score': 1.0,
               '_source': {'keyword': '动物', 'content': '王叔家的小白爱吃鸡胸肉'}}, 
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '4', '_score': 1.0, 
               '_source': {'keyword': '食物', 'content': '我喜欢吃大白菜'}}, 
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '5', '_score': 1.0, 
               '_source': {'keyword': '食物', 'content': '鸡胸肉很好吃'}}, 
              {'_index': 'es_zilongtest', '_type': '_doc', '_id': '6', '_score': 1.0, 
               '_source': {'keyword': '食物', 'content': '小白菜也好吃'}}]}}
'''


# 查询数据
body = {
    'from': 0,  # 从0开始
    'size': 10  # size可以在es.search中指定，也可以在此指定，默认是10
}

print(es.search(index='es_zilongtest', body=body))

# size的另一种指定方法
es.search(index='es_python', filter_path=filter_path, body=body, size=200)

# 有过滤字段查询数据
body ={
     'from':0, #从0开始
}
# 定义过滤字段，最终只显示此此段信息 hits.hits._source.写在前面 后面写你自己定义的字段名 我这里是keyword和content
filter_path=['hits.hits._source.keyword',  # keyword为第一个需要显示的字段
             'hits.hits._source.content']  # content为字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_zilongtest',filter_path=filter_path,body=body))

body ={
     'from':0,
     'query':{    # 查询命令
          'match':{ # 查询方法：模糊查询
               'content':'小白菜'  #content为字段名称，match这个查询方法只支持查找一个字段
          }
     }
}
'''可以看到 content中不仅出现了小白菜 还出现了大白菜 大白 小白等内容 因为模糊查询把小白菜进行了拆分'''
'''{‘hits’: {‘hits’: [{’_source’: {‘keyword’: ‘食物’, ‘content’: ‘小白菜也好吃’}}, 
{’_source’: {‘keyword’: ‘食物’, ‘content’: ‘我喜欢吃大白菜’}},
 {’_source’: {‘keyword’: ‘动物’, ‘content’: ‘大白把隶属家的小黄咬了’}},
  {’_source’: {‘keyword’: ‘动物’, ‘content’: ‘王叔家的小白爱吃鸡胸肉’}},
   {’_source’: {‘keyword’: ‘动物’, ‘content’: ‘王博家里买了很多小鸡’}}]}}
'''
'''
{‘took’: 8, ‘timed_out’: False, 
‘_shards’: {‘total’: 1, ‘successful’: 1, ‘skipped’: 0, ‘failed’: 0},
 ‘hits’: {‘total’: {‘value’: 5, ‘relation’: ‘eq’}, ‘max_score’: 3.0320468, 
 ‘hits’: [{’_index’: ‘es_zilongtest’, ‘_type’: ‘_doc’, ‘_id’: ‘6’, ‘_score’: 3.0320468, ‘_source’: {‘keyword’: ‘食物’, ‘content’: ‘小白菜也好吃’}},
  {’_index’: ‘es_zilongtest’, ‘_type’: ‘_doc’, ‘_id’: ‘4’, ‘_score’: 2.1276836, ‘_source’: {‘keyword’: ‘食物’, ‘content’: ‘我喜欢吃大白菜’}}, 
  {’_index’: ‘es_zilongtest’, ‘_type’: ‘_doc’, ‘_id’: ‘1’, ‘_score’: 1.2374083, ‘_source’: {‘keyword’: ‘动物’, ‘content’: ‘大白把隶属家的小黄咬了’}}, 
  {’_index’: ‘es_zilongtest’, ‘_type’: ‘_doc’, ‘_id’: ‘3’, ‘_score’: 1.2374083, ‘_source’: {‘keyword’: ‘动物’, ‘content’: ‘王叔家的小白爱吃鸡胸肉’}},
   {’_index’: ‘es_zilongtest’, ‘_type’: ‘_doc’, ‘_id’: ‘2’, ‘_score’: 0.6464764, ‘_source’: {‘keyword’: ‘动物’, ‘content’: ‘王博家里买了很多小鸡’}}]}}
'''

filter_path=['hits.hits._source.keyword',  # 字段1
             'hits.hits._source.content']  # 字段2
# print(es.search(index='es_zilongtest'))
print(es.search(index='es_zilongtest',filter_path=filter_path,body=body))

#精确单值查询
body1={
     "query":{
          "terms":{
               "keyword.keyword":["食物","测试"] # 查询keyword="食物"或"测试"...的数据
          }
     }
}
'''这里的第一个keyword是我自己设定的字段名，第二个是接口要求的必须为keyword，所以我此处可以改成'''
print(es.search(index='es_zilongtest',body=body1))


#精确多值查询
body1={
     "query":{
          "terms":{
               "content.keyword":["小白菜","大白"] # 查询keyword="小白菜"或"大白"...的数据
          }
     }
}
'''这样搜索结果为空，因为并没有content是小白菜或大白（文中含有这个字段也不行，必须完全相同）'''

# 查询多个字段中都包含指定内容的数据
body3 = {
    "query":{
        "multi_match":{
            "query":"小白菜",  # 指定查询内容，注意：会被分词
            "fields":["keyword", "content"]  # 指定字段
        }
    }
}
print(es.search(index='es_zilongtest',body=body3))


body3 = {
    "query":{
        "prefix":{
            "content.keyword":"小白菜",  # 查询前缀是指定字符串的数据
        }
    }
}
# 注：英文不需要加keyword
print(es.search(index='es_zilongtest',body=body3))

body = {
    'query': {
        'wildcard': {
            'ziduan1.keyword': '?刘婵*'  # ?代表一个字符，*代表0个或多个字符
        }
    }
}
# 注：此方法只能查询单一格式的（都是英文字符串，或者都是汉语字符串）。两者混合不能查询出来。


body = {
    'query': {
        'regexp': {
            'ziduan1': 'W[0-9].+'   # 使用正则表达式查询
        }
    }
}


# must：[] 各条件之间是and的关系
body = {
        "query":{
            "bool":{
                'must': [{"term":{'ziduan1.keyword': '我爱你中国'}},
                         {'terms': {'ziduan2': ['I love', 'China']}}]
            }
        }
    }

# should: [] 各条件之间是or的关系
body = {
        "query":{
            "bool":{
                'should': [{"term":{'ziduan1.keyword': '我爱你中国'}},
                         {'terms': {'ziduan2': ['I love', 'China']}}]
            }
        }
    }

# must_not：[]各条件都不满足
body = {
        "query":{
            "bool":{
                'must_not': [{"term":{'ziduan1.keyword': '我爱你中国'}},
                         {'terms': {'ziduan2': ['I love', 'China']}}]
            }
        }
    }



# bool嵌套bool
# ziduan1、ziduan2条件必须满足的前提下，ziduan3、ziduan4满足一个即可
body = {
    "query":{
        "bool":{
            "must":[{"term":{"ziduan1":"China"}},  #  多个条件并列  ，注意：must后面是[{}, {}],[]里面的每个条件外面有个{}
                    {"term":{"ziduan2.keyword": '我爱你中国'}},
                    {'bool': {
                        'should': [
                            {'term': {'ziduan3': 'Love'}},
                            {'term': {'ziduan4': 'Like'}}
                        ]
                    }}
            ]
        }
    }
}


