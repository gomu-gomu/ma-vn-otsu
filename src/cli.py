import utils.cli as cli



def main(input: str):
  image = cli.load(input)
  threshold, image, data = cli.process(image)
  
  cli.save(image)
  cli.summary(threshold, data)



if __name__ == "__main__":
  cli.init()
  args = cli.args()
  
  main(args.input)
