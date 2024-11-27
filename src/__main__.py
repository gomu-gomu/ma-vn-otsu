import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave


def otsu_thresholding(image):
    """
    Perform Otsu's thresholding on a grayscale image.
    :param image: Input grayscale image as a NumPy array.
    :return: Tuple containing the threshold value and the binary image.
    """
    # Flatten the image into a 1D array for histogram calculation
    pixel_counts, bin_edges = np.histogram(image, bins=256, range=(0, 256))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Total number of pixels
    total_pixels = image.size

    # Initialize variables for Otsu's method
    max_variance = 0
    optimal_threshold = 0

    sum_total = np.dot(pixel_counts, bin_centers)  # Sum of all pixel intensities
    sum_background = 0
    weight_background = 0
    weight_foreground = 0

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

        # Check if the current threshold maximizes the variance
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_threshold = t

    # Apply the optimal threshold to create the binary image
    binary_image = (image >= optimal_threshold).astype(np.uint8) * 255

    return optimal_threshold, binary_image


def main():
    # Path to the fingerprint image
    image_path = os.path.join("assets", "finger_print.jpg")
    output_path = os.path.join("assets", "finger_print_binary.jpg")

    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    # Load the image using matplotlib's imread and convert to grayscale (if not already)
    image = imread(image_path, as_gray=True)

    # Normalize the image to range [0, 255]
    image = (image * 255).astype(np.uint8)

    # Perform Otsu's thresholding
    threshold, binary_image = otsu_thresholding(image)

    # Display the original and thresholded images
    plt.figure(figsize=(10, 5))

    # Original image
    plt.subplot(1, 2, 1)
    plt.title("Original Grayscale Image")
    plt.axis("off")
    plt.imshow(image, cmap="gray")

    # Binary image
    plt.subplot(1, 2, 2)
    plt.title(f"Binary Image (Threshold = {threshold})")
    plt.axis("off")
    plt.imshow(binary_image, cmap="gray")

    # Show the plot
    plt.tight_layout()
    plt.show()

    imsave(output_path, binary_image.astype(np.uint8))
    print(f"Binary image saved to '{output_path}'")

if __name__ == "__main__":
    main()
