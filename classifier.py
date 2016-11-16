from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import svm
import feature_extractor as fts
import glob
import cv2
import os
import sys

knn = KNeighborsClassifier(n_neighbors=5)
svm = svm.SVC()


def read_images(src_dir, feature):
    feature_list = []
    for imagePath in glob.glob(src_dir + "*.jpg"):
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (50, 50))
        image = cv2.GaussianBlur(image, (11, 11), 0)
        if feature == 'histogram':
            hist = fts.compute_histogram(image)
            feature_list.append(hist)
    return feature_list


def calc_features_and_labels(manmade_dir, natural_dir, feature):
    # calculate images features
    manmade_imgs = read_images(manmade_dir, feature)
    natural_imgs = read_images(natural_dir, feature)
    # Label images as manmade or natural
    manmade_lbl = [1] * len(manmade_imgs)
    natural_lbl = [0] * len(natural_imgs)
    # concatenate label and image lists
    responses = manmade_lbl + natural_lbl
    index = manmade_imgs + natural_imgs
    return index, responses


def create_training_set(feature):
    manmade_dir = os.getcwd() + "/Images/manmade_training/out_manmade_1k/"
    natural_dir = os.getcwd() + "/Images/natural_training/out_natural_1k/"
    index, responses = calc_features_and_labels(manmade_dir, natural_dir, feature)
    knn.fit(index, responses)
    svm.fit(index, responses)


def predict(feature):
    manmade_test = os.getcwd() + "/Images/manmade_test/"
    natural_test = os.getcwd() + "/Images/natural_test/"
    index, responses = calc_features_and_labels(manmade_test, natural_test, feature)

    results_knn = []
    results_svm = []
    for feat in index:
        results_knn.append(knn.predict([feat])[0])
        results_svm.append(svm.predict([feat])[0])
    
    target_names = ['manmade', 'natural']
    print 'KNN Classifier'
    print classification_report(responses, results_knn, target_names=target_names)
    print 'SVM Classifier'
    print classification_report(responses, results_svm, target_names=target_names)


def main(argv):
    features = ['histogram']

    if len(argv) is not 1:
        print 'two arguments required, <feature> <test_directory>'
        sys.exit()

    feature = sys.argv[1].lower()
    if feature not in features:
        print 'please provide on of the following features: ' + str(features)
        sys.exit()

    create_training_set(feature)
    predict(feature)


if __name__ == '__main__':
    main(sys.argv[1:])
