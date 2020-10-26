from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


class Model:
    def __init__(self):
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.svm_model_linear = None
        self.log_model_linear = None

    def split_data(self, features, training_label):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(features, training_label,
                                                                                shuffle=True,
                                                                                test_size=0.2,
                                                                                random_state=42)

    def fit_svm(self):
        self.svm_model_linear = SVC(kernel='linear', C=1).fit(self.x_train, self.y_train)
        svm_predictions = self.svm_model_linear.predict(self.x_test)
        accuracy = self.svm_model_linear.score(self.x_test, self.y_test)
        print("Model accuracy with linear svm is: " + str(accuracy))

    def fit_logistic(self):

        self.log_model_linear = LogisticRegression(random_state=0).fit(self.x_train, self.y_train)
        log_predictions = self.log_model_linear.predict(self.x_test)
        accuracy = self.log_model_linear.score(self.x_test, self.y_test)
        print("Model accuracy with logistic regression is: " + str(accuracy))
