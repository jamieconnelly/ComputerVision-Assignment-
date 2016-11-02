import glob
import cv2
import os
from math import sqrt, ceil, floor


class Compare:
    index = {}
    images = {}
    OPENCV_METHODS = {
                    "Correlation": cv2.HISTCMP_CORREL,
                    "Chi-Squared": cv2.HISTCMP_CHISQR,
                    "Intersection": cv2.HISTCMP_INTERSECT,
                    "Hellinger": cv2.HISTCMP_HELLINGER}

    def __init__(self, target_img_path, out_img_dim, num_of_tiles):
        self.target_img_name = target_img_path[target_img_path.rfind("/") + 1:]
        self.out_img_dim = out_img_dim
        self.orginal_img = cv2.imread(target_img_path)
        self.orginal_img = cv2.resize(self.orginal_img, (out_img_dim[0], out_img_dim[1]))
        self.tile_size = int(floor(sqrt(num_of_tiles)))
        print self.tile_size
        self.read_src_images()
        # self.org_img_hist = self.compute_histograms(self.target_img_name, self.orginal_img)

    def compute_histograms(self, filename, image):
        Compare.images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hist = hist.flatten()
        return hist

    def read_src_images(self):
        for imagePath in glob.glob(os.getcwd() +
                                   "/Images/out_natural_1k/*.jpg"):
            filename = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            Compare.index[filename] = self.compute_histograms(filename, image)

    def compare_histograms(self, method):
        results = {}
        reverse = False

        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if method in ("Correlation", "Intersection"):
            reverse = True

        for (k, hist) in self.index.items():
            # compute the distance between the two histograms
            d = cv2.compareHist(self.org_img_hist, hist,
                                self.OPENCV_METHODS[method])
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()],
                         reverse=reverse)
        return results[0]
