#!/usr/bin/env python
import cv2
import numpy as np
# third part 2
for val_i in range(5, 50, 5):
    image = cv2.imread('gray_' + str(val_i) + '_bin_thr_50.jpg', cv2.IMREAD_GRAYSCALE)


    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]
    print("height: {}, width: {}".format(h, w))

    # loop over the image, pixel by pixel
    # We want to iterate over blocks of 10
    # chunks = []
    # for i in range(0, 210, 10):
    #     for j in range(0, 210, 10):
    #         chunks.append((i, i + 10, j, j + 10))

    # print chunks

    # np.average


    def flatten(main_list):
        return [item for sublist in main_list for item in sublist]



    for pixel_min in range(1, 30, 2):
        fixed_img = image.copy()
        for x in range(0, 210, 10):
            for y in range(0, 210, 10):
                zero_pixels = 0
                one_pixels = 0
                for xx in range(x, x + 10):
                    subset = image[xx][y:y + 10]
                    print("len subset: " + str(len(subset)))
                    for pixel in subset:
                        if pixel < 5:
                            zero_pixels += 1
                        if pixel > 250:
                            one_pixels += 1
                    print("pixels of: [{}][{}:{}]: {}".format(
                        xx, y, y + 10, image[xx][y:y + 10]))
                    print("# zero value: " + str(zero_pixels))
                    print("# one value: " + str(one_pixels))


                print("On 10x10 block:")
                print("# zero value: " + str(zero_pixels))
                print("# one value: " + str(one_pixels))
                for xx in range(x, x + 10):
                    if one_pixels >= pixel_min:
                        fixed_img[xx][y:y + 10] = 0
                    else:
                        fixed_img[xx][y:y + 10] = 255



        cv2.imwrite('fixed_img_pixelmin_' + str(pixel_min) + '_minval_' + str(val_i)  + '.jpg', fixed_img)
