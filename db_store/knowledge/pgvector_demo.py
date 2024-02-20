import psycopg2


def connect_to_database():
    # 连接到数据库
    try:
        conn = psycopg2.connect(
            database="your_database_name",
            user="your_database_user",
            password="your_database_password",
            host="your_database_host",
            port="your_database_port"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def close_database_connection(conn):
    # 关闭数据库连接
    if conn:
        conn.close()


def create_extension(conn, extension_name):
    try:
        cursor = conn.cursor()
        # 执行插入操作
        cursor.execute('create extension if not exists %s ;' % extension_name)
        conn.commit()
        cursor.close()
        print("extension %s has been created successfully." % extension_name)
    except psycopg2.Error as e:
        print(f"Error create extension: {e}")


def create_table(conn, tablename, sql_tabledef):
    try:
        cursor = conn.cursor()
        # 创建向量表
        cursor.execute(sql_tabledef)
        conn.commit()
        cursor.close
        print('table %s has been created successfully.' % tablename)
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")


def insert_data(conn, tablename, data):
    try:
        cursor = conn.cursor()
        # 执行插入操作
        cursor.execute("INSERT INTO %s VALUES ('%s',%s, %s,'%s')" % (
            tablename, data['value1'], data['value2'], data['value3'], data['value4']))
        conn.commit()
        cursor.close()
        print("Data inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")


def select_data(conn, tablename):
    try:
        cursor = conn.cursor()
        # 执行查询操作
        cursor.execute("SELECT * FROM %s" % tablename)
        result = cursor.fetchall()
        cursor.close()
        return result
    except psycopg2.Error as e:
        print(f"Error selecting data: {e}")
        return []


def vector_search(conn, tablename, vector_type, nearest_values):
    try:
        cursor = conn.cursor()
        # 执行查询操作
        cursor.execute(
            "SELECT * FROM %s order by embedding %s '%s' limit 5;" % (tablename, vector_type, nearest_values))
        result = cursor.fetchall()
        cursor.close()
        return result
    except psycopg2.Error as e:
        print(f"Error selecting data: {e}")
        return []


def update_data(conn, tablename, data):
    try:
        cursor = conn.cursor()
        # 执行更新操作
        cursor.execute(
            "UPDATE %s SET embedding = '%s' WHERE id = %s" % (tablename, data['new_value'], data['condition']))
        conn.commit()
        cursor.close()
        print("Data updated successfully.")
    except psycopg2.Error as e:
        print(f"Error updating data: {e}")


def delete_data(conn, tablename, condition):
    try:
        cursor = conn.cursor()
        # 执行删除操作
        cursor.execute("DELETE FROM %s WHERE id = %s" % (tablename, condition))
        conn.commit()
        cursor.close()
        print("Data deleted successfully.")
    except psycopg2.Error as e:
        print(f"Error deleting data: {e}")


if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        # 在这里执行数据库操作
        data_to_insert = {
            'value1': '2023-10-12 00:00:00',
            'value2': 1,
            'value3': 1,
            'value4': [1, 2, 3]

        }

        # 创建vector扩展
        create_extension(conn, 'vector')

        # 创建向量表
        sql_tabledef = 'drop table if exists documents_l2;' \
                       'CREATE TABLE documents_l2(' \
                       'created_at timestamptz,' \
                       'id integer,' \
                       'document_type int,' \
                       'embedding vector(3)' \
                       ')' \
                       'distributed by (id);';
        create_table(conn, 'documents_l2', sql_tabledef)

        # 向表里写入数据
        insert_data(conn, 'documents_l2', data_to_insert)

        # 查询数据
        data_to_select = select_data(conn, 'documents_l2')
        print("Selected Data:", data_to_select)

        # 更新数据
        data_to_update = {
            'new_value': '[4,5,6]',
            'condition': 1
        }
        update_data(conn, 'documents_l2', data_to_update)
        # 查询数据
        data_to_select = select_data(conn, 'documents_l2')
        print("Selected Data:", data_to_select)

        # 向量检索
        print('向量检索：L2 distance')
        data_vector_search = vector_search(conn, 'documents_l2', '<->', '[4,5,6]')
        print("vector search（L2）:", data_vector_search)

        print('向量检索：inner product')
        data_vector_search = vector_search(conn, 'documents_l2', '<#>', '[4,5,6]')
        print("vector search(IP):", data_vector_search)

        print('向量检索：cosine distance')
        data_vector_search = vector_search(conn, 'documents_l2', '<=>', '[4,5,6]')
        print("vector search(cos):", data_vector_search)

        # 删除数据
        data_to_delete = 1
        delete_data(conn, 'documents_l2', data_to_delete)
        # 查询数据
        data_to_select = select_data(conn, 'documents_l2')
        print("Selected Data:", data_to_select)

        close_database_connection(conn)