import cv2
import numpy as np
import argparse

# argument parser를 구성해 주고 입력 받은 argument는 parse 합니다.
ap = argparse.ArgumentParser()
# --image : 이미지를 입력 받습니다.
ap.add_argument("-i", "--image", required=True, help="Path to the image")
# --thresh : 임계값을 입력 받습니다. 미 입력시 Otsu를 사용합니다.
ap.add_argument("-th", "--thresh", default=-1, help="Threshold")
args = vars(ap.parse_args())

src = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)
thresh = int(args["thresh"])

# 임계값 미입력 시 Otsu 사용
if thresh == -1:
    ret, dst = cv2.threshold(src, thresh, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("Optimal threshold : ", ret)
elif thresh > 0:
    ret, dst = cv2.threshold(src, thresh, 255, cv2.THRESH_BINARY)

cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
