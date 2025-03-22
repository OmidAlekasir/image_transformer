import cv2

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.spherical_transformer import SphericalTransformer

"""
In this example, the image is rotating around an arbitrary origin. To do this,
the image is moved several pixels to the left, rotated, then traslated to its
orignal position.
"""

if __name__ == '__main__':
    
    src = cv2.imread('../data/waterfall.jpg')
    src_resized = cv2.resize(src, (640, 480))

    height, width, _ = src_resized.shape

    T = SphericalTransformer(width, height, 70)

    beta = 0
    while True:

        beta += 2

        T.translate(dx = width // 2)
        T.rotate(beta = beta)
        T.translate(dx = -width // 2)
        dst = T.transform(src_resized)
        
        cv2.imshow('dst', dst)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break