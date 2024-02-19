
from rank_bm25 import BM25Okapi

retrivel_data = [
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.8, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.7},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.7, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.6,
     '服务开通后，各区域间服务资源独立使用，分别统计与计量。': 0.5},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.4, '银汉智算服务需要开通后方可使用，且为区域级开通，即开通所需使用的区域的服务。': 0.2}
]

retrivel_data = list(set(sum([list(i.keys()) for i in retrivel_data], [])))

query = "且为区域级开通，即开通所需使用的区域的服务"

bm25 = BM25Okapi(retrivel_data)
scores = bm25.get_scores(query)
sorted_docs = sorted(zip(retrivel_data, scores),key=lambda x:x[1],reverse=True)

for doc,score in sorted_docs:
    print(doc,score)
