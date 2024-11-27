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


    pixel_counts, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    max_variance = 0
    iteration_data = []
    optimal_threshold = 0
    total_pixels = image.size

    sum_background = 0
    weight_background = 0
    weight_foreground = 0
    sum_total = np.dot(pixel_counts, bin_centers)

    binary_image = None

    for t in range(0, 256):
      weight_background += pixel_counts[t]
      weight_foreground = total_pixels - weight_background

      if weight_background == 0 or weight_foreground == 0:
        continue

      sum_background += t * pixel_counts[t]
      mean_background = sum_background / weight_background
      mean_foreground = (sum_total - sum_background) / weight_foreground

      variance_between = (
        weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
      )

      iteration_data.append((t, variance_between))

      if variance_between > max_variance:
        max_variance = variance_between
        optimal_threshold = t

    binary_image = (image >= optimal_threshold).astype(np.uint8) * 255

    return optimal_threshold, binary_image, (pixel_counts, bin_centers), iteration_data
