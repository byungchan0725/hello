import cv2
from matplotlib import pyplot as plt

target = cv2.imread("./target.png", cv2.IMREAD_GRAYSCALE)




img1_src = cv2.imread("./screen_capture.png", cv2.IMREAD_GRAYSCALE)

# 템플릿 추출
template = target[800:950, 5:160]
w, h = template.shape[::-1] 

input = target.copy()
meth = 'cv2.TM_CCOEFF'
method = eval(meth)
res = cv2.matchTemplate(img1_src, template, method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    top_left = min_loc
else:
    top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(input, top_left, bottom_right, 0, 2)
center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
input = cv2.circle(input, center, 10, (255, 0, 0), -1)

# 템플릿 매칭 결과와 검출된 이미지 표시
cv2.imshow(f'Detected Point ({meth})', input)  # 검출된 이미지
# cv2.imshow(f'Detected Point ({meth})', template)  # 검출된 이미지

# 키 입력을 기다린 후 창을 닫기
cv2.waitKey(0)  # 아무 키나 입력될 때까지 창을 유지
cv2.destroyAllWindows()  # 모든 창 닫기