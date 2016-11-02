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
        self.orginal_img = cv2.imread(target_img_path).resize(out_img_dim[0], out_img_dim[1])
        self.tile_size = self.get_tile_size(num_of_tiles)
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

    def read_srs_images(self):
        for imagePath in glob.glob(os.getcwd() +
                                   "/Images/out_natural_1k/*.jpg"):
            filename = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            Compare.index[filename] = self.compute_histograms(filename, image)

    def calc_columns_rows(n):
        num_columns = int(ceil(sqrt(n)))
        num_rows = int(ceil(n / float(num_columns)))
        return (num_columns, num_rows)

    def get_tile_size(self, tiles):
        w, h = self.orginal_img.size
        columns, rows = self.calc_columns_rows(tiles)
        tile_w, tile_h = int(floor(w / columns)), int(floor(h / rows))
        return tile_w, tile_h

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
