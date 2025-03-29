import numpy as np

class ImageTransformer():
    """ Perspective Transformation"""

    def __init__(self, width, height, fov_vertical = 70):
        self.width = width
        self.height = height
        self.d = np.sqrt(self.width**2 + self.height**2)
        self.fov = np.deg2rad(fov_vertical)
        self.f = self.d / (2 * np.sin(self.fov))

        self._cv2 = None

        self.__reset()
        
    def __reset(self):
        # Projection 2D -> 3D matrix
        self.H = np.array([ [1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1],
                            [0, 0, 1]])
        
        # Translate the center to the center of the image
        self.translate(dx = -self.width // 2, dy = -self.height // 2)
        
    def rotate(self, alpha = 0, beta = 0, gamma = 0):
        # degree to radian
        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)

        # Rotation matrices around the X, Y, and Z axis
        RX = np.array([ [1, 0, 0, 0],
                        [0, np.cos(alpha), -np.sin(alpha), 0],
                        [0, np.sin(alpha), np.cos(alpha), 0],
                        [0, 0, 0, 1]])
        
        RY = np.array([ [np.cos(beta), 0, -np.sin(beta), 0],
                        [0, 1, 0, 0],
                        [np.sin(beta), 0, np.cos(beta), 0],
                        [0, 0, 0, 1]])
        
        RZ = np.array([ [np.cos(gamma), -np.sin(gamma), 0, 0],
                        [np.sin(gamma), np.cos(gamma), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        
        # Composed rotation matrix with (RX, RY, RZ)
        R = RZ @ RY @ RX

        self.H = R @ self.H

        return self
    
    def translate(self, dx = 0, dy = 0, dz = 0):
        T = np.array([  [1, 0, 0, dx],
                        [0, 1, 0, dy],
                        [0, 0, 1, dz],
                        [0, 0, 0, 1]])
        
        self.H = T @ self.H

        return self
    
    def zoom(self, zoom = 1):
        T = np.array([  [zoom, 0, 0, 0],
                        [0, zoom, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        
        self.H = T @ self.H

        return self
    
    def get_homography(self):
        
        # reset the image coordinates to the top-left corner
        self.translate(dz = self.f)

        # Projection 3D -> 2D matrix
        A2 = np.array([ [self.f, 0, self.width/2, 0],
                        [0, self.f, self.height/2, 0],
                        [0, 0, 1, 0]])
        
        self.H = A2 @ self.H

        H_final = (self.H).astype(float)

        self.__reset()
        
        return H_final

    def transform(self, frame):
        if self._cv2 is None:
            self.__import_cv2()
        
        H = self.get_homography()
        dst = self._cv2.warpPerspective(frame, H, (self.width, self.height))

        return dst

    def __import_cv2(self):
        try:
            import cv2
            self._cv2 = cv2
        except ImportError:
            raise RuntimeError(
                "OpenCV not installed. Install with: pip install opencv-python"
            )