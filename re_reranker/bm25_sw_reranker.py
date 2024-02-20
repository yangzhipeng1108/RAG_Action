# from rank_bm25 import BM25Okapi
#
# retrivel_data  = [
#     "Hello there good man!",
#     "It is quite windy in London",
#     "How is the weather today?"
# ]
#
# tokenized_corpus = [doc.split(" ") for doc in retrivel_data]
#
# bm25 = BM25Okapi(tokenized_corpus)
#
# query = "London tomorrow is a sunny day"
# tokenized_query = query.split(" ")
#
# print(bm25.get_scores(tokenized_query))
#
# print(bm25.get_top_n(tokenized_query, retrivel_data, n=1))
# # ['It is quite windy in London']


from  cutword import Cutter

# cutter = Cutter()
# res = cutter.cutword("精诚所至，金石为开")
# print(res) # ['精诚', '所', '至', '，', '金石为开']
#
# cutter = Cutter(want_long_word=True)
# res = cutter.cutword("精诚所至，金石为开")
# print(res) # ['精诚所至', '，', '金石为开']

from rank_bm25 import BM25Okapi

retrivel_data = [
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.8, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.7},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.7, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.6,
     '服务开通后，各区域间服务资源独立使用，分别统计与计量。': 0.5},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.4, '银汉智算服务需要开通后方可使用，且为区域级开通，即开通所需使用的区域的服务。': 0.2}
]

retrivel_data = list(set(sum([list(i.keys()) for i in retrivel_data], [])))

query = "且为区域级开通，即开通所需使用的区域的服务"

cutter = Cutter()
tokenized_corpus = [cutter.cutword(doc) for doc in retrivel_data]

print(retrivel_data)
print(tokenized_corpus)

bm25 = BM25Okapi(tokenized_corpus)

tokenized_query = cutter.cutword(query)
print(tokenized_query)

print(bm25.get_scores(tokenized_query))

print(bm25.get_top_n(tokenized_query, retrivel_data, n=1))