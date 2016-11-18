import glob
import cv2
import numpy as np
import os
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report


manmade_src_dir_training = os.getcwd() + "/Images/manmade_training/out_manmade_1k/"
natural_src_dir_training = os.getcwd() + "/Images/natural_training/out_natural_1k/"

manmade_src_dir_test = os.getcwd() + "/Images/manmade_test/out_manmade_1k/"
natural_src_dir_test = os.getcwd() + "/Images/natural_test/out_natural_1k/"
#print(manmade_src_dir)
#print(natural_src_dir)

detect = cv2.xfeatures2d.SIFT_create()
extract = cv2.xfeatures2d.SIFT_create()
#detect = cv2.xfeatures2d.SURF_create()
#extract= cv2.xfeatures2d.SURF_create()

bow_train = cv2.BOWKMeansTrainer(1000)
bow_extract = cv2.BOWImgDescriptorExtractor(extract, cv2.BFMatcher(cv2.NORM_L1))


def read_src_images(imagePath):
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (50, 50))
       # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        i= detect.detect(image)
        return bow_extract.compute(image, i)


def read_src_images2(imagePath):
    image = cv2.imread(imagePath,0)
    image = cv2.resize(image, (50, 50))
    #image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    bow_train.add(feature_sift(image))


def define_prediction(value):
    if value[0] == 0:
        print(str(value), "Natural")
    elif value[0] ==1:
        print(str(value), "ManMade")


def compute_surf_keypoints(image):
    surf = cv2.xfeatures2d.SURF_create()
    kp, des = surf.detectAndCompute(image, None)
    return [kp,des]


def feature_sift(fn):
    n=detect.detect(fn)
    return extract.compute(fn, n)[1]


def feature_bow(fn):
    im = cv2.imread(fn, 0)
    image = cv2.resize(im, (50, 50))
   # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h=detect.detect(image)
    if h is not None:
        return bow_extract.compute(image, h)


def compute(test_src, results):
    for image_src in glob.glob(test_src + "*.jpg"):
        sample = feature_bow(image_src)
        if sample is not None:
            #total = total + 1
            p = svm.predict(sample)
            results.append(p[1][0][0])
            #if p[1][0][0] == 0:
            #    natural = natural + 1
            #elif p[1][0][0] == 1:
            #    man_made = man_made + 1


#Train man made
for imagePath in glob.glob(manmade_src_dir_training + "*.jpg"):
    read_src_images2(imagePath)

#Train natural
for imagePath in glob.glob(natural_src_dir_training + "*.jpg"):
    read_src_images2(imagePath)

#Create vocabulary
voc = bow_train.cluster()
bow_extract.setVocabulary(voc)

traindata, trainlabels = [],[]

#Extract
for i in glob.glob(manmade_src_dir_training + "*.jpg"):
    h=read_src_images(i)
    traindata.extend(h)
    trainlabels.append(1) #ManMade Label

for i in glob.glob(natural_src_dir_training + "*.jpg"):
    h = read_src_images(i)
    if h is not None:
        traindata.extend(h)
        trainlabels.append(0) #Natural Label

#Create SVM
svm = cv2.ml.SVM_create()
svm.train(np.array(traindata), cv2.ml.ROW_SAMPLE, np.array(trainlabels))

#svm.train(np.array(traindata), np.array(trainlabels))
#knn = KNeighborsClassifier(n_neighbors=5)
#knn.fit(traindata, np.array(trainlabels))
#man_made=0
#natural=0
#total=0
results=[]
labelMAN=[]
labelNAT=[]

compute(manmade_src_dir_test, results)
compute(natural_src_dir_test, results)

#Prepare labels
labelMAN = [1] * 248 #Since 2 images from natural images failed SIFT I removed 2 from both
labelNAT = [0] * 248


#Combine lables for test
labelcombined=labelMAN + labelNAT

# print "VALUE Natural ", natural
# print "VALUE manmade ", man_made
# print "VALUE TOTAL ", total

#Compute classification report
target_names = ["manmade", "natural"]
print classification_report(labelcombined,results, target_names=target_names)
