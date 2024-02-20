import collections, functools, operator

# Initialising list of dictionary
ini_dict = [{'a': 5, 'b': 10, 'c': 90},
            {'a': 45, 'b': 78},
            {'a': 90, 'c': 10}]

# printing initial dictionary
print("initial dictionary", str(ini_dict))

# sum the values with same keys
result = dict(functools.reduce(operator.add,
                               map(collections.Counter, ini_dict)))

print("resultant dictionary : ", str(result))

# 欧几里德距离
title_json = {}
title_score = {}
query_result = {}
query_limit = str(query_limit)
fusion = 'sum'
cur.execute(
    'SELECT title,1 - (content_embedding <-> %s) AS euclidean_distance FROM subdocument ORDER BY  euclidean_distance DESC  LIMIT  CAST(%s AS integer)  ',
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
cur.execute(f'SELECT content  FROM documents where title in {query_title}')

neighbors = cur.fetchall()
for neighbor in neighbors:
    query_result[neighbor[0]] = title_score[neighbor[0]]

print(query_result)