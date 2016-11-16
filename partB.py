import glob
import cv2
import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

manmade_src_dir = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/manmade_training/out_manmade_1k/"
natural_src_dir = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/natural_training/out_natural_1k/"


def compute_histogram(image):
   hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                       [0, 256, 0, 256, 0, 256])
   cv2.normalize(hist, hist)
   hist = hist.flatten()
   return hist


def compute_surf_keypoints(image):
    surf = cv2.xfeatures2d.SURF_create()
    kp, des = surf.detectAndCompute(image, None)
    return [kp,des]

def read_src_images(src_dir, index, bow):
    for imagePath in glob.glob(src_dir + "*.jpg"):
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (50, 50))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        tup = compute_surf_keypoints(gray_image)
        if tup[1] is None:
            print imagePath
        else:
            bow.add(tup[1])
            index.append(gray_image)
        #index.append(compute_surf_keypoints(gray_image))
        #index.append(compute_histogram(imge))


def define_prediction(value):
    if value[0] == 0:
        print(str(value), "Natural")
    elif value[0] ==1:
        print(str(value), "ManMade")


# def main():
#     index = []
#     #image_src = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
#     image_src = "/home/frank/OpenCV/ImagesAssignment/Images/manmade_test/out_manmade_1k/sun_buodnughobwntsgs.jpg"
#     #image_src ="/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
#     #image_src = "/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_adbhgoutrrryfwya.jpg"
#     image = cv2.imread(image_src)
#     # image_hist = compute_histogram(image)
#     image = cv2.resize(image, (50, 50))
#     #arr = np.concatenate(image)
#     arr = compute_histogram(image)
#     knn = KNeighborsClassifier(n_neighbors=5)
#
#     read_src_images(manmade_src_dir, index)
#     r1 = [1] * len(index) # Label manmade
#     length = len(index)
#     read_src_images(natural_src_dir, index)
#     r2 = [0] * (len(index) - length) # Label natural
#
#     responses = r1 + r2 # concatenate labels
#     print 'feeding KNN to make an evaluation'
#     print type(index[0][0])
#     print type(arr)
#     knn.fit(index, responses)
#
#     define_prediction(knn.predict([arr])) #print value predicted
def main():
    indexM=[]
    indexN=[]
    image_src = "/home/frank/OpenCV/ImagesAssignment/Images/manmade_test/out_manmade_1k/sun_buodnughobwntsgs.jpg"
    image = cv2.imread(image_src)
    image = cv2.resize(image, (50, 50))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    arr = compute_surf_keypoints(gray_image)

    bow=cv2.BOWKMeansTrainer(20)
    read_src_images(natural_src_dir, indexN, bow)
    read_src_images(manmade_src_dir, indexM, bow)
    voc = bow.cluster();
    surf = cv2.xfeatures2d.SURF_create()
    bowDE = cv2.BOWImgDescriptorExtractor(surf, cv2.BFMatcher(cv2.NORM_L2))
    bowDE.setVocabulary(voc)
    traindata=[]
    label=[]
    #out=np.array([])
    for i in indexN:
        tup=compute_surf_keypoints(i)
        data =bowDE.compute(i,tup[0], tup[1])
        traindata.append(tup[1].flatten())
        label.append(1)
    for i in indexM:
        tup=compute_surf_keypoints(i)
        data = bowDE.compute(i, tup[0],tup[1])
        traindata.append(tup[1].flatten())
        label.append(0)

    model = svm.SVC()
   #  svm_params = dict(kernel_type=cv2.ml.SVM_LINEAR, svm_type=cv2.ml.SVM_C_SVC, C=2.67, gamma=3)
   #  svm = cv2.ml.SVM_create()
   #  #svm.setType(cv2.ml.SVM_C_SVC)
   # # svm.setKernel(cv2.ml.SVM_LINEAR)
   # # svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))
    print len(traindata)
    print len(label)
    model.fit(traindata, label)
    # svm.train(traindata,label, params=svm_params)
    #knn = KNeighborsClassifier(n_neighbors=5)
    # read_src_images(manmade_src_dir, index)
    # r1 = [1] * len(index) # Label manmade
    # length = len(index)
    #
    # r2 = [0] * (len(index) - length) # Label natural
    # responses = r1 + r2  # concatenate labels

    print 'feeding KNN to make an evaluation'
    #print type(index)
    #print type(arr)
    response = model.predict(arr)
    print response
    #knn.fit(traindata, label)
    #define_prediction(knn.predict([arr])) #print value predicted


if __name__ == '__main__':
    main()
