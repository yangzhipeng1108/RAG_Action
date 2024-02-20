
#function1
from keybert import KeyLLM, KeyBERT

# Load it in KeyLLM
kw_model = KeyBERT(llm=llm, model='BAAI/bge-large-zh-v1.5')
# Extract keywords
keywords = kw_model.extract_keywords(documents, threshold=0.5)

#function2
from keybert import KeyLLM, KeyBERT
from transformers import AutoTokenizer, pipeline
from ctransformers import AutoModelForCausalLM
from pprint import pprint
from keybert.llm import TextGeneration


# 加速模型
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    gpu_layers=50,
    hf=True
)
# LLM的tokenizer
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
# LLM模型
generator = pipeline(
    model=model,
    tokenizer=tokenizer,
    task='text-generation',
    max_new_tokens=50,
    repetition_penalty=1.1
)

prompt = """
I have the following document:
* The website mentions that it only takes a couple of days to deliver but I still have not received mine
​
Extract 5 keywords from that document.
"""
response = generator(prompt)
print(response[0]["generated_text"])


# 实例提示模板
example_prompt = """
<s>[INST]
我有以下文档:
- 该网站提到只需几天即可交付，但我仍然没有收到我的

请提供本文档中出现的5个关键字，并用逗号分隔它们。
确保只返回关键字，不说其他内容。 例如，不要说：
"以下是文档中出现的关键字"
[/INST] 肉、牛肉、吃、喝、排放</s>"""
# 关键词提示模板
keyword_prompt = """
[INST]
我有以下文档:
- [DOCUMENT]

请提供本文档中出现的5个关键字，并用逗号分隔它们。
确保只返回关键字，不说其他内容。 例如，不要说：
"以下是文档中出现的关键字"
[/INST]
"""
prompt = example_prompt + keyword_prompt
# 使用语言模型+提示模板生成答案 利用原文和KeyLLM抽取的关键词，生成关键词列表
llm = TextGeneration(generator, prompt=prompt)
# Load it in KeyLLM 先对文档聚类，缩减文档数量，抽取出关键词
kw_model = KeyBERT(llm=llm, model='BAAI/bge-large-zh-v1.5')

"""
抽取流程：
  - 文档 -> KeyBERT -> 关键词列表1；
  - 文档+关键词列表1 -> KeyLLM -> 最终的关键词列表。
注意：
  - 输入文档的字数限制512
"""
# Extract keywords
documents = [
        "10月17日晚，新赛季WCBA揭幕战在四川省体育馆打响，志在卫冕的四川远达美乐女篮在主场103：90战胜浙江稠州银行女篮，取得卫冕路上的开门红。",
        "北京时间10月17日消息，中国男排国手张景胤已经前往俄罗斯别尔哥罗德狮子头俱乐部报道。本赛季是张景胤职业生涯第二次留洋。继上赛季中途加盟波超格但斯克俱乐部后，今年张景胤转战俄超为别尔哥罗德狮子头俱乐部效力。张景胤是第一位征战俄超联赛的中国球员。",
        "北京时间10月18日消息，世界羽联超级750级别的丹麦公开赛结束首日争夺，中国队拿到3胜4负的战绩，石宇奇、翁泓阳顺利过关，李诗沣、梁伟铿/王昶等遗憾一轮游。",
        "北京时间10月18日，辽宁男篮球星郭艾伦昨日更新微博，透露自己腿部伤病严重。郭艾伦昨晚8点42分在个人微博上写道：“人生总是充满坎坷”一名网友评论道：“哥你腿长，迈过去不成问题”郭艾伦则在这条评论下面回复道：“我腿完蛋了”",
        "北京时间10月18日，每日电讯报：纽卡斯尔已经准备好面对托纳利长期禁赛的结局。23岁的托纳利回到了意大利，这位今夏以5300万英镑从AC米兰加盟纽卡的中场可以自由训练，并将在周末与水晶宫的英超比赛中出场，但他仍然面临着令人震惊的调查。",
]
keywords = kw_model.extract_keywords(documents, threshold=0.5)
for keyword in keywords:
  print(keyword)


#function3
from keybert import KeyLLM
from sentence_transformers import SentenceTransformer

# Extract embeddings
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
embeddings = model.encode(documents, convert_to_tensor=True)

# Load it in KeyLLM
kw_model = KeyLLM(llm)

# Extract keywords
keywords = kw_model.extract_keywords(
    documents,
    embeddings=embeddings,
    threshold=.5
)


#function4
prompt = """
I have the following document:
* The website mentions that it only takes a couple of days to deliver but I still have not received mine
​
Extract 5 keywords from that document.
"""
response = generator(prompt)
print(response[0]["generated_text"])
