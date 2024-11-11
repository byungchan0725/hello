import mss
import time
import cv2
import numpy as np

def capture_screen():
    with mss.mss() as sct:
        # 휴대폰 연결 창 오른쪽위에 딱 맞추셈
        monitor = {
            "top": 80,    
            "left": 1208,  
            "width": 300,  
            "height": 650  
        }
        
        # Get raw pixels from the screen
        screenshot = np.array(sct.grab(monitor))
        
        # Convert from BGRA to BGR format for OpenCV
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        # Save the image
        cv2.imwrite("screen_capture.png", screenshot)
        # print("Captured screen and saved as 'screen_capture.png'")

# Capture screen every second
while True:
    try:
        capture_screen()
        time.sleep(0.1)
        print('이미지가 저장되었습니다.')
    except KeyboardInterrupt:
        print("\nScreen capture stopped")
        break