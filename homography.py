#!/usr/bin/env python

import cv2
import numpy as np

"""
# This function is used to calculate the Homography using the library CV2
# The common points of both images are hardcoded
# and we set the final day of the event
#  input : - (Because the input images are hardcoded too)
#  output: out.png: Image
"""

if __name__ == '__main__':
    # Read source image.
    im_src = cv2.imread('elevation1x1_new-mer-bleue.bmp')

    pts_src = np.array([[1066, 2324], [1100, 2303], [1088, 2357], [870, 2426], [879, 2189], [1028, 2058], [1192, 2218], [1395, 2196], [1346, 2005], [1806, 3234],
                        [1677, 3462], [1653, 3642], [1761, 3654], [2163, 4062], [2226, 3975], [2277, 3807], [2526, 3639], [3003, 4119], [3240, 4131], [2886, 4008], [2979, 3900]])
    print("src:", pts_src)

    # Read destination image.
    im_dst = cv2.imread('population-density-map.bmp')

    pts_dst = np.array([[818, 1196], [849, 1169], [853, 1221], [649, 1345], [585, 1134], [700, 974], [918, 1067], [1123, 995], [1020, 839], [1792, 1894],
                        [1710, 2130], [1724, 2320], [1830, 2320], [2288, 2688], [2334, 2596], [2364, 2418], [2576, 2242], [3100, 2734], [3338, 2756], [2982, 2620], [3056, 2514]])
    print("dst:", pts_dst)
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))

    # Display images
    cv2.imshow("Source Image", im_src)
    cv2.imshow("Destination Image", im_dst)
    cv2.imshow("Warped Source Image", im_out)
    cv2.imwrite("out.png", im_out)
    cv2.waitKey(0)
