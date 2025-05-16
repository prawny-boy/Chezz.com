"""
Module about the screen.
"""

import pygame as _pygame

from settings import settings

SCREEN_WIDTH = settings["screen"]["width"]
SCREEN_HEIGHT = settings["screen"]["height"]

_pygame.init()
_pygame.font.init()
_pygame.mixer.init()
screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Chezz.com")
icon = _pygame.image.load("Assets/Sprites/Icon.png")
_pygame.display.set_icon(icon)
clock = _pygame.time.Clock()
