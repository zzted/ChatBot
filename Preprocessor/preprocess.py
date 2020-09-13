from urlextract import URLExtract
from xpinyin import Pinyin
import unicodedata
import jieba
import os
import re

p = Pinyin()
extractor = URLExtract()


def tokenize(text):
    words = jieba.lcut(text)
    return words


def skip_section(text, i):
    i += 1
    while "-------" not in text[i]:
        i += 1
    i += 1
    return i


def text_filter(text):
    cur = unicodedata.normalize('NFKC', text)
    if '-------' in cur:
        cur = ""
    #     if("[" in cur and "]" in cur):
    #         cur = cur.split("[")[0] + cur.split("[")[1].split("]")[1]
    urls = extractor.find_urls(cur)
    if len(urls) > 0:
        for link in urls:
            cur = cur.replace(link, "[链接]")
    nums = re.findall(r'-?\d+\.?\d*', cur)
    nums = sorted(nums, key=len, reverse=True)
    if len(nums) > 0:
        for num in nums:
            cur = cur.replace(num, "[数字]")
    if "): " in cur:
        cur = cur.split("):  ")[1]
    if "对方正在使用" in cur and "收发消息" in cur:
        cur = cur.split("对方正在使用")[0] + cur.split("对方正在使用")[1].split("收发消息")[1]

    cur = re.sub(r'''[][【】“”‘’"'、,.。:;@#?!&$/()%~`-―〈〉「」・@+_*=《》^…￥-]+\ *''',
                 " ", cur, flags=re.VERBOSE)
    return cur


class Preprocessor:

    def __init__(self):
        self.data = []
        self.stopWords = [' ']
        self.cluster = 50
        self.classes = []

    def transform(self):
        f = open('chatbot.txt', 'r')
        file_content = f.read()
        text = file_content.splitlines()

        i = 0
        while i < len(text):
            Q = ""
            A = ""
            if "(2017" in text[i] and "佩爱旗舰店" not in text[i]:
                while i < len(text):
                    Q += text_filter(text[i])
                    i += 1
                    if i < len(text) and "-------" in text[i] and "佩爱旗舰店" in text[i]:
                        i = skip_section(text, i)
                        continue
                    if i < len(text) and "(2017" in text[i] and "佩爱旗舰店" in text[i]:
                        break
            if i < len(text) and "(2017" in text[i] and "佩爱旗舰店" in text[i]:
                while i < len(text):
                    A += text_filter(text[i])
                    i += 1
                    if i < len(text) and "-------" in text[i] and "佩爱旗舰店" in text[i]:
                        i = skip_section(text, i)
                        continue
                    if i < len(text) and "(2017" in text[i] and "佩爱旗舰店" not in text[i]:
                        Q = re.sub(r"\s+", " ", Q)
                        Q_p = p.get_pinyin(Q, ' ')
                        Q_p = re.sub(r"\s+", " ", Q_p)
                        A = re.sub(r"\s+", " ", A)
                        A_p = p.get_pinyin(A, ' ')
                        A_p = re.sub(r"\s+", " ", A_p)
                        self.data.append([Q, A, Q_p, A_p])
                        break
            else:
                i += 1

    def write_result(self):
        if not os.path.exists('./clusters'):
            os.makedirs('./clusters')

        for i in range(self.cluster):
            f = open("./clusters/Class_%d.txt" % i, 'w')
            new_class = map(lambda x: x + '\n', self.classes[i])
            f.writelines(new_class)
            f.close()
