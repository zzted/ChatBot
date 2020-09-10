from Preprocessor import preprocess

preprocessor = preprocess.Preprocessor()


def main():
    preprocessor.readfile()
    preprocessor.tf_idf()
    preprocessor.clustering()
    preprocessor.write_result()


if __name__ == '__main__':
    main()
