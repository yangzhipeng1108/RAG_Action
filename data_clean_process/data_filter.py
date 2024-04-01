import jieba
import re
from cutword import Cutter
cutter = Cutter()

def calculate_duplicate_word_rate(text):
    # 将文本拆分成单词
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）|\n'
    result_list = list(filter(lambda x: False if x == ''  else True ,re.split(pattern, text)))

    word_list = []
    for item in result_list:
        word_list.extend(jieba.cut(item))

    # for item in result_list:
    #     word_list.extend(cutter.cutword(item))

    total_words = len(word_list)

    # 使用集合来记录不重复的单词
    unique_words = set(word_list)
    unique_word_count = len(unique_words)

    # 计算重复率
    duplicate_rate = 1 - (unique_word_count / total_words)

    return duplicate_rate



def calculate_duplicate_character_rate(text):
    # 将文本拆分成单词
    pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）|\n'
    result_list = list(filter(lambda x: False if x == ''  else True ,re.split(pattern, text)))

    word_list = []
    for item in result_list:
        word_list.extend(list(item))

    total_words = len(word_list)

    # 使用集合来记录不重复的单词
    unique_words = set(word_list)
    unique_word_count = len(unique_words)

    # 计算重复率
    duplicate_rate = 1 - (unique_word_count / total_words)

    return duplicate_rate


def count_special_characters(text):
    special_characters = "!@#$%^&*()-_+={}[]|\:;\"'<>,.?/~`\n"
    special_count = 0
    total_characters = len(text)
    print(total_characters)

    for char in text:
        if char in special_characters:
            special_count += 1

    return special_count, total_characters


def calculate_special_character_percentage(text):
    special_count, total_characters = count_special_characters(text)
    percentage = (special_count / total_characters) * 100
    return percentage


import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def calculate_perplexity(document):
    # 加载预训练的GPT-2模型和分词器
    model_path = "gpt2-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True)

    # 将文档编码成tokens
    input_ids = tokenizer.encode(document, return_tensors="pt")

    # 使用模型计算困惑度
    with torch.no_grad():
        output = model(input_ids=input_ids, labels=input_ids)

    # 计算困惑度
    loss = output.loss
    perplexity = torch.exp(loss)

    return perplexity.item()


def calculate_word_len(text):
    # 将文本拆分成单词
    total_len = len(text)
    if total_len < 100:
        return None

    return text

# 示例文本
document = """
这是一个示例文档，其中包含一些重复的词语。
重复的词语会影响文档的独特性和字重复率。
我们将使用Python算法来计算文档的字重复率。
"""

# 计算重复率
rate = calculate_special_character_percentage(document)
print("文档的字重复率：", rate)
