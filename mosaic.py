import glob
import cv2
import os
from sklearn.neighbors import KNeighborsClassifier


class Mosaic:
    index = {}
    OPENCV_METHODS = {"Correlation": cv2.HISTCMP_CORREL,
                      "Chi-Squared": cv2.HISTCMP_CHISQR,
                      "Intersection": cv2.HISTCMP_INTERSECT,
                      "Hellinger": cv2.HISTCMP_HELLINGER}

    def __init__(self, img_path, img_dim, tile_size, src_dir, dis_metric, out_name):
        self.img_name = img_path[img_path.rfind("/") + 1:]
        self.img_dim = img_dim
        self.org_img = self.process_target_image(img_path, img_dim[0], img_dim[1])
        self.source_dir = src_dir
        self.tile_size = tile_size
        self.dis_metric = dis_metric
        self.out_name = os.getcwd() +"/" + out_name + ".jpg"
        print 'output image dimensions are: ' + str(self.org_img.shape)
        self.manmade_src_dir = os.getcwd() + "/Images/manmade_training/out_manmade_1k/"
        self.natural_src_dir = os.getcwd() + "/Images/natural_training/out_natural_1k/"
        self.prediction = None

    def compute_histogram(self, image):
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hist = hist.flatten()
        return hist

    def process_target_image(self, img_path, height, width):
        image = cv2.imread(img_path)
        image = cv2.resize(image, (height, width))
        image = cv2.GaussianBlur(image, (11, 11), 0)
        return image

    def read_src_images(self):
        for imagePath in glob.glob(self.source_dir + "/*.jpg"):
            filename = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (50, 50))
            self.index[filename] = self.compute_histogram(image)

        print 'finished computing ' + str(len(Mosaic.index)) + ' histograms'

    def compare_histograms(self, win_hist, method):
        results = {}
        reverse = False

        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if method in ("Correlation", "Intersection"):
            reverse = True

        for (k, hist) in self.index.items():
            d = cv2.compareHist(win_hist, hist, self.OPENCV_METHODS[method])
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()], reverse=reverse)
        return results[0][1]

    def get_tile(self, img_name, tile_size):
        image = cv2.imread(self.source_dir + "/" + img_name)
        image = cv2.resize(image, (tile_size, tile_size))
        image = cv2.GaussianBlur(image, (11, 11), 0)
        return image

    def create_mosaic(self):
        (h, w, _) = self.org_img.shape
        tileSize = self.tile_size

        for i in range(0, h / tileSize):
            for j in range(0, w / tileSize):
                roi = self.org_img[i * tileSize:(i + 1) * tileSize,
                                   j * tileSize:(j + 1) * tileSize]
                hist = self.compute_histogram(roi)
                img = self.compare_histograms(hist, self.dis_metric)
                tile = self.get_tile(img, tileSize)
                self.org_img[i * tileSize:(i + 1) * tileSize,
                             j * tileSize:(j + 1) * tileSize] = tile
                cv2.imshow("Creating Mosaic", self.org_img)
                cv2.waitKey(1)

        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(self.out_name, self.org_img)

    def define_prediction(self, value):
        if value[0] == 0:
            self.prediction = 0
            print(str(value), "Natural")
        elif value[0] == 1:
            self.prediction = 1
            print(str(value), "ManMade")

    def read_src_images_partB(self,src_dir, index):
        for imagePath in glob.glob(src_dir + "*.jpg"):
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (50, 50))
            #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            index.append(self.compute_histogram(image))

    def update_src_images(self):
        if self.prediction == 1:
            self.source_dir = self.manmade_src_dir
        elif self.prediction == 0:
            self.source_dir = self.natural_src_dir

    def compute_partB(self):
        index = []
        # image_hist = compute_histogram(image)
        image = cv2.resize(self.org_img, (50, 50))
        #arr = np.concatenate(image)
        src_hist = self.compute_histogram(image)
        knn = KNeighborsClassifier(n_neighbors=5)

        self.read_src_images_partB(self.manmade_src_dir, index)
        labelM = [1] * len(index) # Label manmade
        length = len(index)
        self.read_src_images_partB(self.natural_src_dir, index)
        labelN = [0] * (len(index) - length) # Label natural

        responses = labelM + labelN # concatenate labels
        print 'feeding KNN to make an evaluation'
        print type(index[0][0])
        print type(src_hist)
        knn.fit(index, responses)

        self.define_prediction(knn.predict([src_hist])) #print value predicted
