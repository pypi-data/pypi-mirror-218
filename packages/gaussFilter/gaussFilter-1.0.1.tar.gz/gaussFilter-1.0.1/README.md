# gaussFilter

gaussFilter is a Python package that provides a function for applying a Gaussian filter to images using OpenCV.

## Installation

You can install `gaussFilter` using pip:

```bash
pip install gaussFilter
```


## Usage

```python
import cv2
from gaussFilter import apply_gaussian_filter

# Load an image
image = cv2.imread('path/to/your/image.jpg')

# Apply the Gaussian filter with desired sigma and kernel size
filtered_image = apply_gaussian_filter(image, sigma=1.5, kernel_size=5)

# Display the original and filtered images
cv2.imshow('Original Image', image)
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

##Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This package is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.