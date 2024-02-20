from rank_bm25 import BM25Okapi

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

query = "windy London"
tokenized_query = query.split(" ")

print(bm25.get_scores(tokenized_query))

print(bm25.get_top_n(tokenized_query, corpus, n=1))
# ['It is quite windy in London']



from rank_bm25 import BM25Okapi
docs =["Python is a popular programming language.",
       "Python is also used for data analysis.",
       "BM25 is an algorithm used in information retrieval.",
       "BM25 is an extension of TF-IDF."]

query ="Python is an extension of TF-IDF."

bm25 = BM25Okapi(docs)
scores = bm25.get_scores(query)
sorted_docs = sorted(zip(docs, scores),key=lambda x:x[1],reverse=True)

for doc,score in sorted_docs:
    print(doc,score)