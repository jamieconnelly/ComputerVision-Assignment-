from skimage import feature, color, transform
import cv2


def compute_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    hist = hist.flatten()
    return hist


def compute_canny(image):
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = feature.canny(grey_image)
    return edges.flatten()


def compute_hog(image):
    grey_image = color.rgb2gray(image)
    grey_image = cv2.resize(grey_image, (50, 50), interpolation=cv2.INTER_AREA)
    hist, hog = feature.hog(grey_image, orientations=8, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualise=True)
    return hog.flatten()


def compute_hough(image):
    grey_image = color.rgb2gray(image)
    h, theta, distances = transform.hough_line(grey_image)
    return distances
