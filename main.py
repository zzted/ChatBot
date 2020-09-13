from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.cluster import KMeans
from ContentExtractor import contentExtractor
from Preprocessor import preprocess
import numpy as np
import jieba


preprocessor = preprocess.Preprocessor()


def tokenize(text):
    words = jieba.lcut(text)
    return words


def main():
    preprocessor.transform()

    feature = FeatureUnion(
        transformer_list=[
            ('answers', Pipeline([
                ('selector', contentExtractor.ContentExtractor(1)),
                ('Tf-Idf', TfidfVectorizer(stop_words=preprocessor.stopWords, tokenizer=tokenize, ngram_range=(1, 3)))
            ])),
            ('answerPinyin', Pipeline([
                ('selector', contentExtractor.ContentExtractor(3)),
                ('Tf-Idf', TfidfVectorizer(stop_words=preprocessor.stopWords, ngram_range=(1, 5), analyzer=u'word'))
            ]))
        ]
    )
    features = feature.fit_transform(preprocessor.data)
    clusters = 50
    print(features.shape)
    print("Begin Clustering")
    k_means = np.array(KMeans(n_clusters=clusters).fit(features).labels_)
    print("Finished Clustering")
    classes = []
    answers = [x[1] for x in preprocessor.data]
    for i in range(clusters):
        ind = np.where(k_means == i)[0]
        names = []
        for j in ind:
            names.append(answers[j])
        classes.append(names)
    for i in range(clusters):
        f = open("./clusters/Class_%d.txt" % i, 'w')
        newClass = map(lambda x: x + '\n', classes[i])
        f.writelines(newClass)
        f.close()


if __name__ == '__main__':
    main()
