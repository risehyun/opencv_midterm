import cv2
import numpy as np

# 컬러 테이블을 생성하는 함수
def create_colorTable(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)

    # 테이블 전체가 입력된 컬러로 생성 되도록 지정해 줌.
    bar[:] = color

    # bgr 포맷을 rgb 포맷으로 바꾸기 위해 rgb 순서에 맞게 변수를 할당해 줌.
    red, green, blue = int(color[2]), int(color[1]), int(color[0])

    bgr_colors.append((blue, green, red))

    # 할당된 값들을 반환해 줌.
    return bar, (red, green, blue)

# 화면에 그림을 그리는 함수
def onMouse_draw(event, x, y, flags, param):
    global title, oldx, oldy

    if event == cv2.EVENT_LBUTTONDOWN:
        oldx, oldy = x, y

    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.imwrite('Result/DrawImage.jpg', canvas)
        print('Draw Image 저장')

    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            cv2.line(canvas, (oldx, oldy), (x, y), brush_color, 4, cv2.LINE_AA)
            cv2.imshow(title, canvas)
            oldx, oldy = x, y

def onMouse_colorTable(event, x, y, flags, param):
    global brush_color
    if event == cv2.EVENT_LBUTTONDOWN:
        i = 0
        for i in range(len(button_pt)):
            for j in range(0, 11):
                if y > button_pt[i][0] and y < button_pt[i][1] and x > button_pt[i][2] and x < button_pt[i][3]:
                    brush_color = bgr_colors[i]

    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.imwrite('Result/ColorTable.jpg', img_bar)
        print('COLOR TABLE 저장')

bgr_colors = []
brush_color = (0, 0, 0)
button_pt = [(0, 100, 0, 100), (0, 100, 100, 200), (0, 100, 200, 300), (0, 100, 300, 400), (0, 100, 400, 500),
(0, 100, 500, 600), (0, 100, 600, 700), (0, 100, 700, 800), (0, 100, 800, 900), (0, 100, 900, 1000)]
button_pt = np.array(button_pt)

canvas = np.full((300, 400, 3), (255, 255, 255), np.uint8)
pt = (-1, -1)
title = 'Draw Canvas'

# 이미지를 읽어 옴.
img = cv2.imread('Image/cat.jpg')

# 이미지의 높이와 너비를 알기 위해 픽셀을 행렬로 나타내 크기를 알아냄.
height, width, _ = np.shape(img)

# 클러스터링을 위해 새로운 변수를 생성함. 사용할 이미지 행렬, 크기(모든 픽셀을 포함하기 위해 높이*너비를 곱함), 컬러 채널 3개(rgb)를 할당 함.
data = np.reshape(img, (height * width, 3))

# 이후에 있을 계산을 위해 데이터를 float 타입으로 변환해 줌.
data = np.float32(data)

# 클러스터 수를 정의함.
number_clusters = 10

# 알고리즘 종료의 기준을 지정함. (최대 반복 횟수 or 원하는 정확도)
# 정확도는 각 클러스터 센터가 일부 반복에서 기준 엡실론보다 적게 이동하는 즉시 기준 엡실론으로 지정됨.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# 반복 중에 랜덤한 초기 center를 선택함.
flags = cv2.KMEANS_RANDOM_CENTERS

# kmean 함수가 반환한 값을 저장할 변수를 생성하고 사용할 변수, 데이터 클러스터수, 플래그, 기준 등을 할당해 줌.
compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)

font = cv2.FONT_HERSHEY_DUPLEX
bars = []
rgb_values = []

for index, row in enumerate(centers):
    bar, rgb = create_colorTable(100, 100, row)
    bars.append(bar)
    rgb_values.append(rgb)

img_bar = np.hstack(bars)

for index, row in enumerate(rgb_values):
    image = cv2.putText(img_bar, f'{index + 1}', (5 + 100 * index, 20 - 1),
                        font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
#    colors.append(row);
#    print(bgr_colors)
    print(f'{index + 1}. RGB{row}')

h, w, _ = np.shape(img_bar)
print(h, w)


# 화면을 출력합니다.
cv2.imshow('Image', img)
cv2.imshow('Color Table', img_bar)
cv2.imshow(title, canvas)
cv2.setMouseCallback(title, onMouse_draw)
cv2.setMouseCallback('Color Table', onMouse_colorTable)


# 윈도우 화면을 지정된 위치로 이동합니다.
cv2.moveWindow('Image', 200, 200)
cv2.moveWindow(title, 800, 200)
cv2.moveWindow('Color Table', 200, 550)


cv2.waitKey(0)