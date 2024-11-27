import numpy as np
from typing import Any



def thresholding(image: Any):
    """
    Perform Otsu's thresholding step-by-step on a grayscale image.
    :param image: Input grayscale image as a NumPy array.
    :return: Tuple containing:
        - Optimal threshold value
        - Binary image
        - Histogram data (pixel counts and bin centers)
        - Iteration data for visualization (thresholds, variances)
    """

    # Calculate histogram
    pixel_counts, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Normalize the histogram
    total_pixels = image.size
    histogram_normalized = pixel_counts / total_pixels
    
    # Initialize variables for finding optimal threshold
    max_between_class_variance = 0
    optimal_threshold = 0
    iteration_data = []

    # Iterate over all possible thresholds (1 to 255)
    for threshold in range(1, 256):
        # Class probabilities
        weight_0 = np.sum(histogram_normalized[:threshold])
        weight_1 = np.sum(histogram_normalized[threshold:])

        # Class means
        mean_0 = np.sum(bin_centers[:threshold] * histogram_normalized[:threshold]) / weight_0 if weight_0 > 0 else 0
        mean_1 = np.sum(bin_centers[threshold:] * histogram_normalized[threshold:]) / weight_1 if weight_1 > 0 else 0

        # Between-class variance
        between_class_variance = weight_0 * weight_1 * (mean_0 - mean_1) ** 2
        iteration_data.append((threshold, between_class_variance))
        
        # Update optimal threshold if new max variance is found
        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            optimal_threshold = threshold

    # Create binary image based on optimal threshold
    binary_image = (image >= optimal_threshold).astype(np.uint8) * 255

    return optimal_threshold, binary_image, (pixel_counts, bin_centers), iteration_data
