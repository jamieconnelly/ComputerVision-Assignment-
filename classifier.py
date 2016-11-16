from __future__ import division
from sklearn.neighbors import KNeighborsClassifier
import feature_extractor as fts
import glob
import cv2
import os
import sys

manmade_src_dir = os.getcwd() + "/Images/out_manmade_1k/"
natural_src_dir = os.getcwd() + "/Images/out_natural_1k/"
knn = KNeighborsClassifier(n_neighbors=31)

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


def create_training_set(feature):
    # calculate training images features
    manmade_imgs = read_images(manmade_src_dir, feature)
    natural_imgs = read_images(natural_src_dir, feature)
    # Label images as manmade or natural
    manmade_lbl = [1] * len(manmade_imgs) 
    natural_lbl = [0] * len(manmade_imgs)
     # concatenate labels and images
    responses = manmade_lbl + natural_lbl
    index = manmade_imgs + natural_imgs
    knn.fit(index, responses)
    

def predict(test_dir, feature):
    test_imgs = read_images(test_dir, feature)
    
    results = []
    for fts in test_imgs:
        results.append(knn.predict([fts])[0])

    correct = len(filter(lambda i: i == 1, results)) / len(test_imgs) * 100
    err = 100 - correct
    print 'correct: ', correct, '%, ', 'error: ', err, '%'


def main(argv):
    features = ['histogram']

    if len(argv) is not 2:
        print 'two arguments required, <feature> <test_directory>'
        sys.exit()
    
    feature = sys.argv[1].lower()
    if feature not in features:
        print 'please provide on of the following features: ' + str(features)
        sys.exit()
    
    test_dir = os.getcwd() + '/' + sys.argv[2]
    create_training_set(feature)
    predict(test_dir, feature)


if __name__ == '__main__':
    main(sys.argv[1:])