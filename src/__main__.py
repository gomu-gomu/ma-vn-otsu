import numpy as np
import utils.ui as ui
import streamlit as st



def otsu_thresholding_steps(image):
    """
    Perform Otsu's thresholding step-by-step on a grayscale image.
    :param image: Input grayscale image as a NumPy array.
    :return: Tuple containing:
        - Optimal threshold value
        - Binary image
        - Histogram data (pixel counts and bin centers)
        - Iteration data for visualization (thresholds, variances)
    """
    # Flatten the image into a 1D array for histogram calculation
    pixel_counts, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Total number of pixels
    total_pixels = image.size

    # Initialize variables for Otsu's method
    max_variance = 0
    optimal_threshold = 0
    iteration_data = []

    sum_total = np.dot(pixel_counts, bin_centers)  # Sum of all pixel intensities
    sum_background = 0
    weight_background = 0
    weight_foreground = 0

    binary_image = None

    # Iterate through all possible thresholds
    for t in range(256):
        weight_background += pixel_counts[t]
        weight_foreground = total_pixels - weight_background

        if weight_background == 0 or weight_foreground == 0:
            continue

        sum_background += t * pixel_counts[t]
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground

        # Calculate inter-class variance
        variance_between = (
            weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
        )

        # Store iteration data for visualization
        iteration_data.append((t, variance_between))

        # Check if the current threshold maximizes the variance
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_threshold = t

    # Apply the optimal threshold to create the binary image
    binary_image = (image >= optimal_threshold).astype(np.uint8) * 255

    return optimal_threshold, binary_image, (pixel_counts, bin_centers), iteration_data



def main():
  step = ui.init()

  if step == 0:
    ui.upload()
    
  elif step == 1:
    ui.grayscale()

  elif step == 2:
    ui.histogram()

  elif step == 3:
    ui.variance(otsu_thresholding_steps)

  elif step == 4:
   ui.threshold(otsu_thresholding_steps)

  elif step == 5:
    ui.save()

  ui.next(step)



if __name__ == "__main__":
  main()
