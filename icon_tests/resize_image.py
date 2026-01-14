
import cv2
import numpy as np


sizes = [32,64,128,256]
img = cv2.imread('icon_no_bg_gray.png')
for size in sizes:
    res = cv2.resize(img, dsize=(size, size), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("gray_icon/gray_icon"+str(size)+"x"+str(size)+".png",res)


#res = cv2.resize(img, dsize=(342, 108), interpolation=cv2.INTER_CUBIC)
#cv2.imwrite("complication/"+str(342)+"x"+str(108)+".png",res)
