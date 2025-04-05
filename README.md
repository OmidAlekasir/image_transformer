# image_transformer
**The `img3d` library unlocks infinite possibilities.**

* In the following example, the image rotates around the points $(0, 0, 300)$ and $(0, 0, -300)$ in a 3-dimensional Cartesian space. Can you spot the difference?

![Alt Text](src/beta.gif)

* This example demonstrates that the rotation center plays a critical role.

![Alt Text](src/gamma.gif)
## Abstract
This repository provides a tool for 3D image transformations, including rotations and translations in 3D Cartesian coordinates. The transformations are implemented in 3D space using the sequential logic of the main class.

The primary concept of this library originates from the work of **Hou-Ning Hu**, whose GitHub repository can be found [here](https://github.com/eborboihuc/rotate_3d). In addition to fixing existing bugs, the logic for utilizing this `ImageTransformer` has been modified to a sequential logic to accommodate all use cases.

This repository is linked to the PyPI library `img3d`, which can be installed using the following command:
```
pip install img3d
```

## Introduction
Image transformation is a critical component of image processing, particularly for data fusion in real-time applications. This class enables users to perform 3D rotations and translations on images in any desired spatial configuration.

The library's primary output is a $3\times3$ homography matrix, which can be directly integrated with perspective-warping functions in image processing libraries such as **OpenCV**, **VPI**, or other compatible frameworks. By default, the `ImageTransformer` leverages **OpenCV** (if installed) for efficient implementation.

## Description
The `img3d` library treats the image center as the origin of the coordinate system during transformations. Each pixel in the image data is represented as:

$$
f =
\begin{bmatrix}
x \\
y \\
1 \\
\end{bmatrix}
$$

where $x$ and $y$ are the pixel coordinates respectively.

The translation matrix is defined as:

$$
T(dx, dy, dz) =
\begin{bmatrix}
1 & 0 & 0 & dx \\
0 & 1 & 0 & dy \\
0 & 0 & 1 & dz \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

The rotation matrices are defined as:

$$
R_x(\alpha) =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & cos(\alpha) & -sin(\alpha) & 0 \\
0 & sin(\alpha) & cos(\alpha) & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

$$
R_y(\beta) =
\begin{bmatrix}
cos(\beta) & 0 & -sin(\beta) & 0 \\
0 & 1 & 0 & 0 \\
sin(\beta) & 0 & cos(\beta) & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

$$
R_z(\gamma) =
\begin{bmatrix}
cos(\gamma) & -sin(\gamma) & 0 & 0 \\
sin(\gamma) & cos(\gamma) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
\end{bmatrix}
$$

Given that most image processing frameworks (e.g., OpenCV) define the origin of coordinates at the upper-left corner, it is essential to translate the image center to this reference point. This adjustment ensures proper rotational transformations, as the image center serves as the logical origin in real-world applications. After the desired rotation ($R_{4\times4}$) and translation ($T_{4\times4}$) matrices are applied by the user, the image center is restored to its original position.

The algorithm of 3D image transformation in this class is as below:

**Step 1**: 2D to 3D projection ($A_1$)

The first step is to bring the image into a 3D space, using the following 2D to 3D projection matrix:

$$
A_1 =
\begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1 \\
0 & 0 & 1 \\
\end{bmatrix}
$$

**Step 2**: Center to origin ($T_c$)

Translate the image using $T(\frac{-W}{2}, \frac{-H}{2}, 0)$, where $W$ nad $H$ are the width and height of the image, respectively. This positions the image center at the origin.

**Step 3**: Desired transformation ($M$)

This step represents the primary usage of the library, meaning that all rotations and transformations occur at this level. All other steps operate behind the scenes, while this step is explicitly controlled by the user.

**Step 4**: Move to the focal point ($T_f$)

In this step, the image is positioned at the focal point of the image. For more information on the details of the current and next step, please refer to this [link](https://stackoverflow.com/questions/17087446/how-to-calculate-perspective-transform-for-opencv-from-rotation-angles).

**Step 5**: 3D to 2D projection ($A_2$)

The following matrix moves the image to the origin and from 3D to 2D coordinates, forming the final $3\times3$ homography matrix.

$$
A_2 =
\begin{bmatrix}
f & 0 & \frac{W}{2} & 0 \\
0 & f & \frac{H}{2} & 0 \\
0 & 0 & 1 & 0 \\
\end{bmatrix}
$$

By going through these steps, the final homography matrix is formed, using the following matrix multiplication.

$$
H=A_2 \, T_f \, M \, T_c \, A_1
$$

Then, the homography matrix $H$ is applied to the image, using the following formula (using OpenCV or VPI):

$$
f_{new}=Hf
$$

Note that in case that $M=I_{4\times4}$, the image stays intact.

## Example
In this section, brief examples are explained. For more examples, please refer to the **example** folder in this repository.

Firstly, import the necessary libraries, create an instance of the `ImageTransformer` class, and import an image.

**Note that after calling the `transform` or `get_homography` functions, the class's homography matrix is reset to an identity matrix.**

```
from img3d import ImageTransformer
import cv2

# import an image
src = cv2.imread('image.jpg')
height, width, _ = src.shape

# define an instance of the ImageTransformer class
fov_vertical = 70 # vertical field of view of the camera
T = ImageTransformer(width, height, fov_vertical)
```

### Example I:
```
T.rotate(alpha = 20, beta = 30, gamma = 10)
dst = T.transform(src)
```

### Example II:
```
T.translate(dx = 640//2, dy = 480//2)
T.rotate(gamma = 149)

H = T.get_homography()
dst = cv2.warpPerspective(frame, H, (width, height))
```