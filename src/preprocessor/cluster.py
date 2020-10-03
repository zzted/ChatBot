from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from src.preprocessor import content_extract
from sklearn.cluster import KMeans
import numpy as np
import jieba


class Cluster:
    def __init__(self, stop_words: list, stop_words_pinyin: list, cluster_number: int):
        self.stop_words = stop_words
        self.stop_words_pinyin = stop_words_pinyin
        self.feature_union = None
        self.k_means = None
        self.data = None
        self.cluster_number = cluster_number

    @classmethod
    def tokenizer(cls, text):
        words = jieba.lcut(text)
        return words

    def union_feature(self):
        self.feature_union = FeatureUnion(
            transformer_list=[
                ('questions', Pipeline([
                    ('selector', content_extract.ContentExtractor(0)),
                    (
                        'Tf-Idf',
                        TfidfVectorizer(stop_words=self.stop_words, tokenizer=self.tokenizer, ngram_range=(1, 3)))
                ])),
                ('questionsPinYin', Pipeline([
                    ('selector', content_extract.ContentExtractor(2)),
                    ('Tf-Idf', TfidfVectorizer(stop_words=self.stop_words, ngram_range=(1, 5), analyzer=u'char'))
                ])),
                ('answers', Pipeline([
                    ('selector', content_extract.ContentExtractor(1)),
                    (
                        'Tf-Idf',
                        TfidfVectorizer(stop_words=self.stop_words, tokenizer=self.tokenizer, ngram_range=(1, 3)))
                ])),
                ('answerPinyin', Pipeline([
                    ('selector', content_extract.ContentExtractor(3)),
                    ('Tf-Idf', TfidfVectorizer(stop_words=self.stop_words, ngram_range=(1, 5), analyzer=u'char'))
                ]))
            ]
        )

    def fit_transform(self, data):
        self.data = data
        self.union_feature()
        features = self.feature_union.fit_transform(data)
        print(features.shape)
        print("Begin Clustering")
        self.k_means = np.array(KMeans(n_clusters=self.cluster_number).fit(features).labels_)
        print("Finished Clustering")

    def write_result(self):
        classes = []
        to_write = [x[0] + "@" + x[1] for x in self.data]

        for i in range(self.cluster_number):
            ind = np.where(self.k_means == i)[0]
            names = []
            for j in ind:
                names.append(to_write[j])
            classes.append(names)

        for i in range(self.cluster_number):
            f = open("./docs/clusters/res.txt", 'a+')
            newClass = map(lambda x: x + '\n', classes[i])
            f.write("Cluster_%d \n" % i)
            f.writelines(newClass)
            f.close()
        print("Finished writing result data.")
