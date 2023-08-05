"""
gaussFilter.py

This module contains a function for applying a Gaussian filter to an image using OpenCV.

Functions:
- apply_gaussian_filter: Applies a Gaussian filter to an image.
"""

import cv2
import numpy as np


def apply_gaussian_filter(image, sigma, kernel_size):
    """
    Applies a Gaussian filter to an image.

    Args:
        image (numpy.ndarray): The input image.
        sigma (float): The standard deviation of the Gaussian kernel.
        kernel_size (int): The size of the kernel (should be an odd integer).

    Returns:
        numpy.ndarray: The filtered image.
    """
    size = kernel_size
    channels = cv2.split(image)
    filtered_channels = []

    for channel in channels:
        kernel = np.zeros((size, size))
        center = size // 2

        for i in range(size):
            for j in range(size):
                x = i - center
                y = j - center
                kernel[i, j] = (1 / (2 * np.pi * sigma ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))

        kernel /= np.sum(kernel)
        padded_channel = np.pad(channel, ((center, center), (center, center)), mode='constant')
        filtered_channel = np.zeros_like(channel)

        for i in range(channel.shape[0]):
            for j in range(channel.shape[1]):
                filtered_channel[i, j] = np.sum(padded_channel[i:i + size, j:j + size] * kernel)

        filtered_channels.append(filtered_channel)

    filtered_image = cv2.merge(filtered_channels)

    return filtered_image.astype(image.dtype)
