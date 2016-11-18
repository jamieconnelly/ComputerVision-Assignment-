from skimage import feature, color
from sklearn import svm
import glob
import cv2
import os


class Mosaic:
    index = {}
    OPENCV_METHODS = {"Correlation": cv2.HISTCMP_CORREL,
                      "Chi-Squared": cv2.HISTCMP_CHISQR,
                      "Intersection": cv2.HISTCMP_INTERSECT,
                      "Hellinger": cv2.HISTCMP_HELLINGER}

    def __init__(self, img_path, img_dim, tile_size, dis_metric, out_name):
        self.img_name = img_path[img_path.rfind("/") + 1:]
        self.img_dim = img_dim
        self.org_img = self.process_target_image(img_path, img_dim[0], img_dim[1])
        self.src_dir = ''
        self.tile_size = tile_size
        self.dis_metric = dis_metric
        self.out_name = os.getcwd() + "/" + out_name + ".jpg"
        self.img_hog = self.compute_hog(self.org_img)

    def compute_histogram(self, image):
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hist = hist.flatten()
        return hist

    def compute_hog(self, image):
        grey_image = color.rgb2gray(image)
        grey_image = cv2.resize(grey_image, (50, 50),
                                interpolation=cv2.INTER_AREA)
        hist, hog = feature.hog(grey_image, orientations=8,
                                pixels_per_cell=(16, 16),
                                cells_per_block=(1, 1), visualise=True)
        return hog.flatten()

    def process_target_image(self, img_path, height, width):
        image = cv2.imread(img_path)
        image = cv2.resize(image, (height, width))
        image = cv2.GaussianBlur(image, (11, 11), 0)
        return image

    def read_src_images(self, dir):
        for imagePath in glob.glob(dir + "/*.jpg"):
            filename = imagePath[imagePath.rfind("/") + 1:]
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (50, 50))
            self.index[filename] = self.compute_histogram(image)

        print 'finished computing ' + str(len(Mosaic.index)) + ' histograms'

    def compare_histograms(self, win_hist, method):
        results = {}
        reverse = False

        # reverse order for correlation or intersection
        if method in ("Correlation", "Intersection"):
            reverse = True

        for (k, hist) in self.index.items():
            d = cv2.compareHist(win_hist, hist, self.OPENCV_METHODS[method])
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()],
                         reverse=reverse)
        return results[0][1]

    def get_tile(self, dir, img_name, tile_size):
        image = cv2.imread(dir + "/" + img_name)
        image = cv2.resize(image, (tile_size, tile_size))
        image = cv2.GaussianBlur(image, (11, 11), 0)
        return image

    def create_mosaic(self, dir):
        (h, w, _) = self.org_img.shape
        tileSize = self.tile_size

        for i in range(0, h / tileSize):
            for j in range(0, w / tileSize):
                roi = self.org_img[i * tileSize:(i + 1) * tileSize,
                                   j * tileSize:(j + 1) * tileSize]
                hist = self.compute_histogram(roi)
                img = self.compare_histograms(hist, self.dis_metric)
                tile = self.get_tile(dir, img, tileSize)
                self.org_img[i * tileSize:(i + 1) * tileSize,
                             j * tileSize:(j + 1) * tileSize] = tile
                cv2.imshow("Creating Mosaic", self.org_img)
                cv2.waitKey(1)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(self.out_name, self.org_img)

    def extract_hog_features(self, src_dir):
        feature_list = []
        for imagePath in glob.glob(src_dir + "*.jpg"):
            image = cv2.imread(imagePath)
            hog = self.compute_hog(image)
            feature_list.append(hog)
        return feature_list

    def calc_features_and_labels(self, manmade_dir, natural_dir):
        manmade_imgs = self.extract_hog_features(manmade_dir)
        natural_imgs = self.extract_hog_features(natural_dir)
        # Label images as manmade or natural
        manmade_lbl = [1] * len(manmade_imgs)
        natural_lbl = [0] * len(natural_imgs)
        # concatenate label and image lists
        responses = manmade_lbl + natural_lbl
        index = manmade_imgs + natural_imgs
        return index, responses

    def classify_img(self):
        manmade_dir = os.getcwd() + "/training_images/training/out_manmade_1k/"
        natural_dir = os.getcwd() + "/training_images/training/out_manmade_1k/"
        clsf = svm.LinearSVC()
        index, resp = self.calc_features_and_labels(manmade_dir, natural_dir)
        clsf.fit(index, resp)
        img_class = clsf.predict([self.img_hog])
        manmade_dir if img_class == 1 else natural_dir
        print 'target image is ([0] = natural, [1] = manmade): ', img_class
        return manmade_dir if img_class == 1 else natural_dir
