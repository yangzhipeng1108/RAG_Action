from openai import OpenAI
from pgvector.psycopg import register_vector
import psycopg

conn = psycopg.connect(dbname='pgvector_example', autocommit=True)

conn = psycopg.connect(
            dbname="your_database_name",
            user="your_database_user",
            password="your_database_password",
            host="your_database_host",
            port="your_database_port"
        )

conn.execute('CREATE EXTENSION IF NOT EXISTS vector')

query = [
    'The dog is barking',
]

client = OpenAI()

query_response = client.embeddings.create(input=query, model='text-embedding-3-small')
query_embeddings = [v.embedding for v in query_response.data]


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
