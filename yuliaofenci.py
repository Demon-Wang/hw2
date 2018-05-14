# -*- coding: utf-8 -*-
# 将预料集合 结巴分词后生成新的预料集合
import os
import jieba
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
stopwords = stopwordslist('./stopwords.txt')
# 遍历语料集合
for root, dirs, files in os.walk(os.path.dirname(__file__)+"/jianshu_article"):
    i=1
    for file in files:
        # 遍历时排除隐藏文件
        if(file==".DS_Store"):
            continue
        with open(os.path.join(root,file), 'r',encoding='utf-8') as f:
            print(os.path.join(root,file))
            data = f.read()
            # 对文档重命名
            with open(os.path.join(root, str(i))+'.txt', 'a', encoding='utf-8') as g:
                g.write(data)
            seg_list = jieba.cut_for_search(data)
            with open(os.path.join(root, str(i)), 'a', encoding='utf-8') as w:
                for value in seg_list:
                    if(value=='\n' or value==' ' or value in stopwords):
                        continue
                    w.write(value+'\n')
            i+=1
    break