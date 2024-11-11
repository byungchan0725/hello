import mss
import time
import cv2
import numpy as np

def search_target():
    # 이미지 읽기 및 그레이스케일 변환
    screen = cv2.imread("./screen_capture.png", cv2.IMREAD_GRAYSCALE)
    target = cv2.imread("./target.png", cv2.IMREAD_GRAYSCALE)
    
    # 템플릿 추출
    template = target[895:1020, 140:340]
    w, h = template.shape[::-1]
    
    # 빠른 매칭을 위한 이미지 크기 조정
    scale = 0.5
    small_screen = cv2.resize(screen, None, fx=scale, fy=scale)
    small_template = cv2.resize(template, None, fx=scale, fy=scale)
    
    # 템플릿 매칭 수행
    res = cv2.matchTemplate(small_screen, small_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    # 원본 크기로 좌표 변환
    top_left = (int(max_loc[0]/scale), int(max_loc[1]/scale))
    bottom_right = (int((max_loc[0] + small_template.shape[1])/scale), 
                   int((max_loc[1] + small_template.shape[0])/scale))
    
    # 결과 표시
    if max_val > 0.9:  # 신뢰도 임계값
        result_img = cv2.imread("./screen_capture.png")
        cv2.rectangle(result_img, top_left, bottom_right, (0,255,0), 2)
        cv2.imshow('Result', result_img)

def capture_screen():
    with mss.mss() as sct:
        monitor = {
            "top": 80,    
            "left": 1208,  
            "width": 300,  
            "height": 650  
        }
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        cv2.imwrite("screen_capture.png", screenshot)

def main():
    while True:
        try:
            capture_screen()
            search_target()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()