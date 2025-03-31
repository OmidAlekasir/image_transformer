# spherical_image_transformer
## Abstract
This repository provides a tool for 3D image transformations, including rotations and translations in 3D Cartesian coordinates. The transformations operate in 3D space using sequential logic of the main class.

This repository is associated with a PyPI library `img3d` which can be installed through the following command:
```
pip install img3d
```

## Description
Image transformation is an integral part of image processing, particularly for data fusion in real-time applications. This class enables users to rotate and translate images in 3D space in any desired configuration.

The main output of this library is a 3 by 3 homography matrix that can be used with warp-perspective transformers in image processing libraries, such as `OpenCV`, `VPI`, etc. The default transformation in this library is done using `OpenCV`.