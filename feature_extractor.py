import cv2


def compute_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    hist = hist.flatten()
    return hist
