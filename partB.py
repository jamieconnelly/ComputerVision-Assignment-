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


def read_src_images(src_dir, index, filename_arr):
    for imagePath in glob.glob(src_dir + "*.jpg"):
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (50, 50))
        #arr = np.concatenate(image)
        index.append(compute_histogram(image))
        filename_arr.append(filename)
        #index[filename] = image
        #index["matrix"] = image

def main():
    index =[]
    filename_arr = []
    #image_src = "/home/frank/OpenCV/ComputerVision-Assignment-/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
    #image_src = "/home/frank/OpenCV/ImagesAssignment/Images/natural_training/out_natural_1k/sun_aachaucttrrkdicr.jpg"
    #image_src ="/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_aabzgoowomavupwl.jpg"
    image_src = "/home/frank/OpenCV/ImagesAssignment/Images/natural_test/out_natural_1k/sun_adbhgoutrrryfwya.jpg"
    image = cv2.imread(image_src)
    # image_hist = compute_histogram(image)
    image = cv2.resize(image, (50, 50))
    #arr = np.concatenate(image)
    arr=compute_histogram(image)
    knn = KNeighborsClassifier(n_neighbors=5)

    read_src_images(manmade_src_dir, index, filename_arr)
    #r1 = np.full((1, len(index)), 0, dtype=np.int8)
    r1 = [0] * len(index)
    length = len(index)
    read_src_images(natural_src_dir, index, filename_arr)
    #r2 = np.full((1, (len(index) - length)), 1, dtype=np.int8)
    r2 = [1] * (len(index) - length)
    #responses = np.concatenate((r1, r2), axis=0)
    responses = r1 + r2
    print 'finished computing  histograms'
    knn.fit(index, responses)

    print(knn.predict([arr]))

if __name__ == '__main__':
    main()