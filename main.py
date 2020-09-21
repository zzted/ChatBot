from src.preprocessor import preprocess, textfilter, content_extract, file_reader, cluster
import time


def main():
    text_filter = textfilter.TextFilter(skip_word=[["对方正在使用", "收发消息"]],
                                        skip_line="-------",
                                        skip_prefix="): ")

    conversation = preprocess.Conversation(["(2017"], ["佩爱旗舰店"],
                                           ["(2017", "佩爱旗舰店"], [],
                                           ["-------", "佩爱旗舰店"], [],
                                           text_filter)

    data_file = file_reader.DataFile()

    start = time.time()
    data_file.read(file_path='./docs/chatbot.txt')
    end = time.time()
    print("Reading file took %f sec" % (end - start))

    cluster_data = cluster.Cluster([" ", "亲", "嗯"], [], 50)

    start = time.time()
    conversation.transform(data_file.text)
    end = time.time()
    print("Content extracting took %f sec" % (end - start))

    start = time.time()
    cluster_data.fit_transform(conversation.data)
    end = time.time()
    print("Clustering took %f sec" % (end - start))

    start = time.time()
    cluster_data.write_result()
    end = time.time()
    print("Writing results took %f sec" % (end - start))


if __name__ == '__main__':
    main()
