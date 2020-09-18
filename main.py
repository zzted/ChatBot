from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.cluster import KMeans
from src.preprocessor import preprocess, textfilter, contentExtractor
import numpy as np
import jieba

text_filter = textfilter.TextFilter(skip_word=[["对方正在使用", "收发消息"]],
                                    skip_line="-------",
                                    skip_prefix="): ")

conversation = preprocess.Conversation(["(2017"], ["佩爱旗舰店"],
                                       ["(2017", "佩爱旗舰店"], [],
                                       ["-------", "佩爱旗舰店"], [],
                                       text_filter)


def tokenize(text):
    words = jieba.lcut(text)
    return words


def main():
    f = open('chatbot.txt', 'r')
    file_content = f.read()
    text = file_content.splitlines()
    stop_words = [" ", "亲", "嗯"]

    conversation.transform(text)

    feature = FeatureUnion(
        transformer_list=[
            ('questions', Pipeline([
                ('selector', contentExtractor.ContentExtractor(0)),
                ('Tf-Idf', TfidfVectorizer(stop_words=stop_words, tokenizer=tokenize, ngram_range=(1, 3)))
            ])),
            ('questionsPinYin', Pipeline([
                ('selector', contentExtractor.ContentExtractor(2)),
                ('Tf-Idf', TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 5), analyzer=u'char'))
            ])),
            ('answers', Pipeline([
                ('selector', contentExtractor.ContentExtractor(1)),
                ('Tf-Idf', TfidfVectorizer(stop_words=stop_words, tokenizer=tokenize, ngram_range=(1, 3)))
            ])),
            ('answerPinyin', Pipeline([
                ('selector', contentExtractor.ContentExtractor(3)),
                ('Tf-Idf', TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 5), analyzer=u'char'))
            ]))
        ]
    )

    features = feature.fit_transform(conversation.data)
    clusters = 50
    print(features.shape)
    print("Begin Clustering")
    k_means = np.array(KMeans(n_clusters=clusters).fit(features).labels_)
    print("Finished Clustering")

    questions = [x[0] for x in conversation.data]
    answers = [x[1] for x in conversation.data]

    classes = []
    for i in range(clusters):
        ind = np.where(k_means == i)[0]
        names = []
        for j in ind:
            names.append(answers[j])
        classes.append(names)
    for i in range(clusters):
        f = open("./res/answers/Class_%d.txt" % i, 'w')
        newClass = map(lambda x: x + '\n', classes[i])
        f.writelines(newClass)
        f.close()

    classes = []
    for i in range(clusters):
        ind = np.where(k_means == i)[0]
        names = []
        for j in ind:
            names.append(questions[j])
        classes.append(names)
    for i in range(clusters):
        f = open("./res/questions/Class_%d.txt" % i, 'w')
        newClass = map(lambda x: x + '\n', classes[i])
        f.writelines(newClass)
        f.close()


if __name__ == '__main__':
    main()
