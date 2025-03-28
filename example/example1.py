import cv2

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.spherical_transformer import SphericalTransformer

"""
In this example, the image is rotating around an arbitrary origin. To do this,
the image is moved several pixels to the upper-left corner, rotated, then
traslated to its orignal position.
The rotation is around the z-axis.
"""

if __name__ == '__main__':
    
    src = cv2.imread('../data/waterfall.jpg')
    src_resized = cv2.resize(src, (640, 480))

    height, width, _ = src_resized.shape

    T = SphericalTransformer(width, height, 70)

    gamma = 0
    limit = 20
    flag = 0
    while True:

        if gamma <= -limit:
            flag = 1
        if gamma >= limit:
            flag = 0

        if flag:
            gamma +=1
        else:
            gamma -=1

        # around the origin (0, 0, 0)
        T.rotate(gamma = gamma)
        dst1 = T.transform(src_resized)

        # around (0, 0, 200)
        T.translate(dx = 640//2, dy = 480//2)
        T.rotate(gamma = gamma)
        T.translate(dx = -640//2, dy = -480//2)
        dst2 = T.transform(src_resized)

        # show the results
        cv2.imshow('Rotation origin = (0, 0, 0)', dst1)
        cv2.imshow('Rotation origin = (0, 0, 200)', dst2)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break