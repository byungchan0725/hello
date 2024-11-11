import mss
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

target = cv2.imread("./target.png", cv2.IMREAD_GRAYSCALE)
# template = target[800:950, 5:160]
#     w, h = template.shape[::-1] 
    
#     input = target.copy()

def search_target():
    screen = cv2.imread("./screen_capture.png", cv2.IMREAD_GRAYSCALE)
    
    # 템플릿 추출
    template = target[800:950, 5:160]
    w, h = template.shape[::-1] 
    
    input = target.copy()
    meth = 'cv2.TM_CCOEFF'
    method = eval(meth)
    res = cv2.matchTemplate(screen, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(input, top_left, bottom_right, 0, 2)
    center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
    input = cv2.circle(input, center, 10, (255, 0, 0), -1)
    cv2.imshow(f'Detected Point ({meth})', input)
    cv2.waitKey(1)  # 1ms 대기 추가

def capture_screen():
    with mss.mss() as sct:
        # 휴대폰 연결 창 오른쪽위에 딱 맞추셈
        monitor = {
            "top": 80,    
            "left": 1208,  
            "width": 300,  
            "height": 650  
        }
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        cv2.imwrite("screen_capture.png", screenshot)
        time.sleep(0.2)
        search_target()

while True:
    try:
        capture_screen()
        time.sleep(0.1)
        print('이미지가 저장되었습니다.')
        if cv2.waitKey(1) & 0xFF == ord('q'):  # q를 누르면 종료
            break
    except KeyboardInterrupt:
        print("\nScreen capture stopped")
        break
    
cv2.destroyAllWindows()  # 모든 창 닫기