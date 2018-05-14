# -*- coding: utf-8 -*-
import jieba
import math
from flask import Blueprint,request,render_template
import os
sjet=Blueprint('sjet',__name__)

@sjet.route('/',methods=['GET','POST'])
def fun1():
    if request.method=='POST':
        query = request.form['content']
        BASE_DIR = os.path.dirname(__file__)
        file_dir = os.path.join(BASE_DIR, 'jianshu_big/')
        results = []  # 保存每篇文章信息以及与query的相似度:id title 内容 相似度
        words_count = []  # 保存每篇文章每个词的tf值
        stopwords = stopwordslist(os.path.join(os.path.dirname(__file__), 'stopwords.txt'))
        for i in range(1, 91):
            with open(file_dir + str(i) + '.txt', 'r',encoding='utf-8') as f:
                news = []
                news.append(i)
                title = f.readline()
                news.append(title.strip())
                content = ''
                while True:
                    words = f.readline()
                    if words:
                        if words == '\n' or words == ' ' or words in stopwords:
                            continue
                        content += words.strip()
                    else:
                        break
                seg_list = jieba.cut_for_search(title + content, HMM=False)
                #计算query每个单词tf
                wc = {}
                seg_l = list(seg_list)
                for word in seg_l:
                    wc[word] = (wc.get(word, 0.0) + 1.0)
                for key in wc:
                    wc[key] /= (len(seg_l) * 1.0)
                words_count.append(wc)
                news.append(content)
                results.append(news)
        seg_list = jieba.cut_for_search(query, HMM=False)
        words_in_query = list(seg_list)
        tfidf_in_query = {}
        # 计算query word的tf值
        for word in words_in_query:
            if word == '\n' or word == ' ' or word in stopwords:
                continue
            word = word.strip()
            if len(word) > 0:
                tfidf_in_query[word] = tfidf_in_query.get(word, 0.0) + 1.0
        a_pow = 0.0  # query向量模长的平方
        # 计算语料库中有多少文章出现了query中的这个词， 最后直接计算这个词的tfidf
        for key in tfidf_in_query:
            news_count = 1.0
            for i in range(90):
                if words_count[i].get(key, -1) != -1:
                    news_count += 1.0
            tfidf_in_query[key] = tfidf_in_query[key] / len(words_in_query) \
                                  * math.log10(90.0 / news_count)
            a_pow += tfidf_in_query[key] ** 2
        for i in range(90):
            ab = 0.0  # 向量内积
            b_pow = 0.0  # 文章向量模长的平方
            # 计算文章每个词的tfidf
            for key in words_count[i]:
                sum = 1.0
                for j in range(90):
                    if words_count[j].get(key, -1) != -1:
                        sum += 1.0
                words_count[i][key] *= math.log10(90 / sum)
                ab += tfidf_in_query.get(key, 0.0) * words_count[i][key]
                b_pow += words_count[i][key] ** 2
            # 计算query与文档的余弦相似度
            Cosinesimilarity = ab / (a_pow * b_pow) ** 0.5
            results[i].append(Cosinesimilarity)
        results = sorted(results, key=lambda news: news[-1], reverse=True)
        for i in results:
            print(i[1])
            print(i[3])
        return render_template('sjet.html',results=results)
    return render_template('sjet.html')
@sjet.route('/article/<int:id>', methods=['GET'])
def news_page(id):
    BASE_DIR = os.path.dirname(__file__)
    with open(BASE_DIR+'/jianshu_big/' + str(id) + '.txt', 'r',encoding='utf-8') as f:
        title = f.readline()
        content = []
        while True:
            c = f.readline()
            if c:
                content.append(c)
            else:
                break

    return render_template('article.html', title=title, content=content)
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords