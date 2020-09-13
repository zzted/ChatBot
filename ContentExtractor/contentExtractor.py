from sklearn.base import BaseEstimator, TransformerMixin


class ContentExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, target=0):
        self.target = target

    def transform(self, text, y=None):
        return [x[self.target] for x in text]

    def fit(self, text, y=None):
        return self
