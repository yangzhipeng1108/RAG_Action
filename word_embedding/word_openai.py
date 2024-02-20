import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(encoding.encode(string))
    return num_tokens


num_tokens = num_tokens_from_string("tiktoken is great!", "cl100k_base")
print(num_tokens)

num_tokens = num_tokens_from_string("我是谁,谁是我，我能做什么", "cl100k_base")

enc = tiktoken.encoding_for_model("gpt-4")

print(enc.encode('我是谁,谁是我，我能做什么'))

import openai
import numpy as np

# 首先需要设置OpenAI的API密钥
openai.api_key = "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"

# 定义要比较的两段文本
text1 = "The cat jumped over the lazy dog."
text2 = "The quick brown fox jumps over the lazy dog."

# 使用GPT-2模型对两段文本进行嵌入表示
embedding1 = openai.Embedding.create(model="text-embedding-ada-002", document=text1).vector
embedding2 = openai.Embedding.create(model="text-embedding-ada-002", document=text2).vector

# 计算两个向量的余弦相似度
cosine_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# 输出相似度
print("相似度为：", cosine_sim)

import openai
import os
from openai.embeddings_utils import cosine_similarity, get_embedding
embedding =  get_embedding("cat",engine="text-embedding-ada-002")
print(embedding)



# 导入 pandas 包。Pandas 是一个用于数据处理和分析的 Python 库，方便进行数据的读取、处理、分析等操作。
import pandas as pd
# 导入 tiktoken 库。Tiktoken 是 OpenAI 开发的一个库，用于从模型生成的文本中计算 token 数量。
import tiktoken
# 这个函数可以获取 GPT-3 模型生成的嵌入向量。
from openai.embeddings_utils import get_embedding

import openai
import os
# 从OPENAI_API_KEY环境变量中读取你的API密钥
openai.api_key = os.getenv("OPENAI_API_KEY")


# 模型类型建议使用官方推荐的第二代嵌入模型：text-embedding-ada-002
embedding_model = "text-embedding-ada-002"
# text-embedding-ada-002 模型对应的分词器（TOKENIZER）
embedding_encoding = "cl100k_base"

'''如OpenAI官方发布的 第二代模型：text-embedding-ada-002。它最长的输入是8191个tokens，输出的维度是1536。'''