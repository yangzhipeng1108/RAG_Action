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


query = 'The dog is barking'



model = FlagModel('BAAI/bge-large-zh-v1.5',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

tile_embedding = model.encode(query)


#欧几里德距离
neighbors = conn.execute('SELECT content,1 - (content_embedding <-> %(id)s)) AS euclidean_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 ', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])


#余弦相似度
neighbors = conn.execute('SELECT content,1 - (content_embedding <=> %(id)s)) AS cosine_similarity FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 ', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])

#曼哈顿距离
neighbors = conn.execute('SELECT content,1 - (content_embedding <#> %(id)s)) AS manhattan_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 ', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])


#欧几里德距离
neighbors = conn.execute('BEGIN; SET LOCAL ivfflat.probes = 10;SELECT content,1 - (content_embedding <-> %(id)s)) AS euclidean_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])


#余弦相似度
neighbors = conn.execute('BEGIN; SET LOCAL ivfflat.probes = 10;SELECT content,1 - (content_embedding <=> %(id)s)) AS cosine_similarity FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])

#曼哈顿距离
neighbors = conn.execute('BEGIN; SET LOCAL ivfflat.probes = 10;SELECT content,1 - (content_embedding <#> %(id)s)) AS manhattan_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])


#欧几里德距离
neighbors = conn.execute('BEGIN; SET LOCAL hnsw.ef_search = 100;SELECT content,1 - (content_embedding <-> %(id)s)) AS euclidean_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])


#余弦相似度
neighbors = conn.execute('BEGIN; SET LOCAL hnsw.ef_search = 100;SELECT content,1 - (content_embedding <=> %(id)s)) AS cosine_similarity FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])

#曼哈顿距离
neighbors = conn.execute('BEGIN; SET LOCAL hnsw.ef_search = 100;SELECT content,1 - (content_embedding <#> %(id)s)) AS manhattan_distance FROM Subdocument ORDER BY  cosine_similarity DESC  LIMIT 5 COMMIT;', {'id': query_embeddings}).fetchall()
for neighbor in neighbors:
    print(neighbor[0])
