import numpy as np
import jieba
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def tokenize(text):
    words = jieba.lcut(text)
    return words


class Preprocessor:

    def __init__(self):
        self.client_questions = None
        self.stop_words = ["。", "，", "？"]
        self.column_index = []
        self.column_names = []
        self.word_matrix = None
        self.cluster = 50
        self.classes = []

    def readfile(self):
        f = open('chatbot.txt', 'r')
        file_content = f.read()
        content_split = file_content.splitlines()
        self.client_questions = [x.split("):  ")[1] for x in content_split
                                 if ("佩爱旗舰店" not in x) and ("):" in x)]
        for i in range(len(self.client_questions)):
            if "[" in self.client_questions[i] and "]" in self.client_questions[i]:
                self.client_questions[i] = self.client_questions[i].split("[")[0] + \
                                           self.client_questions[i].split("[")[1].split("]")[1]

        self.client_questions = [x for x in self.client_questions if ("http" not in x) and len(x) != 0]

    def tf_idf(self):
        vectorizer = TfidfVectorizer(tokenizer=tokenize,
                                     stop_words=self.stop_words)
        matrix = vectorizer.fit_transform(self.client_questions)

        original_features = vectorizer.get_feature_names()
        
        for i in range(len(original_features)):
            if len(re.findall(r'[\u4e00-\u9fff]+', original_features[i])) != 0:
                self.column_index.append(i)
                self.column_names.append(original_features[i])

        self.word_matrix = np.array(matrix.toarray()).T[self.column_index]

    def clustering(self):
        print("Begin clustering")
        k_means = np.array(KMeans(n_clusters=self.cluster).fit(self.word_matrix.T).labels_)
        print("Finished clustering")
        for i in range(self.cluster):
            ind = np.where(k_means == i)[0]
            names = []
            for j in ind:
                names.append(self.client_questions[j])
            self.classes.append(names)

    def write_result(self):
        if not os.path.exists('./clusters'):
            os.makedirs('./clusters')

        for i in range(self.cluster):
            f = open("./clusters/Class_%d.txt" % i, 'w')
            new_class = map(lambda x: x + '\n', self.classes[i])
            f.writelines(new_class)
            f.close()
