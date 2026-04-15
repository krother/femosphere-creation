"""
Draw a femosphere planet
"""
import numpy as np
from PIL import Image
from noise import pnoise2

# Image settings
width, height = 1024, 1024
planet_radius = 500

BACKGROUND_COLOR = 255, 0, 255
RED = 255, 92, 0


def get_perlin_array(height, width, octaves, scale, x_offset=42, y_offset=42):
    y, x = np.mgrid[0:height, 0:width]
    x += x_offset
    y += y_offset

    coords = np.stack([y, x], axis=-1)
    perlin = np.vectorize(
        lambda y, x: pnoise2(x / scale, y / scale, octaves=octaves)
    )
    noise = perlin(coords[..., 0], coords[..., 1])
    return ((noise - noise.min()) * 255 / (noise.max() - noise.min())).astype(np.uint8)


planet = np.zeros((height, width, 3), dtype=np.uint8)
planet[:, :] = BACKGROUND_COLOR

# make landscapes
mask = get_perlin_array(height, width, octaves=5, scale=100)
planet[mask > 160] = RED

# apply circular mask
# y, x = np.mgrid[0:height, 0:width]
# y -= height // 2
# x -= width // 2
# r = y ** 2 + x ** 2
# circle_mask = r < planet_radius ** 2
# planet[circle_mask] = 0

# save the planet
img = Image.fromarray(planet)
img.save('planet.png')
img.show()
