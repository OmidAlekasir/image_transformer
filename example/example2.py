import cv2

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.image_transformer import ImageTransformer

"""
In this example, the image is rotating around an arbitrary origin. To do this,
the image is moved several pixels deeper into the z-axis, rotated, then
traslated to its orignal position.
The rotation is around the y-axis.
"""

if __name__ == '__main__':
    
    src = cv2.imread('../data/waterfall.jpg')
    src_resized = cv2.resize(src, (640, 480))

    height, width, _ = src_resized.shape

    T = ImageTransformer(width, height, 70)

    beta = 0
    limit = 20
    flag = 0
    while True:

        if beta <= -limit:
            flag = 1
        if beta >= limit:
            flag = 0

        if flag:
            beta +=1
        else:
            beta -=1

        # around the origin (0, 0, 0)
        T.rotate(beta = beta)
        dst1 = T.transform(src_resized)

        # around (0, 0, 200)
        T.translate(dz = 200)
        T.rotate(beta = beta)
        T.translate(dz = -200)
        dst2 = T.transform(src_resized)

        # around (0, 0, -200)
        T.translate(dz = -200)
        T.rotate(beta = beta)
        T.translate(dz = 200)
        dst3 = T.transform(src_resized)

        # show the results
        cv2.imshow('Rotation origin = (0, 0, 0)', dst1)
        cv2.imshow('Rotation origin = (0, 0, 200)', dst2)
        cv2.imshow('Rotation origin = (0, 0, -200)', dst3)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break