from pgvector.psycopg2 import register_vector
import psycopg2
import psycopg2.extras
from FlagEmbedding import FlagModel

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="vector_demo",
    user="postgres",
    password="123456",
)

cur = conn.cursor()
cur.execute('CREATE EXTENSION IF NOT EXISTS vector')

from pgvector.psycopg2 import register_vector

register_vector(conn)

cur.execute('DROP TABLE IF EXISTS subdocument')
cur.execute(
    'CREATE TABLE subdocument (id bigserial PRIMARY KEY,title text , title_embedding vector(1024),content text,content_embedding vector(1024))')

conn.commit()

model = FlagModel('BAAI/bge-large-zh-v1.5',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation

insert_data = []

def pg_store_Subdocument(Subdocument_result_dict):
    for key in Subdocument_result_dict.keys():
        if len(Subdocument_result_dict[key]) > 1:
            key_list = [key] * len(Subdocument_result_dict[key])

            key_embeddings = model.encode(key_list)

            value_embeddings = model.encode(Subdocument_result_dict[key])
            inter_data = [(title, title_embedding, content, content_embedding) for
                          title, title_embedding, content, content_embedding in
                          zip(key_list, key_embeddings, Subdocument_result_dict[key], value_embeddings)]

            insert_data.extend(inter_data)
        elif len(Subdocument_result_dict[key]) == 0:
            pass
        else:
            title_embedding = model.encode([key])

            content_embedding = model.encode(Subdocument_result_dict[key])

            insert_data.append((key, str(list(title_embedding[0])), Subdocument_result_dict[key][0],
                         str(list(content_embedding[0]))))

f = open("Subdocument_result_dict.txt",encoding='utf-8')
line = f.readlines()
for value  in line :
    document_result_dict = eval(value)
    print(document_result_dict)
    pg_store_Subdocument(document_result_dict)

# 构造INSERT语句
insert_query = "INSERT INTO subdocument (title,title_embedding,content, content_embedding)  VALUES %s"

# 使用mogrify方法构造批量插入语句
psycopg2.extras.execute_values(cur, insert_query, insert_data)

cur.execute('CREATE INDEX  ON subdocument USING ivfflat(content_embedding vector_cosine_ops) WITH(lists = 1)')
conn.commit()

cur.execute('DROP TABLE IF EXISTS documents')
cur.execute(
    'CREATE TABLE documents (id bigserial PRIMARY KEY,title text , title_embedding vector(1024), content text, content_embedding vector(1024))')

conn.commit()
insert_document_data =[]
def pg_store_document(result_dict):
    for key in result_dict.keys():
        title_embedding = model.encode(key)

        content_embedding  = model.encode(result_dict[key])
        insert_document_data.append((key, str(list(title_embedding)), result_dict[key], str(list(content_embedding))))


f = open("document_result_dict.txt",encoding='utf-8')
line = f.readlines()
for value  in line:
    document_result_dict = eval(value)
    print(document_result_dict)
    i = pg_store_document(document_result_dict)

# 构造INSERT语句
insert_document_query = "INSERT INTO documents (title,title_embedding,content, content_embedding)  VALUES %s"

# 使用mogrify方法构造批量插入语句
psycopg2.extras.execute_values(cur, insert_document_query, insert_document_data)


cur.execute('CREATE INDEX  ON documents USING ivfflat(content_embedding vector_cosine_ops) WITH(lists = 1)')
conn.commit()
# 关闭游标
cur.close()

# 关闭连接
conn.close()
