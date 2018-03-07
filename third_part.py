#!/usr/bin/env python

from PIL import Image
import cv2
import numpy as np

img = Image.open('qrcore.jpg')
img_np = cv2.imread('qrcore.jpg')


img_hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)

low = np.array([0, 0, 0])
highs = []
for max_v in range(1, 50):
    highs.append(np.array([255, 255, max_v]))

masks = []
img_names = []
for high in highs:
    mask_ = cv2.inRange(img_hsv, low, high)
    masks.append(mask_)
    img_name = 'mask_' + str(high[2]) + '.jpg'
    img_names.append(img_name)
    cv2.imwrite(img_name, mask_)

masks_from_files = []
for img_name in img_names:
    masks_from_files.append(cv2.imread(img_name))
bin_thresholds = [1, 2, 5, 10, 50]
for bin_thr in bin_thresholds:
    for idx, mask in enumerate(masks_from_files):
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, gray_mask_bin = cv2.threshold(
            gray, bin_thr, 255, cv2.THRESH_BINARY)
        cv2.imwrite('gray_' + str(idx + 5) + '_bin_thr_' +
                    str(bin_thr) + '.jpg', gray_mask_bin)


# res = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)

# cv2.imshow('hsv img', img_hsv)
# cv2.imshow('mask', mask)
# cv2.imshow('res', res)

# k = cv2.waitKey(0)

# cv2.destroyAllWindows()
