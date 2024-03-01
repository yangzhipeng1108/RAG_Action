import os
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
os.environ["BAICHUAN_API_KEY"] = ""

from langchain_community.llms.baichuan import BaichuanLLM

from IR_retrieval.es_retrieval import  es_subdocument_retrieval
from IR_retrieval.pg_bge_retrieval import pg_subdocument_bge_retrieval
from re_reranker.rrf_reranker import reciprocal_rank_fusion



from pgvector.psycopg2 import register_vector
import psycopg2
from FlagEmbedding import FlagModel


model = FlagModel('BAAI/bge-large-zh-v1.5',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="vector_demo",
    user="postgres",
    password="123456",
)

cur = conn.cursor()

def rag_search(input, history=[], top_p=0.85,temperature=0.3):

    es_query_result = es_subdocument_retrieval(input)
    pg_query_result = pg_subdocument_bge_retrieval(cur,query_embeddings = str(list(model.encode(input))))

    retrieval_result = [es_query_result] + [pg_query_result]

    reranker_result = reciprocal_rank_fusion(retrieval_result)

    original_array = sorted(reranker_result, key=lambda k: reranker_result[k], reverse=True)

    odd_part = original_array[::2]
    even_part = original_array[1::2][::-1]

    context = odd_part + even_part
    context = ' '.join(context)

    llm = BaichuanLLM()

    template = '请根据一下背景知识{context}，回答以下问题{question}'

    prompt = PromptTemplate.from_template(template)

    question_gen = prompt | llm | StrOutputParser()

    response = question_gen.invoke({"context": context, "question": input})

    new_history = history + [(input, response)]

    return response, new_history


resource,_ = rag_search('银汉智算平台采用是什么存储系统')
print(resource)


# 关闭游标
cur.close()

# 关闭连接
conn.close()

