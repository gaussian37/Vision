import cv2
import numpy as np
import argparse

# argument parser를 구성해 주고 입력 받은 argument는 parse 합니다.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-t", "--type", required=True, help="mean or gaussian")
ap.add_argument("-b", "--block", required=True, help="Block size")
ap.add_argument("-c", "--c", default=0, help="Constant")
args = vars(ap.parse_args())

src = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
adaptive_type = args["type"]
blockSize = int(args["block"])
c = int(args["c"])

if adaptive_type == "mean":
    dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, blockSize, c)
    print("adaptiveThreshold Type : Mean")
elif adaptive_type == "gaussian":
    dst = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, blockSize, c)
    print("adaptiveThreshold Type : Gaussian")
else:
    ret, dst = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("Otsu, Optimal threshold : ", ret)
    
cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
