# -*- coding: utf-8 -*-

print("Bag of words".center(40, "-"))

# import os
# # 文本数据
# # corpus = ["The cat sat the mat", "The dog ate my homework"]
#
# file_path = os.path.join("./data", "corpus.txt")
# with open(file_path, encoding="utf-8") as f:
#     corpus = f.readlines()
#
# # 构建词汇表
# vocab = sorted(set(" ".join(corpus).split()))
# word_to_idx = {word: idx for idx, word in enumerate(vocab)}
#
# print("词汇表:", vocab)
# print("索引映射:", word_to_idx)
#
#
# # 将文本转换为词袋表示
# def text_to_bag_of_words(text, vocab_size, word_to_idx):
#     bag_of_words = [0] * vocab_size
#
#     # 计算每个单词出现的次数
#     words = text.split()
#     for word in words:
#         if word in word_to_idx:
#             idx = word_to_idx[word]
#             bag_of_words[idx] += 1
#
#     return bag_of_words
#
#
# # 获取词汇表大小
# vocab_size = len(vocab)
#
# # 将语料库中的每句话转换为词袋表示
# bag_of_words_corpus = [text_to_bag_of_words(sentence, vocab_size, word_to_idx) for sentence in corpus]
#
# # 打印词袋表示结果
# for sentence, bow in zip(corpus, bag_of_words_corpus):
#     print(f"句子: '{sentence.strip()}'")
#     print(f"词汇: {list(word_to_idx.keys())}")
#     print(f"词袋表示: {bow}")
#
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#
# count_vec = CountVectorizer(ngram_range=(1, 1),  # to use bigrams ngram_range=(2,2)
#                             # stop_words='english'
#                             )
# # transform
# feature = count_vec.fit_transform(corpus)
#
# # create dataframe
# df = pd.DataFrame(feature.toarray(), columns=count_vec.get_feature_names_out())
# print(df)

print("TF-IDF".center(40, "-"))

# import math
# import os
# import pandas as pd
#
# # 读取文件路径
# file_path = os.path.join("./data", "corpus.txt")
#
# # 从文件中读取语料库
# with open(file_path, encoding="utf-8") as f:
#     corpus = f.readlines()
#
# # 构建词汇表
# vocab = sorted(set(" ".join(corpus).split()))
# word_to_idx = {word: idx for idx, word in enumerate(vocab)}
# vocab_size = len(vocab)
#
# # 计算文档频率
# doc_freq = {word: 0 for word in vocab}
# for sentence in corpus:
#     unique_words = set(sentence.split())
#     for word in unique_words:
#         if word in doc_freq:
#             doc_freq[word] += 1
#
# # 计算逆文档频率(IDF)
# num_docs = len(corpus)
# idf = {word: math.log(num_docs / (1 + df)) for word, df in doc_freq.items()}
#
#
# # 将文本转换为TF-IDF表示
# def text_to_tfidf(text, idf, vocab_size, word_to_idx):
#     tfidf = [0] * vocab_size
#     words = text.split()
#
#     # 计算词频(TF)
#     word_count = {}
#     for word in words:
#         if word in word_count:
#             word_count[word] += 1
#         else:
#             word_count[word] = 1
#
#     # 计算TF-IDF
#     for word, count in word_count.items():
#         if word in idf:
#             idx = word_to_idx[word]
#             tfidf[idx] = (count / len(words)) * idf[word]
#
#     return tfidf
#
#
# # 将语料库中的每句话转换为TF-IDF表示
# tfidf_corpus = [text_to_tfidf(sentence, idf, vocab_size, word_to_idx) for sentence in corpus]
#
# # 打印TF-IDF表示结果
# # for sentence, tfidf in zip(corpus, tfidf_corpus):
# #     print(f"句子: '{sentence.strip()}'")
# #     print(f"词汇: {vocab}")
# #     print(f"TF-IDF表示: {tfidf}")
# df = pd.DataFrame(tfidf_corpus, columns=vocab)
# print(df)
#
# print("----".center(40, "-"))
#
#
#
# import os
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# # 读取文件路径
# file_path = os.path.join("./data", "corpus.txt")
#
# # 从文件中读取语料库
# with open(file_path, encoding="utf-8") as f:
#     corpus = f.readlines()
#
# # 使用TfidfVectorizer初始化一个TF-IDF向量化器
# # vectorizer = TfidfVectorizer()
# vectorizer = TfidfVectorizer(stop_words=None, lowercase=False)
#
# # 学习语料库并进行向量化
# X = vectorizer.fit_transform(corpus)
#
# # 获取词汇表
# vocab = vectorizer.get_feature_names_out()
#
# # 打印TF-IDF矩阵
# # print("TF-IDF Matrix:\n", X.toarray())
#
# # 打印词汇表
# # print("Vocabulary:\n", vocab)
#
# # 打印每条记录的TF-IDF值
# # for sentence, tfidf in zip(corpus, X.toarray()):
# #     print(f"句子: '{sentence.strip()}'")
# #     print(f"{vocab}")
# #     print(f"TF-IDF表示: \n{tfidf}\n")
# df = pd.DataFrame(X.toarray(), columns=vocab)
# print(df)
#
# import nltk
# # nltk.download('stopwords')
# nltk.download('punkt')

print("N-gram".center(40, "-"))

# import os
#
# # 读取文件路径
# file_path = os.path.join("./data", "corpus.txt")
#
# # 从文件中读取语料库
# with open(file_path, encoding="utf-8") as f:
#     corpus = f.readlines()
#
#
# 定义生成 N-gram 的函数
# def generate_ngrams(text, n=2):
#     """
#     生成词级别的 N-gram。
#
#     参数:
#     text (str): 输入文本。
#     n (int): N-gram 的大小。
#
#     返回:
#     list: 包含 N-gram 的列表。
#     """
#     words = text.split()
#     ngrams = [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
#     return ngrams
#
#
# # 生成 N-gram
# n = 2  # 可以调整 N 的大小
# ngram_corpus = [generate_ngrams(sentence, n=n) for sentence in corpus]
#
# # 打印 N-gram 结果
# for sentence, ngrams in zip(corpus, ngram_corpus):
#     print(f"句子: '{sentence.strip()}'")
#     print(f"N-gram (n={n}): {ngrams}\n")
#
#
# # 定义生成字符级别的 N-gram 的函数
# def generate_char_ngrams(text, n=2):
#     """
#     生成字符级别的 N-gram。
#
#     参数:
#     text (str): 输入文本。
#     n (int): N-gram 的大小。
#
#     返回:
#     list: 包含 N-gram 的列表。
#     """
#     ngrams = [text[i:i + n] for i in range(len(text) - n + 1)]
#     return ngrams
#
#
# # 生成字符级别的 N-gram
# char_n = 2  # 可以调整 N 的大小
# char_ngram_corpus = [generate_char_ngrams(sentence, n=char_n) for sentence in corpus]
#
# # 打印字符级别的 N-gram 结果
# for sentence, char_ngrams in zip(corpus, char_ngram_corpus):
#     print(f"句子: '{sentence.strip()}'")
#     print(f"字符级别的 N-gram (n={char_n}): {char_ngrams}\n")

