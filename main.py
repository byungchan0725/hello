import mss
import cv2
import pyautogui
import numpy as np

def search_target(screen, template):
    # 빠른 매칭을 위한 이미지 크기 조정
    scale = 0.5  # 더 작은 스케일 사용
    small_screen = cv2.resize(screen, None, fx=scale, fy=scale)
    small_template = cv2.resize(template, None, fx=scale, fy=scale)
    
    # 템플릿 매칭 수행
    res = cv2.matchTemplate(small_screen, small_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    
    if max_val > 0.9:
        # 원본 크기로 좌표 변환
        center_x = int((max_loc[0] + small_template.shape[1]/2) / scale)
        center_y = int((max_loc[1] + small_template.shape[0]/2) / scale)
        # pyautogui.click(x=center_x//2, y=center_y//2)
        pyautogui.moveTo(x=center_x//2, y=center_y//2)
        return True
    return False

def main():
    # 템플릿 이미지 한 번만 로드
    target = cv2.imread("./full_target.png", cv2.IMREAD_GRAYSCALE)
    template = target[880:1030, 2510:2720]
    
    # mss 객체 재사용
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        
        while True:
            try:
                # 스크린샷을 파일로 저장하지 않고 직접 처리
                screenshot = np.array(sct.grab(monitor))
                gray_screen = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
                
                if search_target(gray_screen, template):
                    # 매칭 성공 시 잠시 대기
                    print('hello')
                    pyautogui.PAUSE = 0.1
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except KeyboardInterrupt:
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    pyautogui.PAUSE = 0  # PyAutoGUI 기본 딜레이 제거
    print('메크로가 시작되었습니다.')
    main()