import glob
import cv2
import os
from math import sqrt, floor


class Compare:
    index = {}
    OPENCV_METHODS = {"Correlation": cv2.HISTCMP_CORREL,
                      "Chi-Squared": cv2.HISTCMP_CHISQR,
                      "Intersection": cv2.HISTCMP_INTERSECT,
                      "Hellinger": cv2.HISTCMP_HELLINGER}

    def __init__(self, img_path, img_dim, num_of_tiles, src_dir):
        self.img_name = img_path[img_path.rfind("/") + 1:]
        self.img_dim = img_dim
        self.org_img = cv2.imread(img_path)
        self.org_img = cv2.resize(self.org_img, (img_dim[0], img_dim[1]))
        self.source_dir = src_dir
        self.tile_size = 5  # int(floor(sqrt(num_of_tiles)))
        # self.validate_img_size(self.img_dim, self.tile_size, num_of_tiles)
        self.read_src_images()
        print self.org_img.shape

    def validate_img_size(self, h_w, tile_size, num_of_tiles):
        if (h_w[0] * h_w[1]) / (tile_size * tile_size) != num_of_tiles:
            # no of tiles doesnt fit output image dimensions, resize image
            self.org_img = cv2.resize(self.org_img,
                                      (h_w[0] / tile_size * tile_size,
                                       h_w[1] / tile_size * tile_size))

    def compute_histogram(self, image):
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hist = hist.flatten()
        return hist

    def read_src_images(self):
        for imagePath in glob.glob(self.source_dir + "/*.jpg"):
            filename = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (50, 50))
            Compare.index[filename] = self.compute_histogram(image)

        print 'finished computing ' + str(len(Compare.index)) + ' histograms'

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

    def get_tile(self, path, tileSize):
        image = cv2.imread(os.getcwd() + "/Images/training_mix/" + path)
        image = cv2.resize(image, (tileSize, tileSize))
        # image = cv2.GaussianBlur(image, (5, 5), 0)
        return image

    def create_mosaic(self):
        (h, w, _) = self.org_img.shape
        tileSize = self.tile_size

        for i in range(0, h / self.tile_size):
            for j in range(0, w / tileSize):
                roi = self.org_img[i * tileSize:(i + 1) * tileSize,
                                   j * tileSize:(j + 1) * tileSize]
                fts = self.compute_histogram(roi)
                img = self.compare_histograms(fts, 'Hellinger')
                tile = self.get_tile(img, tileSize)
                self.org_img[i * tileSize:(i + 1) * tileSize,
                             j * tileSize:(j + 1) * tileSize] = tile
                cv2.imshow("Progress", self.org_img)
                cv2.waitKey(1)

        cv2.imwrite("img.jpg", self.org_img.shape)
