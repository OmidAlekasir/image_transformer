import cv2
from spherical_homography import ImageTransformer

if __name__ == '__main__':
    
    src = cv2.imread('src/src.jpg')
    src = cv2.resize(src, (640, 480))

    height, width, _ = src.shape

    transformer = ImageTransformer(width, height, 70)
    H = transformer.transform(alpha = 0, beta = 0, gamma = 0)
    dst = cv2.warpPerspective(src, H, (width, height))

    cv2.imshow('src', src)
    cv2.imshow('dst', dst)

    cv2.waitKey(10000000)