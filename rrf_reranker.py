

retrivel_data = [
    {'文件存储':0.8,'文件存储 目录结构':0.7},{'文件存储':0.7,'文件存储 目录结构':0.6,'公共数据盘':0.5},{'文件存储':0.4,'缓存盘':0.2}
]

def reciprocal_rank_fusion(search_results_list, k=60):
    fused_scores = {}

    for doc_scores in search_results_list:
        for rank, (doc, score) in enumerate(sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            previous_score = fused_scores[doc]
            fused_scores[doc] += 1 / (rank + k)
            print(
                f"Updating score for {doc} from {previous_score} to {fused_scores[doc]} based on rank {rank} in query")

    reranked_results = {doc: score for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)}
    print("Final reranked results:", reranked_results)
    return reranked_results

print(reciprocal_rank_fusion(retrivel_data,1))
