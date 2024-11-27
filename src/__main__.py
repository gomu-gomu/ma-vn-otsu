import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import os
import io


def otsu_thresholding(image):
    """
    Perform Otsu's thresholding on a grayscale image.
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
    st.title("Algorithme d'Otsu")
    st.markdown("""Cette application vous permet de traiter une image en utilisant le seuillage d'Otsu. 
      Téléchargez une image en niveaux de gris, affichez l'histogramme et le processus d'itération, et voyez le résultat seuillé.""")

    uploaded_file = st.file_uploader("Télécharger une image en niveaux de gris", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = imread(io.BytesIO(uploaded_file.read()))
        if len(image.shape) == 3:
            image = rgb2gray(image)

        image = (image * 255).astype(np.uint8)

        # Display the original image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Process Image"):
            # Perform Otsu's thresholding
            threshold, binary_image, histogram_data, iteration_data = otsu_thresholding(image)

            # Display the histogram with iteration steps
            pixel_counts, bin_centers = histogram_data
            thresholds, variances = zip(*iteration_data)

            st.subheader("Histogram and Iteration Process")
            fig, ax1 = plt.subplots()

            # Plot histogram
            ax1.bar(bin_centers, pixel_counts, width=1, color="gray", alpha=0.7, label="Histogram")
            ax1.set_xlabel("Pixel Intensity")
            ax1.set_ylabel("Frequency")
            ax1.legend(loc="upper left")

            # Plot variance vs. thresholds
            ax2 = ax1.twinx()
            ax2.plot(thresholds, variances, color="red", label="Variance")
            ax2.axvline(threshold, color="blue", linestyle="--", label=f"Threshold = {threshold}")
            ax2.set_ylabel("Variance")
            ax2.legend(loc="upper right")

            st.pyplot(fig)

            # Display the thresholded image
            st.subheader("Thresholded Image")
            st.image(binary_image, caption="Binary Image", use_container_width=True)

            # Save the binary image
            output_path = os.path.join("assets", "finger_print_binary.jpg")
            imsave(output_path, binary_image.astype(np.uint8))
            st.success(f"Binary image saved to '{output_path}'")

if __name__ == "__main__":
  main()
