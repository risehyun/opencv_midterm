import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL

# 불러올 이미지를 지정 합니다.
img = cv2.imread("image/testImage.jpg")

# 생성할 윈도우의 이름을 지정 합니다.
title, title2, title3 = 'Original Image', 'Color Table', 'Result Image'

# 윈도우를 생성 합니다.
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(title2, cv2.WINDOW_AUTOSIZE)
cv2.namedWindow(title3, cv2.WINDOW_AUTOSIZE)

# 이미지를 윈도우에 표시 합니다.
cv2.imshow(title, img)

# 키 이벤트를 대기 합니다.
cv2.waitKey(0)

# 열린 모든 윈도우를 제거 합니다.
cv2.destroyAllWindows()