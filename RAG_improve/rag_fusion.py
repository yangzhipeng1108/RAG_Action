import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings

pinecone.init(api_key="...", environment="...")
#%%
all_documents = {
    "doc1": "Climate change and economic impact.",
    "doc2": "Public health concerns due to climate change.",
    "doc3": "Climate change: A social perspective.",
    "doc4": "Technological solutions to climate change.",
    "doc5": "Policy changes needed to combat climate change.",
    "doc6": "Climate change and its impact on biodiversity.",
    "doc7": "Climate change: The science and models.",
    "doc8": "Global warming: A subset of climate change.",
    "doc9": "How climate change affects daily weather.",
    "doc10": "The history of climate change activism.",
}
#%%
vectorstore = Pinecone.from_texts(
    list(all_documents.values()), OpenAIEmbeddings(), index_name="rag-fusion"
)

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
#%%
from langchain import hub

prompt = hub.pull("langchain-ai/rag-fusion-query-generation")
#%%
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant that generates multiple search queries based on a single input query."),
#     ("user", "Generate multiple search queries related to: {original_query}"),
#     ("user", "OUTPUT (4 queries):")
# ])
#%%
generate_queries = (
    prompt | ChatOpenAI(temperature=0) | StrOutputParser() | (lambda x: x.split("\n"))
)

original_query = "impact of climate change"
#%%
vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
#%%
from langchain.load import dumps, loads


def reciprocal_rank_fusion(results: list[list], k=60):
    fused_scores = {}
    for docs in results:
        # Assumes the docs are returned in sorted order of relevance
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            previous_score = fused_scores[doc_str]
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_results
#%%
chain = generate_queries | retriever.map() | reciprocal_rank_fusion
#%%
chain.invoke({"original_query": original_query})