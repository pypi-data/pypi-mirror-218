# bgr2grey

bgr2grey is a Python package that provides a function for converting RGB images to grayscale.

## Installation

You can install `bgr2grey` using pip:

```bash
pip install bgr2grey
```
## Usage

```bash
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

```

## License

This package is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.