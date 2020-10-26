from src.preprocessor import data_clean, text_filter, read_file, feature_extract
import time


def main():
    text_filter = text_filter.TextFilter(skip_word=[["对方正在使用", "收发消息"]],
                                         skip_line="-------",
                                         skip_prefix="): ")

    conversation = data_clean.Conversation(["(2017"], ["佩爱旗舰店"],
                                           ["(2017", "佩爱旗舰店"], [],
                                           ["-------", "佩爱旗舰店"], [],
                                           text_filter)

    data_file = read_file.DataFile()

    start = time.time()
    data_file.read(file_path='../../docs/chatbot.txt')
    end = time.time()
    print("Reading file took %f sec" % (end - start))

    cluster_data = feature_extract.Cluster([" ", "亲", "嗯", "好的"], [], 100)

    start = time.time()
    conversation.transform(data_file.text)
    end = time.time()
    print("Content extracting took %f sec" % (end - start))

    # with open("/home/zz/Documents/ChatBot/docs/transformed_text.txt", 'w') as fp:
    #     for list_item in conversation.data:
    #         fp.write('%s\n' % list_item[0])
    #         fp.write('%s\n' % list_item[2])

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
