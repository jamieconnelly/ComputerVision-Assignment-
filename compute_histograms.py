from compare import Compare
import os
import json
import cv2
import glob


def compute_histograms(filename, image):
        Compare.images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        hist = hist.flatten()
        return hist


def main():
    json_array = []
    index = {}

    for imagePath in glob.glob(os.getcwd() + "/Images/out_natural_1k/*.jpg"):
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (100, 100))
        cv2.imwrite('test/' + filename, image)
        index['test/' + filename] = compute_histograms(filename, image).tolist()
        json_array.append(index)


if __name__ == "__main__":
    main()
