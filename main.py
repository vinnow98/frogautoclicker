import subprocess
import time
import numpy as np
import cv2

def capture_screen():
    result= subprocess.run(
       ["adb","exec-out","screencap","-p"],  capture_output=True
    )
   
    image_array = np.frombuffer(result.stdout,dtype=np.uint8)
    #SS arrives as rawbytes
    image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
    #OpenCV decodes the numbers into an image that can be analysed.
    return image

threshold = 0.75
poll_interval = 0  # seconds between checks
cooldown = 0.1 
templates = {
            "ad_money" : cv2.imread("ad_money.png"),
            "free_money" : cv2.imread("free_money.png"),
            "tip_money" : cv2.imread("tip_money.png"),
            "tip_money1" : cv2.imread("tip_money1.png"),
            "tip_money2" : cv2.imread("tip_money2.png"),
            "cross" : cv2.imread("cross.png"),
            }
try:
    while True:
        screen = capture_screen()
        if screen is not None:
            height,width,channels = screen.shape
        else:
            print("Failed to capture screen.")
            time.sleep(3)
            continue

        tapped = False
      

        for name, template in templates.items():
            if template is None:
                print(f"Can't find {name}!")
                continue
            result = cv2.matchTemplate(screen,template,cv2.TM_CCOEFF_NORMED)
            
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                x, y = max_loc
                h, w = template.shape[:2]
                cx, cy = x + w // 2, y + h // 2
                print(f"{name} found ({max_val:.2f}), tapping {cx},{cy}")
                subprocess.run(["adb", "shell", "input", "tap", str(cx), str(cy)])
                tapped = True
                break   # one tap per loop; remove to tap both
        time.sleep(cooldown if tapped else poll_interval)

except KeyboardInterrupt:
    print("Stopped.")

        

