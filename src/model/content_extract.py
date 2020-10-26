from sklearn.base import BaseEstimator, TransformerMixin
from xpinyin import Pinyin

p = Pinyin()


class ContentExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, target=0):
        self.target = target

    def transform(self, text, y=None):
        if self.target == 0:
            return text
        if self.target == 1:
            return [p.get_pinyin(x, '') for x in text]

    def fit(self, text, y=None):
        return self
