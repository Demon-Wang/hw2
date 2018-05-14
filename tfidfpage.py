# -*- coding: utf-8 -*-
import jieba
import os

import math
from flask import Blueprint,request,render_template
tfidf=Blueprint('tfidf',__name__)
@tfidf.route('/',methods=['GET','POST'])
def compute():
    if request.method == 'POST':
        # 获取上传的文档文件保存为test.txt并运行tfidf计算函数
        file=request.files['file']
        file.save(os.path.join(os.path.dirname(__file__),'test.txt'))
        result=tfidf_calc(os.path.dirname(__file__),'test.txt')
        return render_template('tfidf.html',result=result,message="结果如下")
    else:
        return render_template('tfidf.html')

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
stopwords = stopwordslist(os.path.join(os.path.dirname(__file__),'stopwords.txt'))
def tfidf_calc(path,filename):
    with open(os.path.join(path,filename), 'r',encoding='utf-8') as f:
        data = f.read()
    seg_list = jieba.cut_for_search(data, HMM=False)
    word_count = {}  # 计算上传的文本中每个词语的数量
    text_count = {}  # 计算每个词语出现在语料库的多少文本中
    tfidf_result = {}  # 计算结果
    word_sum = 0.0  # 计算文本的总的词数量
    text_sum = 90.0  # 语料库中总的文本数量
    for word in list(seg_list):
        # 去掉停用词
        if (word == '\n' or word == ' ' or word in stopwords):
            continue
        try:
            word_count[word] += 1.0
        except:
            word_count[word] = 1.0
            text_count[word] = 1.0
        word_sum += 1.0
    for i in range(1, 90):
        word_set = set()  # 语料库每个文本的词语集合
        with open(os.path.dirname(__file__) + '/jianshu_big/' + str(i),
                  'r',encoding='utf-8') as f:
            while True:
                words = f.readline()
                if words:
                    word_set.add(words.strip())
                else:
                    break

                # 计算上传文本的每个词出现在语料库的多少文件中
        for key in text_count:
            if key in word_set:
                text_count[key] += 1.0
    result = []
    # 计算上传文本每个词的TFIDF并写入文件
    with open(os.path.join(os.path.dirname(__file__), '5.txt'),'a',encoding='utf-8') as w:
        for key in word_count:
            tfidf_result[key] = (word_count[key] / word_sum) * \
                                math.log10(text_sum / text_count[key])
            re = key + '---' + str(tfidf_result[key])
            w.write(re + '\n')
            result.append(re)
    return result
