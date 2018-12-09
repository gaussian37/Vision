import argparse
import cv2

# Points 들을 저장할 리스트와 Crop이 실행 되었는지 저장할 Boolean 변수를 선언합니다.
refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
	# refPt와 cropping 변수를 global로 만듭니다.
	global refPt, cropping

	# 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
	# cropping = True로 만들어 줍니다.
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# 왼쪽 마우스 버튼이 놓여지면 (x, y) 좌표 기록을 하고 cropping 작업을 끝냅니다.
	# 이 때 crop한 영역을 보여줍니다.
	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		cropping = False
 
		# ROI 사각형을 이미지에 그립니다.
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)


# argument parser를 구성해 주고 입력 받은 argument는 parse 합니다.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
 
# 이미지를 load 합니다.
image = cv2.imread(args["image"])
# 원본 이미지를 clone 하여 복사해 둡니다.
clone = image.copy()
# 새 윈도우 창을 만들고 그 윈도우 창에 click_and_crop 함수를 세팅해 줍니다.
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)


'''
키보드에서 다음을 입력받아 수행합니다.
- q : 작업을 끝냅니다.
- r : 이미지를 초기화 합니다.
- c : ROI 사각형을 그리고 좌표를 출력합니다.
'''
while True:
	# 이미지를 출력하고 key 입력을 기다립니다.
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# 만약 r이 입력되면, crop 할 영열을 리셋합니다.
	if key == ord("r"):
		image = clone.copy()

 	# 만약 c가 입력되고 ROI 박스가 정확하게 입력되었다면
	# 박스의 좌표를 출력하고 crop한 영역을 출력합니다.
	elif key == ord("c"):
		if len(refPt) == 2:
			roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
			print(refPt)
			cv2.imshow("ROI", roi)
			cv2.waitKey(0)
	# 만약 q가 입력되면 작업을 끝냅니다.
	elif key == ord("q"):
		break
 
# 모든 window를 종료합니다.
cv2.destroyAllWindows()
