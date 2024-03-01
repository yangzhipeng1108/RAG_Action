# !/usr/bin/env python
# encoding: utf-8
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from operator import itemgetter
from FlagEmbedding import FlagReranker


app = FastAPI()

# reranker = FlagReranker('/data_2/models/bge-reranker-base/models--BAAI--bge-reranker-base/blobs', use_fp16=True)
reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation


class QuerySuite(BaseModel):
    query: str
    passages: list[str]
    top_k: int = 1


@app.post('/bge_base_rerank')
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


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=50072)