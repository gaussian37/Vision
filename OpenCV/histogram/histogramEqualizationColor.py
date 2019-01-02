import cv2
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Image path to the directory")
args = vars(ap.parse_args())
path = args['image']

# 입력 받은 이미지를 불러옵니다.
src = cv2.imread(path)

# hsv 컬러 형태로 변형합니다.
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
# h, s, v로 컬러 영상을 분리 합니다. 
h, s, v = cv2.split(hsv)
# v값을 히스토그램 평활화를 합니다.
equalizedV = cv2.equalizeHist(v)
# h,s,equalizedV를 합쳐서 새로운 hsv 이미지를 만듭니다.
hsv2 = cv2.merge([h,s,equalizedV])
# 마지막으로 hsv2를 다시 BGR 형태로 변경합니다.
hsvDst = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)

# YCrCb 컬러 형태로 변환합니다.
yCrCb = cv2.cvtColor(src, cv2.COLOR_BGR2YCrCb)
# y, Cr, Cb로 컬러 영상을 분리 합니다.
y, Cr, Cb = cv2.split(yCrCb)
# y값을 히스토그램 평활화를 합니다.
equalizedY = cv2.equalizeHist(y)
# equalizedY, Cr, Cb를 합쳐서 새로운 yCrCb 이미지를 만듭니다.
yCrCb2 = cv2.merge([equalizedV, Cr, Cb])
# 마지막으로 yCrCb2를 다시 BGR 형태로 변경합니다.
yCrCbDst = cv2.cvtColor(yCrCb2, cv2.COLOR_YCrCb2BGR)

# src, hsv, YCrCb 각각을 출력합니다.
cv2.imshow('src', src)
cv2.imshow('hsv dst', hsvDst)
cv2.imshow('YCrCb dst', yCrCbDst)
cv2.waitKey()
cv2.destroyAllWindows()
