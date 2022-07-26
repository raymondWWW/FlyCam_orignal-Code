"""
Code Source:
https://stackoverflow.com/questions/64965843/opencv-videowriter-writes-an-empty-video

"""


import cv2
import numpy as np
import time
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


img = np.zeros((640, 480))

center_x = 0
center_y = 256

# videoFile1 = 'video.mp4'

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('SaveVideo2.avi', fourcc, 20.0, (480, 640), isColor=False)

while True:
    img = np.zeros((640, 480), dtype=np.uint8)
    img = cv2.circle(img, (center_x, center_y), 20, 120, -1)

    cv2.imshow('img', img)
    out.write(img)

    center_x += 3
    time.sleep(1/30)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
