"""
bgr2grey.py

This module contains a function for converting an RGB image to grayscale using the formula Y = 0.299R + 0.587G + 0.114B.

Functions:
- rgb_to_gray: Converts an RGB image to grayscale.

Usage example:
    import cv2
    from bgr2grey import rgb_to_gray

    # Load an RGB image
    image = cv2.imread('path/to/your/image.jpg')

    # Convert the image to grayscale
    gray_image = rgb_to_gray(image)

    # Display the original and grayscale images
    cv2.imshow('Original Image', image)
    cv2.imshow('Grayscale Image', gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""
import numpy as np


def rgb_to_gray(rgb_image):
    """
    Converts an RGB image to grayscale using the formula Y = 0.299R + 0.587G + 0.114B.

    Args:
        rgb_image (numpy.ndarray): The input RGB image.

    Returns:
        numpy.ndarray: The grayscale image.
    """
    height, width, _ = rgb_image.shape
    gray_image = np.empty((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            r, g, b = rgb_image[i, j]
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_image[i, j] = gray_value

    return gray_image
