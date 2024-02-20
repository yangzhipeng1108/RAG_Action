import psycopg2
import numpy as np
# 连接到数据库
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="vector_demo",
    user="postgres",
    password="123456",
)

# 创建游标
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS subdocument')
cur.execute("CREATE TABLE subdocument (id bigserial PRIMARY KEY,tile text , tile_embedding vector(1024),content text,content_embedding vector(1024))")
# 执行查询

embedding = [6, 7, 8]
cur.execute('INSERT INTO items (embedding) VALUES (%s)', (embedding,))

cur.execute("SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
conn.commit()
# 获取结果
results = cur.fetchall()
print(results)

# 关闭游标
cur.close()

# 关闭连接
conn.close()