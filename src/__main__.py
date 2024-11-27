import utils.ui as ui
from utils.otsu import thresholding



def main():
  step = ui.init()

  if step == 0:
    ui.upload()
    
  elif step == 1:
    ui.grayscale()

  elif step == 2:
    ui.histogram()

  elif step == 3:
    ui.variance(thresholding)

  elif step == 4:
   ui.threshold(thresholding)

  elif step == 5:
    ui.save()

  ui.next(step)



if __name__ == "__main__":
  main()
