# 在数据库服务器上安装 pgvector
# cd /tmp
# git clone --branch v0.4.2 https://github.com/pgvector/pgvector.git
# cd pgvector
# make
# make install # 可能需要sudo

import numpy as np


'''
在您的数据库中，运行此命令以启用扩展
CREATE EXTENSION IF NOT EXISTS vector;
创建一个存储向量的表
CREATE TABLE items (id bigserial PRIMARY KEY, name, features vector(3));
添加数据的工作原理如下
INSERT INTO items (features) VALUES ('[1,2,3]'), ('[4,5,6]');
由于 pgvector 构建在 postgres 之上，因此许多 PG DML 可用。例如。要更新插入，您可以运行
INSERT INTO items (id, features) VALUES (1, '[1,2,3]'), (2, '[4,5,6]')
2ON CONFLICT (id) DO UPDATE SET features = EXCLUDED.features;
'''


'''
<->：该运算符计算两个向量之间的欧几里德距离。欧几里德距离是多维空间中向量表示的点之间的直线距离。较小的欧几里德距离表示向量之间的相似性较大，因此该运算符在查找和排序相似项目时非常有用。
SELECT id, name, features, features <-> '[0.45, 0.4, 0.85]' as distance
2FROM items
3ORDER BY features <-> '[0.45, 0.4, 0.85]';
<=>：该运算符计算两个向量之间的余弦相似度。余弦相似度比较两个向量的方向而不是它们的大小。余弦相似度的范围在 -1 到 1 之间，1 表示向量相同，0 表示无关，-1 表示向量指向相反方向。
SELECT id, name, features, features <=> '[0.45, 0.4, 0.85]' as similarity
2FROM items
3ORDER BY features <=> '[0.45, 0.4, 0.85]' DESC;
<#>：该运算符计算两个向量之间的曼哈顿距离（也称为 L1 距离或城市街区距离）。曼哈顿距离是每个维度对应坐标差的绝对值之和。相对于欧几里德距离而言，曼哈顿距离更加强调沿着维度的较小移动。
SELECT id, name, features, features <#> '[0.45, 0.4, 0.85]' as distance
2FROM items
3ORDER BY features <#> '[0.45, 0.4, 0.85]';p'''

'''
4.3、pgvector索引
在 pgvector 中，可以通过添加索引来使用近似最近邻搜索，以提高查询性能。以下是一些关于 pgvector 索引的建议：

1）、在表中有一定数量的数据后创建索引：在创建索引之前，确保表中有足够的数据，以便索引能够提供更好的查询性能。

2）、选择适当数量的列表：可以根据表的大小来选择适当数量的列表。一般来说，可以使用表的行数除以 1000（最多 1M 行）和平方根(rows)（超过 1M 行）作为起点。

3）、指定适当的探针数量：在执行查询时，可以指定适当的探针数量来平衡查询速度和召回率。一般来说，可以使用列表数量除以 10（最多 1M 行）和平方根(lists)（超过 1M 行）作为起点。

这些建议可以帮助您在近似最近邻搜索中获得良好的准确性和性能。请注意，具体的索引配置可能需要根据您的数据和查询需求进行调整，以达到最佳性能。

BEGIN;
SET LOCAL ivfflat.probes = 10;
SELECT ...
COMMIT;
为您要使用的每个距离函数添加一个索引。

L2距离
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
内积
CREATE INDEX ON items USING ivfflat (embedding vector_ip_ops) WITH (lists = 100);
余弦距离
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
'''