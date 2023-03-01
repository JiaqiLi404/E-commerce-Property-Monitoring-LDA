import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from gensim import corpora, models
import jieba.posseg as jp
from wordcloud import WordCloud
import matplotlib as mpl
from sklearn import svm
from matplotlib import colors

# 环境准备
plt.style.use('seaborn')
sns.set(font_scale=2)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
stopwords = ('根据', '图片', 'Moment', '是', '不', '也', '到', '将', '有', '都', 'G', '更', '就', '还', '会', '人', '要', '没有',
             '可能', '需要', '就是', '包括', '已经', '还有', '甚至', '作为', '非常', '进行')  # 停词


# 数据读取
def loadcsv():
    f = open(r'附件1.csv', encoding='utf-8"')
    df = pd.read_csv(f, delimiter='\t', sep='\t', error_bad_lines=False)
    df['char_length'] = df['正文'].astype(str).apply(len)
    return df


# jieba分词
def fenci(texts):
    print('开始分词')
    flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性
    # 分词
    words_ls = []
    onesen = ""
    for text in texts:
        words = [w.word for w in jp.cut(text) if w.flag in flags and w.word not in stopwords]
        onesen += " ".join(words) + " "
        words_ls.append(words)
    print('分词完毕')
    return words_ls, onesen


# lda 模型
def lda(words_ls):
    # 构造词典
    dictionary = corpora.Dictionary(words_ls)
    print('词典构建完毕')
    # 对每段文本依据词典生成向量
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    print('lda模型开始训练')
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=3)
    # 打印所有主题，每个主题显示 5 个词
    for topic in lda.print_topics(num_words=10):
        print(topic)
    # 主题推断
    print(lda.inference(corpus))
    print('lda模型已完成')


# 生成词云
def cloud(sen):
    print('开始制作词云')
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/simkai.ttf", background_color="white", max_font_size=130,
                          max_words=200, stopwords=set(stopwords)).generate(sen)
    image = wordcloud.to_image()
    wordcloud.to_file('ciyun.png')
    image.show()
    print('词云制作结束')


# 支持向量机主题分类
def svm(x, y):
    clf = svm.SVC(C=0.5, kernel='rbf', gamma=1, decision_function_shape='ovr')
    clf.fit(x, y.ravel())
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()
    x1, x2 = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j]
    grid_test = np.stack((x1.flat, x2.flat), axis=1)
    grid_hat = clf.predict(grid_test)
    grid_hat = grid_hat.reshape(x1.shape)

    cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
    cm_dark = mpl.colors.ListedColormap(['g', 'b', 'r'])

    plt.pcolormesh(x1, x2, grid_hat, cmap=cm_light)
    plt.scatter(x[:, 0], x[:, 1], c=np.squeeze(y), edgecolor='k', s=50, cmap=cm_dark)  # 样本点
    plt.xlabel('关键词1的词频', fontsize=20)
    plt.ylabel('关键词2的词频', fontsize=20)
    plt.xlim(x1_min, x1_max)
    plt.ylim(x2_min, x2_max)
    plt.title('基于svm的主题分类示意图', fontsize=30)
    plt.grid()
    plt.show()


df = loadcsv()
texts = df['正文'].tolist()[0:5000]
wlist, sen = fenci(texts)
lda(wlist)
cloud(sen)
