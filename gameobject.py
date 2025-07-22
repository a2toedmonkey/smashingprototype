import pygame
import constants
import math
import os
import random

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class ImageObject(GameObject):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height)
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))

    def random_item(self, area_folder):
        folder_path = f"assets/props/{area_folder}"
        image_files = [
            f for f in os.listdir(folder_path) 
            if f.endswith(".png") or f.endswith(".jpg")
        ]
        if not image_files:
            raise FileNotFoundError(f"No image files found in {folder_path}")

        chosen = random.choice(image_files)
        full_path = os.path.join(folder_path, chosen)

        self.image = pygame.image.load(full_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.image.get_rect().size)