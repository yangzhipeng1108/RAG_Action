from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import  davies_bouldin_score

# 使用 TfidfVectorizer 将文档转换为数值特征向量
vectorizer = TfidfVectorizer()

documents = ["This is the first document.", "This document is the second document.", "And this is the third one.", "Is this the first document?"]

# 将文本转换为数值特征向量
X = vectorizer.fit_transform(documents)

# 初始化一个指定簇数的 KMeans 模型
kmeans = KMeans(n_clusters=3)

# 在特征向量上拟合 KMeans 模型
kmeans.fit(X)

# 预测每个文档的簇标签
labels = kmeans.predict(X)
print(labels)
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import io
from sklearn import metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import  davies_bouldin_score

# 使用 TfidfVectorizer 将文档转换为数值特征向量
vectorizer = TfidfVectorizer()

# with io.open("aaa.txt", "r", encoding="utf-8") as f:
#     text = f.read()
documents = ["This is the first document.", "This document is the second document.", "And this is the third one.", "Is this the first document?"]

# 将文本转换为数值特征向量
X = vectorizer.fit_transform(documents)

# 初始化一个指定簇数的 KMeans 模型
kmeans = KMeans(n_clusters=3)

# 在特征向量上拟合 KMeans 模型
kmeans.fit(X)

# 预测每个文档的簇标签
labels = kmeans.predict(X)

# 三种评估指标
score = silhouette_score(X, labels)
ch_score = metrics.calinski_harabasz_score(X.toarray(), kmeans.labels_)
davies_bouldin_score = davies_bouldin_score(X.toarray(), kmeans.labels_)

print("Calinski-Harabasz指数：", ch_score)
print("轮廓系数评分为：", score)
print("Davies-Bouldin指数评分：", davies_bouldin_score)



