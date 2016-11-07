import glob
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

manmade_src_dir = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/manmade_training/out_manmade_1k/"
natural_src_dir = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/natural_training/out_natural_1k/"


def compute_histogram(image):
   hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                       [0, 256, 0, 256, 0, 256])
   cv2.normalize(hist, hist)
   hist = hist.flatten()
   return hist


def read_src_images(src_dir, index):
    for imagePath in glob.glob(src_dir + "*.jpg"):
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (50, 50))
        index.append(compute_histogram(image))


def define_prediction(value):
    if value[0] == 0:
        print(str(value), "Natural")
    elif value[0] ==1:
        print(str(value), "ManMade")


def main():
    index = []
    #image_src = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
    #image_src = "/home/frank/OpenCV/ImagesAssignment/Images/natural_training/out_natural_1k/sun_aachaucttrrkdicr.jpg"
    #image_src ="/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
    image_src = "/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_adbhgoutrrryfwya.jpg"
    image = cv2.imread(image_src)
    # image_hist = compute_histogram(image)
    image = cv2.resize(image, (50, 50))
    #arr = np.concatenate(image)
    arr = compute_histogram(image)
    knn = KNeighborsClassifier(n_neighbors=5)

    read_src_images(manmade_src_dir, index)
    r1 = [1] * len(index) # Label manmade
    length = len(index)
    read_src_images(natural_src_dir, index)
    r2 = [0] * (len(index) - length) # Label natural

    responses = r1 + r2 # concatenate labels
    print 'feeding KNN to make an evaluation'
    knn.fit(index, responses)

    define_prediction(knn.predict([arr])) #print value predicted

if __name__ == '__main__':
    main()