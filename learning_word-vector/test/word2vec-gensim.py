# -*- coding: utf-8 -*-
# @Time : 2023/1/11 16:03
# @Author : XXX
# @File : word2vec-gensim.py
import jieba
import re
from gensim.models import word2vec
import time


def read_stop(stop_words_path):
    """
    读取停用词
    :return:
    """
    # 读取停用词
    stop_words = []
    with open(stop_words_path, "r", encoding="utf-8") as f_reader:
        for line in f_reader:
            line = line.replace("\r", "").replace("\n", "").strip()
            stop_words.append(line)
    print(len(stop_words))
    stop_words = set(stop_words)
    print(len(stop_words))
    return stop_words


def data_process(data_path, split_data_path):
    """
    数据预处理
    :return:
    """

    # 文本预处理
    sentecnces = []
    rules = u"[\u4e00-\u9fa5]+"
    pattern = re.compile(rules)
    f_writer = open(split_data_path, "w", encoding="utf-8")

    with open(data_path, "r", encoding="utf-8") as f_reader:
        for line in f_reader:
            line = line.replace("\r", "").replace("\n", "").strip()
            if line == "" or line is None:
                continue
            line = " ".join(jieba.cut(line))
            seg_list = pattern.findall(line)
            word_list = []
            for word in seg_list:
                if word not in stop_words:
                    word_list.append(word)
            if len(word_list) > 0:
                sentecnces.append(word_list)
                line = " ".join(word_list)
                f_writer.write(line + "\n")
                f_writer.flush()
    f_writer.close()
    return sentecnces


if __name__ == '__main__':
    stop_words_file = "../data/stop_words.txt"
    data_file = "../data/天龙八部.txt"
    split_data_file = "../data/天龙八部_split.txt"
    stop_words = read_stop(stop_words_file)
    sentecnces = data_process(data_file, split_data_file)
    print(sentecnces[:10])

    # 模型训练
    start_time = time.time()
    print("开始训练模型...")
    model = word2vec.Word2Vec(sentecnces, epochs=50, vector_size=100, window=3, sg=0)
    print("训练模型结束，耗时：", time.time() - start_time)
    # 保存模型
    model.save("../models/天龙八部.bin")
    # 加载模型
    model2 = word2vec.Word2Vec.load("../models/天龙八部.bin")

    # 选出10个与乔峰最相近的10个词
    for e in model2.wv.most_similar(positive=["乔峰"], topn=10):
        print(e[0], e[1])

    # 计算两个词语的相似度
    sim_value = model.wv.similarity('乔峰', '萧峰')
    print(sim_value)

    # 计算两个集合的相似度
    list1 = ['乔峰', '萧远山']
    list2 = ['慕容复', '慕容博']
    sim_value = model.wv.n_similarity(list1, list2)
    print(sim_value)

    # 查看词向量值
    # print(type(model['乔峰']))
    # print(len(model['乔峰']))
    # print(model['乔峰'])
