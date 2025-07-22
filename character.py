import pygame
import constants
import math
import os

class Character(pygame.sprite.Sprite):
    ACTIONS = ["move/side", "move/up", "move/down", "attack", "die"]
    
    def __init__(self, x, y, type):
        super().__init__()  # required for Sprite setup
        self.type=type
        self.hp = 1
        self.dmg = 1
        self.isPlayer = False
        self.isDead = False
        self.isAlive = True
        self.running = False
        self.flip = False

        # Visuals and position
        #self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        #self.image.fill(color)
        #self.rect = self.image.get_rect(center=(x, y))

        # Animation placeholders
        self.animations={}
        #self.action = None
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        self.action = "move/down"
        self.animations = self.load_animation_frames(f"assets/characters/{self.type}", Character.ACTIONS, constants.CHARACTER_SIZES[self.type])

        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, dx, dy, obstacles, status=0):
        self.running = dx != 0 or dy != 0

        if dx < 0:
            self.flip = True
        elif dx > 0:
            self.flip = False

            # Determine direction for animation
        if dy < 0:
            self.action = "move/up"
        elif dy > 0:
            self.action = "move/down"
        elif dx != 0:
            self.action = "move/side"
        
        if dx != 0 and dy != 0:
            dx *= math.sqrt(2) / 2
            dy *= math.sqrt(2) / 2

        if status == -1:
            dx /= 2
            dy /= 2
        elif status == 1:
            dx *= 2
            dy *= 2

        # Check horizontal movement
        future_rect = self.rect.copy()
        future_rect.x += dx
        if not pygame.sprite.spritecollideany(self._make_temp(future_rect), obstacles):
            self.rect.x += dx

        # Check vertical movement
        future_rect = self.rect.copy()
        future_rect.y += dy
        if not pygame.sprite.spritecollideany(self._make_temp(future_rect), obstacles):
            self.rect.y += dy
            
        
    def path(self,player_x,player_y,scent=False,scent_range=0):
        #check if the enemy can see the player->no obstructions in a straight line
        #scent assumes the person is within range, has to be set as true and then set with a range
        #represents the range at which an enemy will move toward the player
        player_detected = False
        #loop to see if player detected
        #scent works with sight not in lieu of
        if scent:
            pass
        
        #check vision below here
            pass
        
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 100  # ms between frames
        now = pygame.time.get_ticks()

        if now - self.update_time > animation_cooldown:
            self.update_time = now
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.action])
            old_center = self.rect.center
            self.image = self.animations[self.action][self.frame_index]
            self.rect = self.image.get_rect(center=old_center)
    
    def draw(self, surface):
        frame = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(frame, self.rect)
    
    def _make_temp(self, rect):
        temp = pygame.sprite.Sprite()
        temp.rect = rect
        return temp
    

    @staticmethod
    def load_animation_frames(base_path, actions, target_size=(64, 64)):
        animations = {}
        for action in actions:
            action_path = os.path.join(base_path, action)

            # If the action directory has subfolders (e.g. side, up, down)
            if any(os.path.isdir(os.path.join(action_path, d)) for d in os.listdir(action_path)):
                for subdir in os.listdir(action_path):
                    full_path = os.path.join(action_path, subdir)
                    if os.path.isdir(full_path):
                        frames = []
                        for filename in sorted(os.listdir(full_path), key=lambda x: int(x.split('.')[0])):
                            img = pygame.image.load(os.path.join(full_path, filename)).convert_alpha()
                            img = pygame.transform.scale(img, target_size)
                            frames.append(img)
                        animations[f"{action}/{subdir}"] = frames
            else:
                frames = []
                for filename in sorted(os.listdir(action_path), key=lambda x: int(x.split('.')[0])):
                    img = pygame.image.load(os.path.join(action_path, filename)).convert_alpha()
                    img = pygame.transform.scale(img, target_size)
                    frames.append(img)
                animations[action] = frames

        return animations


