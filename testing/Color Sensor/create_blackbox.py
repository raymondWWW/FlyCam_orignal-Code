"""
Placeholder Code to create black box, to be used for visual feedback for color sensor
"""

import cv2
import numpy as np
import random

# Channels, in BGR format
B = 0; G = 1; R = 2

height = 100
width = 100
channels = 3

# create black background in OpenCV Image format
background_image = np.zeros((height, width, channels),dtype='uint8') # black display

# Change color of background, method 1 (one channel at a time)
# background_image[:, :, B] = random.randint(0, 255)
#
# background_image[:, :, G] = random.randint(0, 255)
#
# background_image[:, :, R] = random.randint(0, 255)

# Change color of background, method 2 (using a list)
random_b = random.randint(0, 255)
random_g = random.randint(0, 255)
random_r = random.randint(0, 255)
random_color = [random_b, random_g, random_r]
background_image[:, :, :] = random_color

# Idea for method 3, pick 3 "cards" with replacement, store in a list. Should allow for a one-two liner of code.

cv2.imshow("background_image", background_image)
cv2.waitKey(10000)