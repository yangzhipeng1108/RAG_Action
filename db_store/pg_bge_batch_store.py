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

Subdocument_result_dict = {'文件存储': ['银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。',
                                    '文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。'],

                           '文件存储 目录结构': [
                               '目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。',
                               '目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。',
                               '目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。',
                               '目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。',
                               '目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。']}

model = FlagModel('BAAI/bge-large-zh-v1.5',
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation

insert_data = []

def pg_store_Subdocument(Subdocument_result_dict):
    for key in Subdocument_result_dict.keys():
        print(key)
        if len(Subdocument_result_dict[key]) > 1:
            key_list = [key] * len(Subdocument_result_dict[key])
            print('-test-0')
            print(key_list)
            key_embeddings = model.encode(key_list)
            print('-test-1')

            value_embeddings = model.encode(Subdocument_result_dict[key])
            print('-test-2')
            inter_data = [(title, title_embedding, content, content_embedding) for
                          title, title_embedding, content, content_embedding in
                          zip(key_list, key_embeddings, Subdocument_result_dict[key], value_embeddings)]
            print('-test-3')
            insert_data.extend(inter_data)
        else:
            title_embedding = model.encode([key])

            content_embedding = model.encode(Subdocument_result_dict[key])

            insert_data.append((key, str(list(title_embedding[0])), Subdocument_result_dict[key][0],
                         str(list(content_embedding[0]))))

pg_store_Subdocument(Subdocument_result_dict)

# 构造INSERT语句
insert_query = "INSERT INTO subdocument (title,title_embedding,content, content_embedding)  VALUES %s"

# 使用mogrify方法构造批量插入语句
psycopg2.extras.execute_values(cur, insert_query, insert_data)

cur.execute('CREATE INDEX  ON subdocument USING ivfflat(content_embedding vector_cosine_ops) WITH(lists = 1)')


cur.execute('DROP TABLE IF EXISTS documents')
cur.execute(
    'CREATE TABLE documents (id bigserial PRIMARY KEY,title text , title_embedding vector(1024), content text, content_embedding vector(1024))')

document_result_dict = {
    '文件存储': '银汉智算平台采用 CephFS 作为后端存储系统，CephFS是一个支持POSIX接口的文件系统，它使用ceph存储集群来存储数据。文件系统对于客户端来说可以方便的挂载至本地使用。CephFS构建在RADOS之上，继承RADOS的容错性和扩展性，支持多副本，保障数据的高可靠性。',
    '文件存储 目录结构': '目录 /    名称 系统盘    容量限制 20GB    说明 一般系统依赖以及python安装包都会安装在系统盘下，也可以存放代码等小容量的数据。系统盘数据可通过“固化为镜像”操作，保存至自有镜像中。注意：请不要在“/”目录下创建文件夹和文件，否则重启后文件会消失。 目录 /root/tmp    名称 缓存盘    容量限制 20GB    说明 可存放读写IO要求高的缓存数据。实例关机数据保留七天，连续关机七天后将删除缓存数据。在有效期内重新开机，也可能会因为原容器实例所在节点的资源不足等原因（例如GPU卡不足），而导致缓存盘数据丢失。 目录 /root/nas-private    名称 个人网盘    容量限制 100GB    说明 持久化数据盘，用户级独享。在同一个区域，个人网盘对该用户的不同实例可见，并且文件可读可写。 目录 /root/nas-share    名称 共享网盘    容量限制 500GB    说明 持久化数据盘，客户级共享。在同一个区域，共享网盘对该客户下所有用户的不同实例可见，并且文件可读可写。 目录 /root/nas-public    名称 公共数据盘    容量限制 无    说明 平台常用公共数据集的存放目录。文件只读。'}

insert_document_data =[]
def pg_store_document(result_dict):
    for key in result_dict.keys():
        print(key)
        title_embedding = model.encode(key)

        content_embedding  = model.encode(result_dict[key])
        insert_document_data.append((key, str(list(title_embedding)), result_dict[key], str(list(content_embedding))))


pg_store_document(document_result_dict)

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
