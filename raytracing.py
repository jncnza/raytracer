# Import 3rd party libraries
import numpy as np


class Vector():
    """A three element vector used in 3D graphics"""

    def __init__(self, xyz=[0.0, 0.0, 0.0]):
        self.xyz = np.array(xyz)
        self.x, self.y, self.z = xyz

    def __add__(self, other):
        try:
            return Vector(self.xyz + other.xyz)
        except:
            return NotImplemented

    def __sub__(self, other):
        try:
            return Vector(self.xyz - other.xyz)
        except:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.xyz * other.xyz)
        elif isinstance(other, (int, float)):
            return Vector(self.xyz * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, scalar):
        return Vector(self.xyz / scalar)

    def __getitem__(self, index):
        return self.xyz[index]

    def __len__(self):
        return len(self.xyz)

    def __matmul__(self, other):
        return np.dot(self.xyz, other.xyz)

    def __str__(self):
        return str(self.xyz)

    def __repr__(self):
        return f'Vector([{self.x}, {self.y}, {self.z}])'

    def dot(self, other):
        return np.dot(self.xyz, other.xyz)

    def cross(self, other):
        return Vector(np.cross(self.xyz, other.xyz))

    def norm(self):
        return np.linalg.norm(self.xyz)

    def squared_norm(self):
        return np.dot(self.xyz, self.xyz)

    def normalize(self):
        return self / self.norm()


class Point(Vector):
    """An alias for Vector"""

    def __init__(self, xyz=[0.0, 0.0, 0.0]):
        super().__init__(xyz)

    def __repr__(self):
        return f'Point([{self.x}, {self.y}, {self.z}])'


class Ray():
    """Simple ray class"""

    def __init__(self, origin, direction):
        # Ideally, origin is an instance of Point and direction is Vector
        self.origin = origin
        self.direction = direction

    def point_at(self, t):
        return Point(self.origin + t*self.direction)

    def bg_color(self):
        t = self.direction.normalize().y
        return t*WHITE + (1-t)*Color([0.5, 0.7, 1.0])

    @classmethod
    def from_points(cls, tail, head):
        return cls(tail, head - tail)


class Sphere():
    """A sphere is the only implemented 3D shape. Has center, radius and material"""

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        # Auxiliary vector for cleaner code
        center_to_origin = ray.origin - self.center

        # Find the coefficients for the quadratic equation
        a = ray.direction.squared_norm()
        b = 2 * center_to_origin @ ray.direction
        c = center_to_origin.squared_norm() - self.radius**2
        # Find the discriminant
        d = b**2 - 4*a*c

        if d >= 0 and (t := (-b - d**0.5) / (2*a)) >= 0:
            return t
        else:
            return None


class Color():
    """Simple color class"""

    def __init__(self, rgb=[0.0, 0.0, 0.0]):
        self.rgb = np.array(rgb)
        self.r, self.g, self.b = rgb

    def __add__(self, other):
        try:
            return Color(self.rgb + other.rgb)
        except:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Color(self.rgb * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return str(self.rgb)

    def __repr__(self):
        return f'Color([{self.r}, {self.g}, {self.b}])'

    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        r = int(hexcolor[1:3], 16) / 255
        g = int(hexcolor[3:5], 16) / 255
        b = int(hexcolor[5:7], 16) / 255

        return cls([r, g, b])


class Scene():
    """Renders 3D scene into a 2D scene using ray tracing"""

    def __init__(self, camera, objects, width, height):
        self.camera = camera
        self.objects = objects
        self.width = width
        self.height = height

    def render(self):
        aspect_ratio = self.width / self.height

        x0, x1 = -1, +1
        x_step = (x1-x0) / (self.width-1)

        y0, y1 = -1/aspect_ratio, +1/aspect_ratio
        y_step = (y1-y0) / (self.height-1)

        image = Image(self.width, self.height)

        for j in range(self.height):
            y = y0 + j*y_step
            for i in range(self.width):
                x = x0 + i*x_step
                ray = Ray.from_points(self.camera, Point([x, y, 0]))
                image.set_pixel(i, j, self.trace(ray))

        return image

    def trace(self, ray):
        # Find the nearest object hit by the ray in the scene
        point_hit, object_hit = self.find_nearest(ray)
        color = self.color_at(ray, point_hit, object_hit) if object_hit else ray.bg_color()

        return color

    def find_nearest(self, ray):
        dist_min, object_hit = None, None

        for _object in self.objects:
            dist = _object.intersect(ray)
            if dist is not None and (object_hit is None or dist < dist_min):
                dist_min, object_hit = dist, _object

        point_hit = ray.point_at(dist_min) if object_hit else None

        return point_hit, object_hit

    def color_at(self, ray, point_hit, object_hit):
        return object_hit.material


class Image():
    """Simple image class"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for x in range(width)] for y in range(height)]

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, ppm_file_path):
        # Define auxiliary function
        def to_byte(color):
            """Converts floats between 0 and 1 into ints between 0 and 255"""
            return [int(max(min(round(val * 255), 255), 0)) for val in color.rgb]

        if ppm_file_path.endswith('.ppm'):
            with open(ppm_file_path, 'w') as ppm_file:
                # Write the header
                ppm_file.write(f'P3 {self.width} {self.height}\n255\n')
                # Write the image pixels
                for row in self.pixels:
                    for color in row:
                        r, g, b = to_byte(color)
                        ppm_file.write(f'{r:3} {g:3} {b:3}\t')
                    ppm_file.write('\n')
        else:
            raise SyntaxError('Image must be a ppm file.')


# Define some constants
RED = Color.from_hex('#FF0000')
GREEN = Color.from_hex('#00FF00')
BLUE = Color.from_hex('#0000FF')
BLACK = Color.from_hex('#000000')
WHITE = Color.from_hex('#FFFFFF')
