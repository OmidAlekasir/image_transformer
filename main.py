import cv2
from spherical_transformer import SphericalTransformer

if __name__ == '__main__':
    
    src = cv2.imread('src/src.jpg')
    src = cv2.resize(src, (640, 480))

    height, width, _ = src.shape

    T = SphericalTransformer(width, height, 70)
    
    # H = transformer.transform(alpha = 0, beta = 0, gamma = 0)
    # dst = cv2.warpPerspective(src, H, (width, height))

    beta = 0

    while 1:
        beta += 1

        T.rotate(beta = beta)

        H = T.get_homography()
        dst = cv2.warpPerspective(src, H, (width, height))
        
        cv2.imshow('dst', dst)

        if cv2.waitKey(10) == 'q':
            break