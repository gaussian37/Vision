import argparse
import cv2
import numpy as np

# findLocalMaxima()는 src에서 Morphology 연산(팽창 & 침식)으로 
# Local maxia의 좌표를 points 배열에 검출하여 반환함
def findLocalMaxima(src):
    kernel= cv2.getStructuringElement(shape = cv2.MORPH_RECT, ksize = (11,11))
    
    # cv2.dilate()로 src에서 rectKernel의 이웃에서 최댓값을 dilate에 계산
    # kernel = None을 사용하면 기본적으로 3 x 3 커널이 사용됩니다.
    dilate = cv2.dilate(src, kernel)
    
    # src == dilate 연산으로 src에서 local maxima 위치를 localMax 배열에 계산합니다.
    localMax = (src == dilate)

    # cv2.erode()로 src에서 rectKernel의 이웃에서 최솟값을 erode에 계산합니다.
    erode = cv2.erode(src, kernel) # local min if kernel = None, 3x3
    
    # src > erode로 최솟값보다 큰 위치를 localMax2에 계산합니다.
    localMax2 = src > erode 
    
    # & 연산으로 local maxima 위치를 계산
    localMax &= localMax2
    
    # 행,열 순서로 localMax 위치를 찾습니다.
    points = np.argwhere(localMax == True)
    
    # 좌표 순서를 열(x), 행(y)으로 변경 합니다.
    points[:,[0,1]] = points[:,[1,0]] # switch x, y 
    return points

# argument parser를 구성해 주고 입력 받은 argument는 parse 합니다.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

src = cv2.imread(args["image"])

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# grayscale의 gray에서 cv2.preCornerDetect()로 res를 계산합니다.
res = cv2.preCornerDetect(gray, ksize = 3)

# 극대값만을 찾기 위해서 np.abs(res)인 절대값 배열에서
# cv2.threshold()로 임계값 thresh = 0.1 보다 작은 값은 0으로 변경하여 res2에 저장합니다.
# res에서 임계값보다 작은 값을 제거 합니다.
# findLocalMaxima() 함수를 통해 res2에서 
# 지역 극값의 좌표를 코너점으로 찾아 corners에 저장합니다.
ret, res2 = cv2.threshold(np.abs(res), 0.1, 0, cv2.THRESH_TOZERO)

# corner를 저장합니다.
corners = findLocalMaxima(res2) 
print('corners.shape=', corners.shape)

# src를 dst에 복사하고, 코너점 배열 corners의 각 코너점 좌표에 cv2.circle()로
# dst에 반지름 5, 빨간색 원을 그립니다.
dst = src.copy()
for x, y in corners:
    cv2.circle(dst, (x, y), 5,(0, 0, 255), 2)

cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()