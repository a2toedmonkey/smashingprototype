import pygame
import constants
import math
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, image_path, player_origin=False):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (32, 32))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = speed
        self.player_origin = player_origin


    def update(self, obstacles, screen_rect):
        dx = self.direction[0] * self.speed
        dy = self.direction[1] * self.speed
        self.rect.x += dx
        self.rect.y += dy
        
        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if pygame.sprite.spritecollideany(self, obstacles) or not screen_rect.contains(self.rect):
            self.kill()


