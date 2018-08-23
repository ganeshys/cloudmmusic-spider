# _*_ coding:utf-8 _*_
import json
import jieba
import re
from collections import Counter
from pyecharts import Bar, Pie
from pprint import pprint


def format_content(content):
    content = content.replace(u'\xa0', u' ')
    content = re.sub(r'\[.*?\]', '', content)
    content = re.sub(r'\s*作曲.*\n', '', content)
    content = re.sub(r'\s*作词.*\n', '', content)
    content = re.sub(r'.*:', '', content)
    content = re.sub(r'.*：', '', content)
    content = content.replace('\n', ' ')
    return content


# 分词
def word_segmentation(content, stop_words):
    # 使用 jieba 分词对文本进行分词处理

    seg_list = jieba.cut(content, cut_all=False)

    seg_list = list(seg_list)

    # 去除停用词
    word_list = []
    for word in seg_list:
        if word not in stop_words:
            word_list.append(word)

    # 过滤遗漏词、空格
    user_dict = [' ', '哒']
    filter_space = lambda w: w not in user_dict
    word_list = list(filter(filter_space, word_list))

    return word_list


# 词频统计
# 返回前 top_N 个值，如果不指定则返回所有值
def word_frequency(word_list, *top_N):
    if top_N:
        counter = Counter(word_list).most_common(top_N[0])
    else:
        counter = Counter(word_list).most_common()

    return counter


def plot_chart(counter, chart_type='Bar'):
    items = [item[0] for item in counter]
    values = [item[1] for item in counter]

    if chart_type == 'Bar':
        chart = Bar('词频统计')
        chart.add('词频', items, values, is_more_utils=True)
    else:
        chart = Pie('词频统计')
        chart.add('词频', items, values, is_label_show=True, is_more_utils=True)

    chart.show_config()
    chart.render()


def main():
    with open('lyric1.json', 'rb') as f:
        data = json.load(f)

    # 停用词表来自：
    # https://github.com/XuJin1992/ChineseTextClassifier
    with open('stop_words.txt', encoding='UTF-8') as f:
        stop_words = f.read().split('\n')

    lyric = data[0]
    lyric = format_content(lyric)

    seg_list = word_segmentation(lyric, stop_words)

    counter = word_frequency(seg_list, 10)

    plot_chart(counter)


if __name__ == '__main__':
    main()
