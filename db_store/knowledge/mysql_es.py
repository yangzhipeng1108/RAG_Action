from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time

# 连接ES
es = Elasticsearch(
    ['127.0.0.1'],
    port=9200
)

# 连接MySQL
print("Connect to mysql...")
mysql_db = "test"
m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

try:
    num_id = 0
    while True:
        s = time.time()
        # 查询数据
        sql = "select name,age,area from testTable LIMIT {}, 100000".format(num_id*100000)
        # 这里假设查询出来的结果为 张三 26 北京
        m_cursor.execute(sql)
        query_results = m_cursor.fetchall()

        if not query_results:
            print("MySQL查询结果为空 num_id=<{}>".format(num_id))
            break
        else:
            actions = []
            for line in query_results:
            # 拼接插入数据结构
                action = {
                    "_index": "company_base_info_2",
                    "_type": "company_info",
                    "_source": {
                        "name": line[0],
                        "age": line[1],
                        "area": line[2],
                    }
                }
				# 形成一个长度与查询结果数量相等的列表
                actions.append(action)
            # 批量插入
            a = helpers.bulk(es, actions)
            e = time.time()
            print("{} {}s".format(a, e-s))
        num_id += 1

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")
