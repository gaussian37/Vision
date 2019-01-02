import cv2
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Image path to the directory")
args = vars(ap.parse_args())
path = args['image']
fname = os.path.splitext(path)[0]

# 입력 받은 이미지를 불러옵니다.
src = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
# 불러온 이미지에 histogram equalization을 적용합니다.
dst = cv2.equalizeHist(src)
srcHist = cv2.calcHist(images = [src],
                       channels = [0],
                       mask = None,
                       histSize = [256],
                       ranges = [0, 256])

dstHist = cv2.calcHist(images = [dst],
                       channels = [0],
                       mask = None,
                       histSize = [256],
                       ranges = [0, 256])

cv2.imshow('src', src)
cv2.imshow('dst', dst)
plt.title('Grayscale histogram of {} image'.format(fname), fontSize = 16)
plt.plot(srcHist, color = 'b', label = 'src hist')
plt.plot(dstHist, color = 'r', label = 'dst hist')
plt.legend(loc='best')
plt.show()


cv2.waitKey()
cv2.destroyAllWindows()
