# encoding: utf-8
from pydantic import BaseModel
from operator import itemgetter
from FlagEmbedding import FlagReranker


# reranker = FlagReranker('/data_2/models/bge-reranker-base/models--BAAI--bge-reranker-base/blobs', use_fp16=True)
reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation


retrivel_data = [
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.8, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.7},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.7, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.6,
     '服务开通后，各区域间服务资源独立使用，分别统计与计量。': 0.5},
    {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.4, '银汉智算服务需要开通后方可使用，且为区域级开通，即开通所需使用的区域的服务。': 0.2}
]

retrivel_data = list(set(sum([list(i.keys()) for i in retrivel_data], [])))

query = "且为区域级开通，即开通所需使用的区域的服务"

class QuerySuite(BaseModel):
    query: str
    passages: list[str]
    top_k: int = 1


def rerank(query_suite: QuerySuite):
    scores = reranker.compute_score([[query_suite.query, passage] for passage in query_suite.passages])
    if isinstance(scores, list):
        similarity_dict = {passage: scores[i] for i, passage in enumerate(query_suite.passages)}
    else:
        similarity_dict = {passage: scores for i, passage in enumerate(query_suite.passages)}
    sorted_similarity_dict = sorted(similarity_dict.items(), key=itemgetter(1), reverse=True)
    result = {}
    for j in range(query_suite.top_k):
        result[sorted_similarity_dict[j][0]] = sorted_similarity_dict[j][1]
    return result

qS = QuerySuite(query = query,passages = retrivel_data,top_k = 5)

result = rerank(qS)
print(result)
