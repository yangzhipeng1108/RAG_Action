from gensim.summarization import bm25
import jieba

"""
注意这里的gensim使用的是3.8.1版本的，高版本的可能会出现找不到gensim.summarization
"""
class BM25Model:
    def __init__(self, data_list):
        self.data_list = data_list
        # corpus : list of list of str
        self.corpus = self.load_corpus()

    def bm25_similarity(self, query, num_best=1):
        query = jieba.lcut(query)  # 分词
        bm = bm25.BM25(self.corpus)
        scores = bm.get_scores(query)
        id_score = [(i, score) for i, score in enumerate(scores)]
        id_score.sort(key=lambda e: e[1], reverse=True)
        return id_score[0: num_best]

    def load_corpus(self):
        corpus = [jieba.lcut(data) for data in self.data_list]
        return corpus


if __name__ == '__main__':

    retrivel_data = [
        {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.8, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.7}, {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.7, '管理员后台开通可以线下联系客户经理，通过管理员后台直接开通服务。': 0.6, '服务开通后，各区域间服务资源独立使用，分别统计与计量。': 0.5}, {'平台管理员将对申请信息进行审核，并为符合要求的客户开通服务。': 0.4, '银汉智算服务需要开通后方可使用，且为区域级开通，即开通所需使用的区域的服务。': 0.2}
    ]

    retrivel_data = list(set(sum([list(i.keys()) for i in retrivel_data], [])))

    query = "且为区域级开通，即开通所需使用的区域的服务"
    BM25 = BM25Model(retrivel_data)
    print(BM25.bm25_similarity(query, 1))