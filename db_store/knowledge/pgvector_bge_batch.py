# 使用批量插入可以显著提高插入数据的速度。以下是使用Psycopg2和PostgreSQL进行批量插入的最快方式。
#
# 步骤1：使用COPY命令
#
# 使用COPY命令将数据从文件或内存中批量插入到PostgreSQL数据库中。您可以在Python代码中使用Psycopg2库执行此操作。以下是使用COPY命令批量插入数据的示例代码。
#
# ```python
import psycopg2

#连接到PostgreSQL数据库
conn = psycopg2.connect(database="testdb", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

#创建一个临时表
cur.execute("CREATE TEMP TABLE temp_table (id INT, name TEXT)")

#将数据加载到临时表中
with open('data.csv', 'r') as f:
    cur.copy_from(f, 'temp_table', sep=',')

#将数据从临时表插入到目标表中
cur.execute("INSERT INTO target_table SELECT * FROM temp_table")

#提交事务
conn.commit()
# ```
#
# 步骤2：使用批量插入语句
#
# 如果您没有文件或内存中的数据，而是要从Python列表中插入数据，那么使用批量插入语句将是最快的方法。以下是使用批量插入语句批量插入数据的示例代码。
#
# ```python
import psycopg2

#连接到PostgreSQL数据库
conn = psycopg2.connect(database="testdb", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

#准备数据
data = [(1, 'name1'), (2, 'name2'), (3, 'name3')]

#构造INSERT语句
insert_query = "INSERT INTO target_table (id, name) VALUES %s"

#使用mogrify方法构造批量插入语句
psycopg2.extras.execute_values(cur, insert_query, data)

#提交事务
conn.commit()
# ```
#
# 在上面的代码中，使用了Psycopg2库的execute_values方法，它使用mogrify方法构造批量插入语句，并将数据一次性插入到目标表中。这比执行单个INSERT语句多次要快得多。
