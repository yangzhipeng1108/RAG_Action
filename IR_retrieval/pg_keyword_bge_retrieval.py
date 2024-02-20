from pgvector.psycopg2 import register_vector
import psycopg2
from FlagEmbedding import FlagModel

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="vector_demo",
    user="postgres",
    password="123456",
)

query = '银汉智算平台采用是什么存储系统'

cur = conn.cursor()

model = FlagModel('BAAI/bge-large-zh-v1.5',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation

query_embeddings = str(list(model.encode(query)))

# 欧几里德距离
cur.execute(
    'SELECT keyword,1 - (keyword_embedding <-> %s) AS euclidean_distance FROM subkeyword ORDER BY  euclidean_distance DESC  LIMIT 5 ',
    (query_embeddings,))

neighbors = cur.fetchall()
for neighbor in neighbors:
    print(neighbor[0])


# 余弦相似度
cur.execute(
    'SELECT keyword,1 - (keyword_embedding <=> %s) AS cosine_similarity FROM subkeyword ORDER BY  cosine_similarity DESC  LIMIT 5 ',
    (query_embeddings,))
neighbors = cur.fetchall()
for neighbor in neighbors:
    print(neighbor[0])

# 曼哈顿距离
cur.execute(
    'SELECT keyword,1 - (keyword_embedding <#> %s) AS manhattan_distance FROM subkeyword ORDER BY  manhattan_distance DESC  LIMIT 5 ',
    (query_embeddings,))
neighbors = cur.fetchall()
for neighbor in neighbors:
    print(neighbor[0])

# 关闭游标
cur.close()

# 关闭连接
conn.close()
