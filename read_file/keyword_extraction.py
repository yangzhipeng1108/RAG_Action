from zhkeybert import KeyBERT, extract_kws_zh

docs = """时值10月25日抗美援朝纪念日，《长津湖》片方发布了“纪念中国人民志愿军抗美援朝出国作战71周年特别短片”，再次向伟大的志愿军致敬！
电影《长津湖》全情全景地还原了71年前抗美援朝战场上那场史诗战役，志愿军奋不顾身的英勇精神令观众感叹：“岁月峥嵘英雄不灭，丹心铁骨军魂永存！”影片上映以来票房屡创新高，目前突破53亿元，暂列中国影史票房总榜第三名。
值得一提的是，这部影片的很多主创或有军人的血脉，或有当兵的经历，或者家人是军人。提起这些他们也充满自豪，影片总监制黄建新称：“当兵以后会有一种特别能坚持的劲儿。”饰演雷公的胡军透露：“我父亲曾经参加过抗美援朝，还得了一个三等功。”影片历史顾问王树增表示：“我当了五十多年的兵，我的老部队就是上甘岭上下来的，那些老兵都是我的偶像。”
“身先士卒卫华夏家国，血战无畏护山河无恙。”片中饰演七连连长伍千里的吴京感叹：“要永远记住这些先烈们，他们给我们带来今天的和平。感谢他们的付出，才让我们有今天的幸福生活。”饰演新兵伍万里的易烊千玺表示：“战争的残酷、碾压式的伤害，其实我们现在的年轻人几乎很难能体会到，希望大家看完电影后能明白，是那些先辈们的牺牲奉献，换来了我们的现在。”
影片对战争群像的恢弘呈现，对个体命运的深切关怀，令许多观众无法控制自己的眼泪，观众称：“当看到影片中的惊险战斗场面，看到英雄们壮怀激烈的拼杀，为国捐躯的英勇无畏和无悔付出，我明白了为什么说今天的幸福生活来之不易。”（记者 王金跃）"""
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')
extract_kws_zh(docs, kw_model)



import os
import getpass
from langchain.chat_models import ChatOpenAI
os.environ['OPENAI_API_KEY'] = ''
llm=ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)

from keybert import KeyLLM, KeyBERT

# Load it in KeyLLM
kw_model = KeyBERT(llm=llm, model='BAAI/bge-large-zh-v1.5')
# Extract keywords
keywords = kw_model.extract_keywords(query, threshold=0.5)
print(keywords)

from sklearn.feature_extraction.text import CountVectorizer
import jieba


def tokenize_zh(text):
    words = jieba.lcut(text)
    return words


vectorizer = CountVectorizer(tokenizer=tokenize_zh)

from keybert import KeyBERT

kw_model = KeyBERT()
doc = "我爱北京天安门"
keywords = kw_model.extract_keywords(doc, vectorizer=vectorizer)
print(keywords)