import logging
import argparse
import numpy as np

from typing import Any
from skimage import io, color
from utils.otsu import thresholding


def init():
  """
    Initializes the logger
  """

  console = logging.StreamHandler()
  console.setLevel(logging.INFO)

  logging.basicConfig(filename='assets/result.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  logging.getLogger().addHandler(console)



def args():
  """
    Parses the command line arguments
  """
  parser = argparse.ArgumentParser(description="Testez l'implémentation du seuillage d'Otsu.")
  parser.add_argument('input', type=str, help='Chemin d\'accès à l\'image d\'entrée')
  
  return parser.parse_args()



def load(input: str):
  """
    Loads the image from the given path

    :param input: The path to the image

    :return: The loaded image
  """
  logging.info(f"Chargement de l'image à partir du chemin : {input}")

  image = io.imread(input)
  if len(image.shape) == 3:
    logging.info("Conversion d'image en niveaux de gris.")

    image = color.rgb2gray(image)
    image = (image * 255).astype(np.uint8)
  
  return image



def process(image: Any):
  """
    Performs Otsu's thresholding on the given image

    :param image: The image to process

    :return: The optimal threshold, the binary image and the iteration data
  """

  logging.info("Effectuer le seuillage d'Otsu.")
  optimal_threshold, binary_image, (pixel_counts, bin_centers), iteration_data = thresholding(image)
  
  logging.info(f"Seuil optimal trouvé : {optimal_threshold}")
  logging.info(f"Centres des bacs d'histogramme : {bin_centers[:10]}...")
  logging.info(f"Nombre d'itérations : {len(iteration_data)}")

  return optimal_threshold, binary_image, iteration_data



def save(image: Any):
  """
    Saves the processed image to the result file

    :param image: The processed image
  """

  result_image_path = 'assets/result.jpg'
  logging.info(f"Saving resulting binary image to: {result_image_path}")
  
  io.imsave(result_image_path, image)



def summary(threshold: int, data: list[Any]):
  """
    Prints a summary of the processed image

    :param threshold: The optimal threshold
    :param data: The iteration data
  """

  logging.info("Résumé :")
  logging.info(f"Seuil optimal : {threshold}")
  logging.info(f"Itérations totales : {len(data)}")
