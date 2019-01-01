import cv2
import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.mplot3d import Axes3D

def compareColorHistogram(image, histSize, fname):
    '''
    R,G,B 히스토그램 각각을 그래프에 표시하여 비교하는 함수
    '''
    histColor = ['b', 'g', 'r']
    # 총 256개의 픽셀 값에서 histSize 만큼 나눠 주게 되면 hist 구간의 갯수가 됩니다.
    nbins = 256 // histSize
    # x축을 nbins 만큼의 구간으로 만들되 각 tick를 [0, 255] 까지 범위로 만들어 줍니다.
    binX = np.arange(histSize) * nbins
    # B, G, R 을 차례로 접근하면서 히스토그램을 각 색깔에 맞게 그립니다.
    for i in range(3):
        hist = cv2.calcHist(images = [image],
                            channels = [i],
                            mask = None,
                            histSize = [histSize],
                            ranges = [0, 256])
        plt.plot(binX, hist, color = histColor[i])
    # plot의 제목을 출력합니다.
    plt.suptitle("{} image histogram".format(fname), fontsize = 16)
    plt.show() 

def compareColorHistogram2d(image, histSize, fname):
    '''
    R,G,B 3가지를 2개씩 묶어서 나올 수 있는 경우의 수를 모두 2d로 표현하는 함수
    '''
    # (R, G), (G, B), (R, B) 3가지 경우의 수를 표현할 수 있도록 subplot을 구성합니다.
    fig, axes = plt.subplots(1, 3, figsize=(15, 7))
    channels_mapping = {0: 'B', 1: 'G', 2: 'R'}
    for i, channels in enumerate([[0, 1], [0, 2], [1, 2]]):
        # cv2.calcHist 함수를 통하여 이미지의 히스토그램을 구합니다.
        # 2 채널의 이미지를 한번에 구해야 하므로 histSize와 ranges를 2개 입력해줍니다.
        hist = cv2.calcHist(images = [image],
                            channels = channels,
                            mask = None, 
                            histSize = [histSize] * 2,
                            ranges = [0, 256] * 2)

        # x축, y축에 입력 될 채널을 할당해 줍니다.
        channel_x = channels_mapping[channels[0]]
        channel_y = channels_mapping[channels[1]]
        
        # 각 subplot을 차례차례 접근합니다.
        ax = axes[i] 
        # subplot의 x, y축의 범위를 정합니다. 범위는 [0, histSize) 까지로 먼저 정합니다.
        ax.set_xlim([0, histSize - 1])
        ax.set_ylim([0, histSize - 1])
        
        # x와 y에 각각 어떤 color의 정보인지 기입합니다.
        ax.set_xlabel("{} color".format(channel_x))
        ax.set_ylabel("{} color".format(channel_y))
        
        # 각 subplot의 title을 입력합니다.
        ax.set_title(f'2D Color Histogram for {channel_x} and {channel_y}')

        # 히스토그램 구간 총 갯수
        nbins = 256 // histSize
        
        # ax.set_x/ylib에서 정했던 scale에 bin 갯수만큼 곱해주어 [0, 255]의 범위를 갖게 합니다.
        # 처음에 32개의 히스토그램 사이즈를 가지고 만들었다면, 각 채널당 8개의 구간이 존재합니다.
        # 처음 셋팅을 [0, histSize) 의 범위로 셋팅을 해주었기 때문에 bin의 갯수를 곱해주면
        # 전체 범위가 됩니다.
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: 
                                                   '{:}'.format(int(x*nbins))))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: 
                                                   '{:}'.format(int(x*nbins))))
        # img에 histogram들을 저장합니다.
        img = ax.imshow(hist)

    # image 상단부에는 subplot들이 있고 하단부에 colorbar를 그려줍니다.
    fig.colorbar(img, ax=axes.ravel().tolist(), orientation='orizontal')
    fig.suptitle('2D Color Histograms with {} histSize with {} image'.format(
                    histSize, fname), fontsize=32)
    plt.show()

ap = argparse.ArgumentParser()
# 이미지 경로를 받습니다.
ap.add_argument("-i", "--image", required=True, help="Image path")
# 히스토그램의 간격 사이즈를 받습니다.
ap.add_argument("-b", "--bins", required=True, help="Each hist size")
args = vars(ap.parse_args())
path = 'lenna.png' # args["image"]
histSize = 32 # int(args['bins'])

# 그래프 제목을 출력하기 위해 입력받은 사진의 이름을 저장합니다.
fname = os.path.splitext(path)[0]
# 이미지를 color로 불러옵니다.
src = cv2.imread(path, cv2.IMREAD_COLOR)

compareColorHistogram(src, histSize, fname)
compareColorHistogram2d(src, histSize, fname)
