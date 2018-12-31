# 이미지의 threshold를 구하는 함수

이미지 전처리를 할 때 종종 사용하는 threshold 함수 입니다.

내용은 다음을 참조하시기 바랍니다. <br>
https://gaussian37.github.io/vision-opencv-threshold/

간단하게 실행하려면 아래와 같습니다.

```  
python threshold.py --image="이미지 파일 경로" --thresh=임계값
```

```
python adaptiveThreshold.py --image="이미지 파일 경로" --type="mean 또는 gaussian 선택" --block=block 사이즈 --c=상수
```
