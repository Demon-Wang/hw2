# -*- coding: utf-8 -*-
import jieba
from flask import Blueprint,request,render_template
import math
import os
sim=Blueprint('sim',__name__)
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
stopwords = stopwordslist(os.path.join(os.path.dirname(__file__),'stopwords.txt'))
@sim.route('/',methods=['GET','POST'])
def fun():
    if request.method=='POST':
        one=request.form['one']
        two=request.form['two']
        # 结巴分词并去掉stopwords
        tem1 = jieba.cut_for_search(one, HMM=False)
        tem2 = jieba.cut_for_search(two, HMM=False)
        word1=[]
        worl2=[]
        for value in tem1:
            if(value in stopwords):
                continue
            word1.append(value)
        for value in tem2:
            if(value in stopwords):
                continue
            worl2.append(value)

        result_transvection_1 = transvection_1(word1, worl2)
        result_transvection_2, result_cos, result_jaccard = similarity(word1, worl2)
        return render_template('sim.html', message='结果如下',result_cos=result_cos,
                               result_transvection_1=result_transvection_1,
                               result_transvection_2=result_transvection_2,
                               result_jaccard=result_jaccard)
    else:
        return render_template('sim.html')
@sim.route('/<int:id>', methods=['GET'])
def news_page(id):
    new={}
    count=0
    content=[]
    BASE_DIR = os.path.dirname(__file__)
    file_dir = os.path.join(BASE_DIR, 'jianshu_big/')
    # 计算所选文档的各个单词的tf
    with open(file_dir + str(id), 'r', encoding='utf-8') as f:
        while True:
            words = f.readline()
            if words:
                new[words]=new.get(words,0.0)+1.0
            else:
                break
        for key in new:
            new[key] /= (len(new) * 1.0)
        for e in (1,90):
            if e==id:
                continue;
            for key in new:
                count=1
                with open(file_dir + str(e), 'r', encoding='utf-8') as g:
                    while True:
                        word=g.readline()
                        if word:
                            if(word==key):
                                count+=1
                        else:
                            break
    for key in new:
        content.append(key+"tf:"+str(new[key])+" idf:"+str(math.log10(90.0 / count))+" tfidf:"+str(new[key]/math.log10(90.0 / count))+"\n")
    return render_template('article.html',id=id,content=content)

# 计算内积（二值）
def transvection_1(seg_list_1, seg_list_2):
    seg_1 = set(seg_list_1)
    seg_2 = set(seg_list_2)

    count = 0.0
    for s in seg_1:
        if s in seg_2:
            count += 1.0

    return count


# 计算内积（加权）、余弦、Jaccard
def similarity(seg_list_1, seg_list_2):
    seg_1 = {}
    seg_2 = {}

    # 统计第一句话中每个词出现的数量
    for word in seg_list_1:
        try:
            seg_1[word] += 1.0
        except:
            seg_1[word] = 1.0

    # 统计第二句话中每个词出现的数量
    for word in seg_list_2:
        try:
            seg_2[word] += 1.0
        except:
            seg_2[word] = 1.0

    # 计算内积（加权）
    result_transvection_2 = 0.0
    # 计算向量模长
    cos_denominator_1 = 0.0
    cos_denominator_2 = 0.0
    for key in seg_1:
        try:
            result_transvection_2 += (seg_1[key] * seg_2[key])
        except:
            pass
        cos_denominator_1 += seg_1[key] ** 2

    for key in seg_2:
        cos_denominator_2 += seg_2[key] ** 2
    # 计算余弦
    result_cos = result_transvection_2 / (cos_denominator_1 * cos_denominator_2) ** 0.5
    # 计算Jaccard
    result_jaccard = result_transvection_2 / (cos_denominator_1 + cos_denominator_2 - result_transvection_2)
    return result_transvection_2, result_cos, result_jaccard