import numpy as np

class ImageTransformer(object):
    """ Perspective transformation class for image
        with shape (height, width, #channels) """

    def __init__(self, width, height, fov_vertical = 70):
        self.width = width
        self.height = height
        self.d = np.sqrt(self.width**2 + self.height**2)
        self.fov = np.deg2rad(fov_vertical)
        self.f = self.d / (2 * np.sin(self.fov))

    def transform(self, alpha=0, beta=0, gamma=0, dx=0, dy=0, dz=0, zoom = 1):

        alpha = np.deg2rad(alpha)
        beta = np.deg2rad(beta)
        gamma = np.deg2rad(gamma)

        # Translation matrix
        # virtual distance of the camera to the image (in pixels)
        dz = self.height / (2 * np.tan(self.fov / 2))
        T = np.array([  [zoom, 0, 0, dx],
                        [0, zoom, 0, dy],
                        [0, 0, 1, dz],
                        [0, 0, 0, 1]])

        # Projection 2D -> 3D matrix
        A1 = np.array([ [1, 0, -self.width/2],
                        [0, 1, -self.height/2],
                        [0, 0, 1],
                        [0, 0, 1]])
        
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
        
        Ti = np.array([  [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, self.f - dz],
                        [0, 0, 0, 1]])

        # Composed rotation matrix with (RX, RY, RZ)
        R = RZ @ RY @ RX

        # Projection 3D -> 2D matrix
        A2 = np.array([ [self.f, 0, self.width/2, 0],
                        [0, self.f, self.height/2, 0],
                        [0, 0, 1, 0]])

        # Final transformation matrix
        return A2 @ Ti @ R @ T @ A1