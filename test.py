import pygame
import os

pygame.init()

# Folder containing your sprite images
SPRITES_FOLDER = os.path.join("Assets", "Sprites")

def load_all_sprites(folder):
    sprites = {}
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            path = os.path.join(folder, filename)
            image = pygame.image.load(path).convert_alpha()
            sprites[filename] = image
    return sprites

# Load all sprites into a dictionary

