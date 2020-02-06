# Import local libraries
import raytracing as rt

# Define some constants
WIDTH = 320
HEIGHT = 200


def main():
    # Setup everything
    camera = rt.Point([0, 0, -1])
    objects = [rt.Sphere(rt.Point(), 0.3, rt.RED)]
    scene = rt.Scene(camera, objects, WIDTH, HEIGHT)
    image = scene.render()

    # Write the image to a ppm file
    image.write_ppm('sphere_image.ppm')


if __name__ == '__main__':
    main()
