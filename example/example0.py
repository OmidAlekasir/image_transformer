from img3d import ImageTransformer
import cv2

"""
In this example, the image is simply rotating around the origin.
"""

if __name__ == '__main__':
    
    src = cv2.imread('../data/waterfall.jpg')
    src_resized = cv2.resize(src, (640, 480))

    height, width, _ = src_resized.shape

    T = ImageTransformer(width, height, 70)

    alpha = 0
    beta = 0
    while True:

        alpha += 1
        beta += 2

        T.rotate(alpha = alpha, beta = beta)
        dst = T.transform(src_resized)
        
        cv2.imshow('dst', dst)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break