import pygame  
import constants
import random
import math
from gameobject import GameObject, ImageObject
from character import Character
from utils import spawn_random_props
from projectile import Projectile

pygame.init()

#got to lesson 8 on udemy to learn about this
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption("Smashing Dungeons")

#create clock for maintaining frame rate
clock = pygame.time.Clock()

#define player movement variables
moving_left = False
moving_right = False
moving_down = False
moving_up = False

#projectile directions
firing_up = False
firing_down = False
firing_left = False
firing_right = False



levels=['woodfloor.jpg','castlefloor.png','forestfloor.jpg','oceanfloor.jpg']

#music handling
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load("assets/audio/beat.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


#adding props

objects = pygame.sprite.Group()
spawn_random_props("castle", 3, objects)

#adding walls
walls = pygame.sprite.Group()

top_wall = GameObject(0, 0, constants.SCREEN_WIDTH, constants.WALL_THICKNESS)
bottom_wall = GameObject(0, constants.SCREEN_HEIGHT - constants.WALL_THICKNESS, constants.SCREEN_WIDTH, constants.WALL_THICKNESS)
left_wall = GameObject(0, 0, constants.WALL_THICKNESS, constants.SCREEN_HEIGHT)
right_wall = GameObject(constants.SCREEN_WIDTH - constants.WALL_THICKNESS, 0, constants.WALL_THICKNESS, constants.SCREEN_HEIGHT)
walls.add(top_wall, bottom_wall, left_wall, right_wall)


#making chars to load
# Create player
player = Character(300, 300,"player")

# Group for drawing and updates
character_group = pygame.sprite.Group()
character_group.add(player)

#List of solid objects the player can collide with
solids = pygame.sprite.Group()
solids.add(*walls)
solids.add(*objects)

#projectiles
projectiles = pygame.sprite.Group()

last_fire_time = 0
run=True
switchbg = True
counter=0
while run:

    if switchbg == True:
        level = random.choice(levels)
        startbut = pygame.image.load(f"assets/backgrounds/{level}")
        startbut_scaled = pygame.transform.scale(startbut, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        switchbg = False
        
    clock.tick(constants.FPS)
    screen.blit(startbut_scaled,(0,0))
    objects.draw(screen)
    #draw walls
    walls.draw(screen)
    ######Debugging code for changing background/room
    #counter+=1
    #if(counter%60 == 0):
        #switchbg=True
    #
    #################################################
    
    
    #calculate player movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0

    if keys[pygame.K_d]:
        dx = constants.SPEED
    if keys[pygame.K_a]:
        dx = -constants.SPEED
    if keys[pygame.K_w]:
        dy = -constants.SPEED
    if keys[pygame.K_s]:
        dy = constants.SPEED
    
    
    #event handler
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        #take keyboard presses
        if event.type == pygame.KEYDOWN:
            
            # Single-direction fire inputs
            if event.key in (pygame.K_UP, pygame.K_i):
                firing_up = True
            if event.key in (pygame.K_DOWN, pygame.K_k):
                firing_down = True
            if event.key in (pygame.K_LEFT, pygame.K_j):
                firing_left = True
            if event.key in (pygame.K_RIGHT, pygame.K_l):
                firing_right = True

            # Diagonal shortcuts
            if event.key == pygame.K_u:  # Up-left
                firing_up = True
                firing_left = True
            if event.key == pygame.K_o:  # Up-right
                firing_up = True
                firing_right = True
            if event.key == pygame.K_n:  # Down-left
                firing_down = True
                firing_left = True
            if event.key == pygame.K_PERIOD:  # Down-right
                firing_down = True
                firing_right = True 
        
        
    # 🔁 Allow held-key firing
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    fx = (1 if keys[pygame.K_RIGHT] or keys[pygame.K_l] else 0) + (-1 if keys[pygame.K_LEFT] or keys[pygame.K_j] else 0)
    fy = (1 if keys[pygame.K_DOWN] or keys[pygame.K_k] else 0) + (-1 if keys[pygame.K_UP] or keys[pygame.K_i] else 0)

    # Diagonal shortcuts
    if keys[pygame.K_u]:  # up-left
        fx = -1
        fy = -1
    elif keys[pygame.K_o]:  # up-right
        fx = 1
        fy = -1
    elif keys[pygame.K_n]:  # down-left
        fx = -1
        fy = 1
    elif keys[pygame.K_PERIOD]:  # down-right
        fx = 1
        fy = 1

    if (fx != 0 or fy != 0) and current_time - last_fire_time > constants.FIRE_COOLDOWN:
        magnitude = math.hypot(fx, fy)
        norm_dir = (fx / magnitude, fy / magnitude)
        projectile = Projectile(
            player.rect.centerx,
            player.rect.centery,
            norm_dir,
            speed=10,
            image_path="assets/projectiles/player/1.png",
            player_origin=True
        )
        projectiles.add(projectile)
        last_fire_time = current_time

    player.move(dx, dy,solids)  # Update position based on input
    character_group.update()
    projectiles.update(solids, screen.get_rect())
    
    for sprite in character_group:
        sprite.draw(screen) # Automatically draws based on .image and .rect
    

    projectiles.draw(screen)
    
    pygame.display.update()


pygame.quit()
