"""Chezz.com is a pygame clone of Chess.com, made as a fun project."""
# Importing/Dependencies
import pygame
import pygame_gui
from sys import exit, dont_write_bytecode

# Initalisations
pygame.init()
clock = pygame.time.Clock()

# Sprites
logo = pygame.image.load("Assets/Sprites/logo.png")
icon = pygame.image.load("Assets/Sprites/icon.png")
company_logo = pygame.image.load("Assets/Sprites/company.png")

# Constants
SETUP = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"],
] # Black is uppercase, white is lowercase

# figure out way to define movements in pieces
PIECES = {}
ORIGINAL_SPRITES = {} # piece: sprite

# Pygame Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_RATE = 60 # Delta Time?
GAME_NAME = "Chezz.com (Cheese Chess)"

# Variables
dont_write_bytecode = True

# Classes
class Piece:
    def __init__(self, x, y, color, movement, image):
        self.x = x
        self.y = y
        self.color = color
        self.movement = movement
        self.image = image

# Functions
def create_board():
    pass

def splash_screen(icons_to_show:list[pygame.Surface]):
    alpha = 0
    dir = "+"
    icon_idx = 0
    for icon in icons_to_show:
        icons_to_show[icons_to_show.index(icon)] = pygame.transform.scale(icon, (200, 200))
    icon = icons_to_show[icon_idx]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                dir = "-"
        
        if dir == "+":
            alpha += 2
            if alpha == 300:
                dir = "-"
        else:
            alpha -= 2
            if alpha == 0:
                icon_idx += 1
                try:
                    icon = icons_to_show[icon_idx]
                except IndexError:
                    screen.fill((0, 0, 0))
                    return
                dir = "+"
        
        screen.fill((0, 0, 0))
        icon.set_alpha(alpha)
        screen.blit(icon, (SCREEN_WIDTH / 2 - icon.get_width() / 2, SCREEN_HEIGHT / 2 - icon.get_height() / 2))
        pygame.display.flip()
        clock.tick(FRAME_RATE)

if __name__ == "__main__":
    # Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_NAME)
    pygame.display.set_icon(icon)

    # Splash Screen
    splash_screen([icon, company_logo])

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        
        pygame.display.flip()
        clock.tick(FRAME_RATE)