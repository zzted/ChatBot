from src.preprocessor import preprocess, textfilter, content_extract, file_reader, cluster


def main():
    text_filter = textfilter.TextFilter(skip_word=[["对方正在使用", "收发消息"]],
                                        skip_line="-------",
                                        skip_prefix="): ")

    conversation = preprocess.Conversation(["(2017"], ["佩爱旗舰店"],
                                           ["(2017", "佩爱旗舰店"], [],
                                           ["-------", "佩爱旗舰店"], [],
                                           text_filter)

    data_file = file_reader.DataFile()

    data_file.read(file_path='/home/zz/Documents/ChatBot/chatbot.txt')

    cluster_data = cluster.Cluster([" ", "亲", "嗯"], [], 50)

    conversation.transform(data_file.text)

    cluster_data.fit_transform(conversation.data)

    cluster_data.write_result("questions")

    cluster_data.write_result("answers")


if __name__ == '__main__':
    main()
