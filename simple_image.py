# Import local libraries
import raytracing as rt

# Define some constants
WIDTH = 3
HEIGHT = 2

# Define basic colors
RED = rt.Color([1, 0, 0])
GREEN = rt.Color([0, 1, 0])
BLUE = rt.Color([0, 0, 1])


def main():
  """Creates a simple ppm image"""

  image = rt.Image(WIDTH, HEIGHT)

  # First row
  image.set_pixel(0, 0, RED)
  image.set_pixel(1, 0, GREEN)
  image.set_pixel(2, 0, BLUE)
  # Second row
  image.set_pixel(0, 1, RED + GREEN)
  image.set_pixel(1, 1, RED + GREEN + BLUE)
  image.set_pixel(2, 1, RED * 0.001)

  # Write the image
  image.write_ppm('simple_image.ppm')


if __name__ == '__main__':
  main()
