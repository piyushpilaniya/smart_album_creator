from scipy.stats import wasserstein_distance
#from scipy.misc import imread
import cv2
import numpy as np

def get_histogram(img):
  '''
  Get the histogram of an image. For an 8-bit, grayscale image, the
  histogram will be a 256 unit vector in which the nth value indicates
  the percent of the pixels in the image with the given darkness level.
  The histogram's values sum to 1.
  '''
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w)

#a = imread('a.jpeg')
#b = imread('b.jpeg')
#c = imread('c.jpeg')
def get_similarity_measure(imagePath1, imagePath2):
  a = cv2.imread(imagePath1,0)
  b = cv2.imread(imagePath2,0)
  # c = cv2.imread('dm.jpeg',0)
  a_hist = get_histogram(a)
  b_hist = get_histogram(b)
  # c_hist = get_histogram(c)
  dist1 = wasserstein_distance(a_hist, b_hist)
  return dist1
  # dist2= wasserstein_distance(a_hist, c_hist)
  # dist3 = wasserstein_distance(c_hist, b_hist)

  # print(dist1)
  # print(dist2)
  # print(dist3)
