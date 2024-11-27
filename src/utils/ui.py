import io
import os

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from skimage.color import rgb2gray
from skimage.io import imread, imsave



def init():
  """
    Initializes the page
  """
  if "step" not in st.session_state:
    st.session_state.step = 0

  st.set_page_config(page_title="Algorithme d'Otsu", page_icon="📷")

  st.title("Algorithme d'Otsu")
  st.markdown("""Ce démo montre comment appliquer l'algorithme de seuillage d'Otsu étape par étape.""")

  return st.session_state.get("step", 0)


def next(step: int):
  """
    The next button step.

    :param step: The step to set
  """
  st.button("Étape suivante", disabled=step == 5, on_click=lambda: set_step(step + 1))



def set_step(step: int):
  """
    Changes the active step

    :param step: The step to set
  """
  st.session_state.step = step



def upload():
  """
    The upload step.
    Uploads an image for processing.
  """
  st.subheader("Étape 1 : Télécharger une image")

  uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "png", "jpeg"])
  if uploaded_file:
    image = imread(io.BytesIO(uploaded_file.read()))

    st.session_state["image"] = image
    st.image(st.session_state["image"], caption="Image téléchargée", use_container_width=True)



def grayscale():
  """
    The grayscale conversion step.
    Converts the uploaded image to grayscale.
  """
  st.subheader("Étape 2 : Conversion en niveaux de gris")
  
  if "image" in st.session_state:
    image = st.session_state["image"]

    if len(image.shape) == 3:
      grayscale_image = rgb2gray(image)
      grayscale_image = (grayscale_image * 255).astype(np.uint8)
    else:
      grayscale_image = image

    st.session_state["image"] = grayscale_image
    st.image(grayscale_image, caption="Image en niveaux de gris", use_container_width=True)
  else:
    st.warning("Veuillez d'abord télécharger une image.")



def histogram():
  """
    The histogram step.
    Visualizes the data on a histogram.
  """
  st.subheader("Étape 3 : Afficher l'histogramme")

  if "image" in st.session_state:
    image = st.session_state["image"]
    pixel_counts, bin_centers = np.histogram(image, bins=256, range=(0, 256))
    
    fig, ax = plt.subplots()
    ax.bar(bin_centers[:-1], pixel_counts, width=1, color="gray")
    ax.set_title("Histogramme des intensités de pixels")
    ax.set_xlabel("Intensité")
    ax.set_ylabel("Nombre de pixels")

    st.pyplot(fig)
  else:
    st.warning("Veuillez d'abord télécharger une image.")



def variance(threshold_fn):
  """
    The variance step.
    Visualizes the data on a histogram.

    :param threshold_fn: The thresholding function
  """
  st.subheader("Étape 4 : Calcul de la variance inter-classes")
  
  if "image" in st.session_state:
    image = st.session_state["image"]
    _, _, _, iteration_data = threshold_fn(image)
    thresholds, variances = zip(*iteration_data)
    
    fig, ax = plt.subplots()
    ax.plot(thresholds, variances, color="red")
    ax.set_title("Variance inter-classes par seuil")
    ax.set_xlabel("Seuil")
    ax.set_ylabel("Variance inter-classes")

    st.pyplot(fig)
  else:
    st.warning("Veuillez d'abord télécharger une image.")



def threshold(threshold_fn):
  """
    The thresholding step.
    Applies the optimal threshold.

    :param threshold_fn: The thresholding function
  """
  st.subheader("Étape 5 : Appliquer le seuil optimal")

  if "image" in st.session_state:
    image = st.session_state["image"]
    threshold, binary_image, _, _ = threshold_fn(image)

    st.session_state["binary_image"] = binary_image
    st.write(f"Seuil optimal : {threshold}")
    st.image(binary_image, caption="Image binaire", use_container_width=True)
  else:
    st.warning("Veuillez d'abord télécharger une image.")



def save():
  """
    The save step.
    Saves the binary image.
  """
  st.subheader("étape 6 : sauvegarder l'image")
  
  if "binary_image" in st.session_state:
    output_path = os.path.join("assets", "result.jpg")
    imsave(output_path, st.session_state["binary_image"])

    st.success(f"l'image binaire a été sauvegardée sous le nom : {output_path}")
  else:
    st.warning("Veuillez appliquer le seuil avant de sauvegarder l'image.")
