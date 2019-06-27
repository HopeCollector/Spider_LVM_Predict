from .createTrainingData import createData
from .pridect import predict
import jieba
import os

jieba.load_userdict(os.path.abspath('./NLP/dic.dt'))
print('自然语言处理模块初始化完成')