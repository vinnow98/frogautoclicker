import cv2
import subprocess
import numpy as np
##SS
# def capture_screen():
#     result= subprocess.run(
#        ["adb","exec-out","screencap","-p"],  capture_output=True
#     )
   
#     image_array = np.frombuffer(result.stdout,dtype=np.uint8)
#     #SS arrives as rawbytes
#     image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
#     #OpenCV decodes the numbers into an image that can be analysed.
#     return image

# screen=capture_screen()
# cv2.imwrite("ad.png",screen)



# ##this is the screencropper
screen = cv2.imread("ad.png")
scale = 0.4
preview = cv2.resize(screen, None, fx=scale, fy=scale)

x, y, w, h = cv2.selectROI("Select icon, then press ENTER", preview, showCrosshair=True)
cv2.destroyAllWindows()

if w == 0 or h == 0:
    raise SystemExit("No selection made")

# convert back to full-resolution coordinates
x, y, w, h = [int(v / scale) for v in (x, y, w, h)]

template = screen[y:y+h, x:x+w]
cv2.imwrite("cross.png", template)
print("Saved template:", template.shape)







# subprocess.run([
#     "adb",
#     "shell",
#     "am",
#     "start",
#     "-a",
#     "android.settings.SETTINGS"
# ])

# #am : android activity manager
# #start: starts an android activity
# #-a : specifies an action
# # android.settings.SETTINGS: The action that opens Android Settings.

# print("Opened Android Settings!")

# the difference between exect-out and shell is that the screen show is sent directly thru ADB's outputstream. no file is created. Output can be accessed with result.stdout