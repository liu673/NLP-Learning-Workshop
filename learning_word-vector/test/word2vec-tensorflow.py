#coding=utf-8

import collections
import re
import math
import random
import jieba
import numpy as np
from six.moves import xrange
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn.manifold import TSNE

# 读取停用词
def read_stopword():
    stop_words = []
    with open("data/stop_words.txt", "r", encoding="utf-8") as f_stopwords:
        for line in f_stopwords:
            line = line.replace("\r", "").replace("\n", "").strip()  # 去除回车换行
            stop_words.append(line)
    print(len(stop_words))
    stop_words = set(stop_words)  # 去重
    print(len(stop_words))
    return stop_words



# 文本预处理
def text_process(stop_words):
    raw_word_list = []
    rules = u"[\u4e00-\u9fa5]+"
    # rules = '[\u4e00-\u9fa5]+'
    pattern = re.compile(rules)
    f_writer = open("data/分词过后的笑傲江湖.txt", "w", encoding="utf-8")
    # count = 0
    with open("data/笑傲江湖.txt", "r", encoding="utf-8") as f_reder:
        lines = f_reder.readlines()
        for line in lines:
            line = line.replace("\r", "").replace("\n", "").strip()  # 去除回车换行
            if line == "" or line is None:  # 去除处理后的空行
                continue
            line = " ".join(jieba.cut(line))  # jieba分词 中间用空格分开
            seg_list = pattern.findall(line)
            word_list = []
            for word in seg_list:
                if word not in stop_words:
                    word_list.append(word)
            if len(word_list) > 0:  # 再次去除遗留的空行
                raw_word_list.extend(word_list)
                # count = count + 1
                print(seg_list)
                # if count == 10:
                #     break
                line = " ".join(word_list)
                f_writer.write(line + "\n")
                f_writer.flush()
    f_writer.close()
    print("原始词数：", len(raw_word_list))
    print("去重后的：", len(set(raw_word_list)))
    vocabulary_size = len(set(raw_word_list))
    return raw_word_list, vocabulary_size

# 词和索引的转换
def word_to_index(raw_word_list):
    words = raw_word_list
    count = [["UNK", "-1"]]
    count.extend(collections.Counter(words).most_common(vocabulary_size-1))
    print("count", len(count))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]  # 获取词的索引
        else:
            index = 0
            unk_count = unk_count + 1
        data.append(index)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))

    return data, reverse_dictionary, dictionary


# skip_gram 生成批量batch
def generate_batch():
    data_index = 0
    batch_size = 128
    num_skips = 4
    skip_window = 2
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    lables = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2*skip_window + 1
    buffer = collections.deque(maxlen=span)
    for _ in range(span):
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    for i in range(batch_size // num_skips):
        target = skip_window
        targets_to_avoid = [skip_window]
        # 进行负采样
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span-1)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            lables[i * num_skips + j] = buffer[target]
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)

    return batch, lables


# skip-gram model
def skip_gram_model(dictionary, reverse_dictionary):
    batch_size = 128
    embedding_size = 300  # 向量维度大小
    skip_window = 2
    num_skips = 4
    valid_window = 100
    num_sample = 64
    learning_rate = 0.01

    # 校验集
    vaild_word = ["令狐冲", "左冷禅", "林平之", "岳不群", "桃根仙"]
    vaild_examples = [dictionary[li] for li in vaild_word]

    # 构建计算图
    graph = tf.Graph()
    with graph.as_default():
        # 输入数据
        train_inputs = tf.placeholder(dtype=tf.int32, shape=[batch_size])
        train_labels = tf.placeholder(dtype=tf.int32, shape=[batch_size, 1])
        vaild_dataset = tf.constant(vaild_examples, dtype=tf.int32)

        with tf.device("/cpu:0"):
            embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
            embed = tf.nn.embedding_lookup(embeddings, train_inputs)

            nce_weight = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_size], stddev=1.0 / math.sqrt(embedding_size)))
            nce_baises = tf.Variable(tf.zeros([vocabulary_size]), dtype=tf.float32)

            # 负采样的loss
            neg_loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weight, biases=nce_baises, inputs=embed, labels=train_labels,
                                                     num_sampled=num_sample, num_classes=vocabulary_size))

            optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(neg_loss)

            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
            normalized_embeddings = embeddings / norm

            valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, vaild_dataset)
            similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)
            init = tf.global_variables_initializer()
            print("模型构建完成")


            # 开始模型的训练
            num_steps = 20000
            with tf.Session(graph=graph) as sess:
                init.run()
                print("*******************初始化成功******************")
                avg_loss = 0

                for step in xrange(num_steps):
                    batch_inputs, batch_lablels = generate_batch()
                    _, loss = sess.run([optimizer, neg_loss], feed_dict={train_inputs: batch_inputs, train_labels: batch_lablels})
                    avg_loss = avg_loss + loss

                    if step % 5000 == 0:
                        if step > 0:
                            avg_loss = avg_loss / 50000
                        print("平均损失在", step, "中为:", avg_loss)

                    # 计算验证集的相似度
                    if step % 10000 == 0:
                        sim = similarity.eval()
                        for i in xrange(len(vaild_word)):
                            val_word = reverse_dictionary[vaild_examples[i]]
                            top_k = 10
                            nearest = (-sim[i, :]).argsort()[:top_k]
                            # print(nearest)
                            sim_str = "与" + val_word + "最近的前10词是"
                            for k in xrange(top_k):
                                close_word = reverse_dictionary[nearest[k]]
                                sim_str = "%s %s" % (sim_str, close_word)
                            print(sim_str)
                final_embeddings = normalized_embeddings.eval()
    return final_embeddings


# 可视化
def show_embs_labels(final_embeddings, low_dim_embs, labels, filename="word2vec.png", fonts=None):
    plt.figure(figsize=(18, 18))
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(label, fontproperties=fonts, xy=(x, y), textcoords="offset points", va="bottom")
        plt.savefig(filename, dpi=800)


if __name__ == '__main__':
    stop_words = read_stopword()  # 停用词
    words, vocabulary_size = text_process(stop_words)
    count = [["UNK", "-1"]]
    count.extend(collections.Counter(words).most_common(vocabulary_size-1))  # 统计词频
    print(count)
    print('count', len(count))

    data, reverse_dictionary, dictionary = word_to_index(words)

    batch, lables = generate_batch()
    for i in range(20):
        print(batch[i], reverse_dictionary[batch[i]], "---->", lables[i, 0], reverse_dictionary[lables[i, 0]])

    final_embeddings = skip_gram_model(dictionary, reverse_dictionary)
    font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=16)
    tsne = TSNE(perplexity=30, n_components=2, init="pca", n_iter=5000)
    plot_only = 500
    low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
    labels = [reverse_dictionary[i] for i in xrange(plot_only)]
    show_embs_labels(final_embeddings, low_dim_embs, labels, fonts=font)
