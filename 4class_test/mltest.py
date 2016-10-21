from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import load_svmlight_file
from sklearn import metrics, svm
from sklearn import cross_validation
import random

def bdt_test(xj,yj):
    print "Testing bdt......."
    bdt = AdaBoostClassifier(
        DecisionTreeClassifier(max_depth=5),
        n_estimators=100,
        learning_rate=0.7)
    X_train_m, X_test_m,y_train_m, y_test_m = cross_validation.train_test_split(xj,yj, test_size=0.3,random_state=random.randint(1, 10000))
    bdt.fit(X_train_m,y_train_m)
    print "Score : "+str(bdt.score(X_test_m,y_test_m, sample_weight=None))
    expected = y_test_m
    predicted = bdt.predict(X_test_m)
    print("Classification report for classifier %s:\n%s\n"
          % (bdt, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

def svm_test(xj,yj):
    print "Testing svm......."
    bdt = svm.SVC(gamma=0.001)
    X_train_m, X_test_m,y_train_m, y_test_m = cross_validation.train_test_split(xj,yj, test_size=0.3,random_state=random.randint(1, 10000))
    bdt.fit(X_train_m,y_train_m)
    print "Score : "+str(bdt.score(X_test_m,y_test_m, sample_weight=None))
    expected = y_test_m
    predicted = bdt.predict(X_test_m)
    print("Classification report for classifier %s:\n%s\n"
          % (bdt, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

if __name__ == '__main__':
    xj,yj = load_svmlight_file("only_wifi.txt")
    #xj,yj = load_svmlight_file("only_caffe_mean.txt")
    #xj,yj = load_svmlight_file("mixed.txt")
    bdt_test(xj,yj)
    svm_test(xj,yj)
