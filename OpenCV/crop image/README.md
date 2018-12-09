# 이미지 내에서 마우스 클릭으로 crop 하고 좌표 출력

이미지 내에서 ROI 영역을 crop 하고 싶을 때 사용할 수 있는 기본 코드 입니다.
코드를 응용하면 ROI 영역을 대상으로 Vision 처리를 할 수 있습니다.

코드는 다음을 참조하시기 바랍니다. <br>
https://gaussian37.github.io/vision-opencv-roi-extraction/

간단하게 실행하려면 아래와 같습니다.

```  
python crop_image.py --images "이미지 파일 경로"
```

<br>

+ 키보드에서 다음을 입력받아 수행합니다.
	- q : 작업을 끝냅니다.
	- r : 이미지를 초기화 합니다.
	- c : ROI 사각형을 그리고 좌표를 출력합니다.
