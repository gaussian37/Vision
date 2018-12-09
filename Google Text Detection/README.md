# Google Vision API를 사용하여 문자 검출 

`google_text_detection.py`는 Google Vision API를 사용하여 이미지 내의 Text Detection을 수행합니다.
사용하기 전에 google cloud 환경과 API 인증에 필요한 json 파일 등록을 완료해야 사용할 수 있습니다.

환경 설정은 다음 내용을 참조 하시기 바랍니다.
https://gaussian37.github.io/Google-Vision-API/


### 사용 방법

``` python
import google_text_detection as gtd

ret = gtd.detect_text("image 파일 경로")
```

`ret`에는 검출한 텍스트 내용이 split 되어 list 형태로 반환됩니다.