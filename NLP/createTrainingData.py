# 制作训练集
import jieba
import numpy as np
import os
import json


punct = set(''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_… ''')

def Word2Number(article, vocabs):
    num_art = []
    print('正在替换 ' + article['title'] + ' ...')
    article['text'] = ''.join(filter(lambda x: x not in punct, article['text']))
    vocabs_temp = jieba.lcut(article['text'])
    for vocab in vocabs_temp:
        if vocab in vocabs:
            num_art.append(vocabs.index(vocab))
    return num_art

def ArticleList2Word(names):
    vocabs = []
    for name in names:
        print('正在分析 ' + name + '  ...')
        with open(os.path.join(os.path.abspath('./spider/news'), name), 'r', encoding='utf-8') as f:
            article = json.load(f)
        article['text'] = ''.join(filter(lambda x: x not in punct, article['text']))
        # 分词
        for vocab in jieba.lcut(article['text']):
            if '' == vocab or '\u3000' == vocab or ' ' == vocab:
                continue
            # 将词加入列表
            if not vocab in vocabs:
                vocabs.append(vocab)
    return vocabs
                
def createData():
    module = []
    tags = []
    max_len = 0
    names = os.listdir(os.path.abspath('./spider/news'))
    vocabs = ArticleList2Word(names) # 将所有文章分词, 将所有词加入列表
    # 将文章里面的词替换成列表里面的索引，顺便存个标签  
    for name in names:
        with open(os.path.join(os.path.abspath('./spider/news'), name), 'r', encoding='utf-8') as f:
            article = json.load(f)
        module.append(Word2Number(article, vocabs))
        tags.append(str(article['tag']))
        if max_len < len(module[-1]):
            max_len = len(module[-1])
    for article in module:
        if max_len > len(article):
            for i in range(0, max_len - len(article)):
                article.append(0)

    with open(os.path.abspath('./NLP/titles'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(names))
    print('文章名列表 - 保存成功')


    with open(os.path.abspath('./NLP/vocabs'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(vocabs))
    print('词汇列表 - 保存成功')

    with open(os.path.abspath('./NLP/tags'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(tags))
    print('文章标签 - 保存成功')

    np.savetxt(os.path.abspath('./NLP/module'), np.array(module, dtype=np.int64),fmt = '%i')
    print('文章模型 - 保存成功')

if __name__ == '__main__':
    import __init__
    createTrainingData()