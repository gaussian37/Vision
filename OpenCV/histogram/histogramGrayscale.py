import cv2
import os
import numpy as np
import argparse
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
# 이미지 경로를 받습니다.
ap.add_argument("-i", "--image", required=True, help="Image path")
# 히스토그램의 간격 사이즈를 받습니다.
ap.add_argument("-b", "--bins", required=True, help="Each hist size")
args = vars(ap.parse_args())

path = args["image"]
histSize = int(args['bins'])

# 그래프 제목을 출력하기 위해 입력받은 사진의 이름을 저장합니다.
fname = os.path.splitext(path)[0]
# 이미지를 grayscale로 불러옵니다.
src = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
# 이미지의 히스토그램을 입력받은 histSize 간격으로 계산합니다.
hist = cv2.calcHist(images = [src], 
                    channels = [0],
                    mask = None, 
                    histSize = [histSize],
                    ranges = [0, 256])

# 히스토그램을 flatten 하여 1차원 배열로 만듭니다.
histFlatten = hist.flatten()
# 히스토그램 bin의 간격에 맞게 [0, 255] 범위의 x축 범위를 만듭니다.
binX = np.arange(histSize) * (256//histSize)

# 히스토그램의 제목을 출력합니다.
plt.title("Histogram of grayscale " + fname + " image")
# 히스토그램의 중앙값을 선으로 연결합니다.
plt.plot(binX, histFlatten, color = 'r')
# 히스토그램을 그립니다.
plt.bar(binX, histFlatten, width = 8, color = 'b')
plt.show()
