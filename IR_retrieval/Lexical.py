
'''
在论文中提出三种方法来构建过滤模型（
 ）的监督数据，分别为StrInc，CXMI，Lexical。本次采用的是Lexical方法，因为发现用StrInc方法命中的数据条数太少，CXMI需要用大模型来预测判断，过于麻烦。

1）对采集的text，abstract字段进行清洗；

2）对text+abstract内容进行切片，切片（seg）最大长度为128；

3）利用jieba对answer进行关键词抽取，判断answer关键词在seg占比，作为排序分数；

4）对每个seg按分数降序排序，取第一条seg为要筛选出的检索数据，其他作为检索内容；
'''

import jieba

def extract_keywords(a):
    """利用jieba进行关键词识别，并过滤掉标点符号"""
    keywords = set()
    pun_list =['。' ,'，' ,'.' ,',' ,'？' ,'!' ,'《' ,'》' ,'<' ,'>' ,'_' ,'-' ,'“' ,'”' ,'"' ,'\t' ,'\n' ,'（' ,'）']
    for w in jieba.cut(a ,HMM=True):
        if w in pun_list:
            continue
        keywords.add(w)
    return list(keywords)

def judge_p1(seg ,keywords):
    """判断答案中的关键词在检索片段出现的比例，作为排序分数"""
    score = 0
    for kw in keywords:
        if kw in seg:
            score += 1
    return score / len(keywords)


max_seq = 128  # 检索片段的最大长度
maxlen = 1212  # 所有检索片段的最大长度
data = []
with open(r'E:\mygithub\LLM-RAG-QA\data\pkumod-ccks_query_list_crawl2.json' ,'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = json.loads(line)
        q = line['query']
        a = line['answer']
        keywords = extract_keywords(a)
        seg_list = {}
        for item in line['crawl']:
            abstract =item['abstract']
            text = item['text']
            abstract = clean_abstract(abstract)
            text = clean_text(text)
            content = abstract + '\n' + text
            for seg in text_segmentate(content, max_seq, seps='\n'):
                if len(seg) > 32:
                    seg = re.sub('\n', '', seg)
                    seg = seg.strip('。|，|；')
                    score = judge_p1(seg, keywords)
                    seg_list[seg] = score
        if len(seg_list) <= 1:
            continue

        seg_list = sorted(seg_list.items(), key=lambda x: x[1], reverse=True)
        if seg_list[0][1] < 0.6:
            continue

        r_list = [s[0] for s in seg_list]
        r_list = truncation_text(r_list, maxlen)
        random.shuffle(r_list)
        tmp = {}
        tmp['query'] = q
        tmp['answer'] = a
        tmp['select_segment'] = seg_list[0][0]
        tmp['recall_segment'] = r_list
        data.append(tmp)