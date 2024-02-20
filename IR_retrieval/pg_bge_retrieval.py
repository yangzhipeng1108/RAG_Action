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



def pg_qa_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5):
    # 欧几里德距离
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode =='euclidean_distance':
        cur.execute(
            'SELECT answer,1 - (question_embedding <-> %s) AS euclidean_distance FROM qa_store ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer) ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT answer,1 - (question_embedding <=> %s) AS cosine_similarity FROM qa_store ORDER BY  cosine_similarity DESC   LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT answer,1 - (question_embedding <#> %s) AS manhattan_distance FROM qa_store ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]
    return  query_result


def pg_answer_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5):
    # 欧几里德距离
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode == 'euclidean_distance':
        cur.execute(
            'SELECT answer,1 - (answer_embedding <-> %s) AS euclidean_distance FROM answer_store ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT answer,1 - (answer_embedding <=> %s) AS cosine_similarity FROM answer_store ORDER BY  cosine_similarity DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT answer,1 - (answer_embedding <#> %s) AS manhattan_distance FROM answer_store ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]
    return query_result


def pg_subdocument_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5):
    # 欧几里德距离
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode == 'euclidean_distance':
        cur.execute(
            'SELECT content,1 - (content_embedding <-> %s) AS euclidean_distance FROM subdocument ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT content,1 - (content_embedding <=> %s) AS cosine_similarity FROM subdocument ORDER BY  cosine_similarity DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT content,1 - (content_embedding <#> %s) AS manhattan_distance FROM subdocument ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings,query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            query_result[neighbor[0]] = neighbors[1]
    return query_result


def pg_document_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5,fusion='sum'):
    # 欧几里德距离
    title_json = {}
    title_score = {}
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode == 'euclidean_distance':
        cur.execute(
            'SELECT title,1 - (content_embedding <-> %s) AS euclidean_distance FROM subdocument ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT title,1 - (content_embedding <=> %s) AS cosine_similarity FROM subdocument ORDER BY  cosine_similarity DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT title,1 - (content_embedding <#> %s) AS manhattan_distance FROM subdocument ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    for key,item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    query_title = list(title_score.keys())

    query_final_result = {}
    cur.execute("SELECT title,content  FROM documents where title in  %s",(tuple(query_title),))

    neighbors = cur.fetchall()
    for neighbor in neighbors:
        query_result[neighbor[1]] = title_score[neighbor[0]]

    return query_result


def pg_keyword_subdocument_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5,fusion='sum'):
    # 欧几里德距离
    title_json = {}
    title_score = {}
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode == 'euclidean_distance':
        cur.execute(
            'SELECT title,1 - (keyword_embedding <-> %s) AS euclidean_distance FROM subkeyword ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT title,1 - (keyword_embedding <=> %s) AS cosine_similarity FROM subkeyword ORDER BY  cosine_similarity DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT title,1 - (keyword_embedding <#> %s) AS manhattan_distance FROM subkeyword ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    for key, item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    query_title = list(title_score.keys())

    query_final_result = {}
    cur.execute("SELECT title,content  FROM subdocument where title in %s",(tuple(query_title),))

    neighbors = cur.fetchall()
    for neighbor in neighbors:
        query_result[neighbor[1]] = title_score[neighbor[0]]

    return query_result



def pg_keyword_document_bge_retrieval(query_embeddings,inquiry_mode='euclidean_distance',query_limit = 5,fusion='sum'):
    # 欧几里德距离
    title_json = {}
    title_score = {}
    query_result = {}
    query_limit = str(query_limit)
    if inquiry_mode == 'euclidean_distance':
        cur.execute(
            'SELECT title,1 - (keyword_embedding <-> %s) AS euclidean_distance FROM subkeyword ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'cosine_similarity':
        # 余弦相似度
        cur.execute(
            'SELECT title,1 - (keyword_embedding <=> %s) AS cosine_similarity FROM subkeyword ORDER BY  cosine_similarity DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    elif inquiry_mode == 'manhattan_distance':
        # 曼哈顿距离
        cur.execute(
            'SELECT title,1 - (keyword_embedding <#> %s) AS manhattan_distance FROM subkeyword ORDER BY  manhattan_distance DESC  LIMIT  CAST(%s AS integer)  ',
            (query_embeddings, query_limit))

        neighbors = cur.fetchall()
        for neighbor in neighbors:
            if neighbor[0] not in title_json:
                title_json[neighbor[0]] = []
            title_json[neighbor[0]].append(neighbor[1])

    for key, item in title_json.items():
        if fusion == 'sum':
            title_score[key] = sum(item)
        elif fusion == 'avg':
            title_score[key] = sum(item) / len(item)
    query_title = list(title_score.keys())

    query_final_result = {}
    cur.execute("SELECT title,content  FROM documents where title in  %s",(tuple(query_title),))

    neighbors = cur.fetchall()
    for neighbor in neighbors:
        query_result[neighbor[1]] = title_score[neighbor[0]]

    return query_result


# 关闭游标
cur.close()

# 关闭连接
conn.close()
