from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from src.model import content_extract
import jieba


class Feature:
    def __init__(self, stop_words):
        self.feature_union = None
        self.stop_words = stop_words

    @classmethod
    def tokenizer(cls, text):
        words = jieba.lcut(text)
        return words

    def get_feature_union(self):
        self.feature_union = FeatureUnion(
            transformer_list=[
                ('questions', Pipeline([
                    ('selector', content_extract.ContentExtractor(0)),
                    ('Tf-Idf', TfidfVectorizer(stop_words=self.stop_words, tokenizer=self.tokenizer, ngram_range=(1, 3)))
                ])),
                ('questionsPinYin', Pipeline([
                    ('selector', content_extract.ContentExtractor(1)),
                    ('Tf-Idf', TfidfVectorizer(stop_words=[' '], ngram_range=(1, 5), analyzer=u'char'))
                ]))
            ]
        )
