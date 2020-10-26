from src.model import feature_extract, linear_model, read_data
import time


def main():
    print("Reading file......")
    start = time.time()
    file_dir = "/home/zz/Documents/ChatBot/docs/clusters/res_100_q10_qp10_a03_ap03.txt"
    stop_words = [" ", "亲", "嗯", "好的"]
    file = read_data.File_reader()
    file.read(file_dir)
    end = time.time()
    print("Reading file took %f sec" % (end - start))

    print("Extracting feature......")
    start = time.time()
    feature_extractor = feature_extract.Feature(stop_words)
    feature_extractor.get_feature_union()
    features = feature_extractor.feature_union.fit_transform(file.training_data)
    end = time.time()
    print("Extracting feature took %f sec" % (end - start))

    models = linear_model.Model()
    models.split_data(features, file.training_label)

    start = time.time()
    print("Fitting linear SVM......")
    models.fit_svm()
    end = time.time()
    print("Fitting linear SVM took %f sec" % (end - start))

    start = time.time()
    print("Fitting logistic regression......")
    models.fit_logistic()
    end = time.time()
    print("Fitting logistic regression took %f sec" % (end - start))


if __name__ == '__main__':
    main()
