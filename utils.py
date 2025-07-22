import pygame
import os
import random
from gameobject import ImageObject
import constants

def spawn_random_props(area_name, count, group, prop_size=(64, 64)):
    folder_path = f"assets/props/{area_name}"
    image_files = [
        f for f in os.listdir(folder_path)
        if f.endswith(".png") or f.endswith(".jpg")
    ]

    if not image_files:
        raise FileNotFoundError(f"No image files found in {folder_path}")

    for _ in range(count):
        chosen = random.choice(image_files)
        full_path = os.path.join(folder_path, chosen)
        
        x = random.randint(0, constants.SCREEN_WIDTH - prop_size[0])
        y = random.randint(0, constants.SCREEN_HEIGHT - prop_size[1])

        prop = ImageObject(x, y, *prop_size, image_path=full_path)
        group.add(prop)

#helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image,(w * scale, h* scale))