import lda
from sklearn.svm import SVC
from datetime import datetime
from .createTrainingData import Word2Number
from .createTrainingData import ArticleList2Word
import json
import os

def predict(ini_topics, ini_iter, ini_random_state, ini_C, ini_kernel):
    # 加载数据
    X = np.loadtxt(os.path.abspath('./NLP/module') ,dtype=np.int64)
    with open(os.path.abspath('./NLP/tags') ,'r' , encoding='utf-8') as f:
        y = f.read().split()

    # 训练模型
    m_lda = lda.LDA(n_topics=ini_topics, n_iter=ini_iter, random_state=ini_random_state)
    m_lda.fit(X)
    d_t = m_lda.ndz_
    s = SVC(C = ini_C, kernel=ini_kernel)
    s.fit(d_t, y)

    # 预测未来
    vocabs = []
    with open(os.path.abspath('./NLP/vocabs'), 'r', encoding='utf-8') as f:
        vocabs = f.read().split('\n')
    current_date = datetime.now()
    current_date = str(current_date.year) + '.' + str(current_date.month) + '.' + str(current_date.day)
    # 获取当天新闻
    today_news = []
    for name in os.listdir(os.path.abspath('./spider/news')):
        with open(os.path.join(os.path.abspath('./spider/news') ,name), 'r', encoding='utf-8') as f:
            temp = json.load(f)
            if temp['time'] == current_date:
                today_news.append(temp)
    # 索引替换
    module = []
    for a in today_news:
        module.append(Word2Number(a, vocabs))
    # 模型预测
    return s.predict(np.array(module, dtype = np.int64))