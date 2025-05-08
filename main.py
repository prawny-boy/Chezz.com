"""Chezz.com is a pygame clone of Chess.com, made as a fun project."""
# Importing/Dependencies
import pygame
import pygame_gui as gui
from sys import exit, dont_write_bytecode

# Initalisations
pygame.init()
clock = pygame.time.Clock()

# Sprites
logo = pygame.image.load("Assets/Sprites/logo.png")
icon = pygame.image.load("Assets/Sprites/icon.png")
icon_pawn = pygame.image.load("Assets/Sprites/iconpawn.png")
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
class BoardLocation:
    def __init__(self, row:int, column:int):
        self.row = row
        self.column = column

class MovementPattern:
    def __init__(self, name:str, pattern:list[BoardLocation], movement_type:str):
        self.movement_type = movement_type # "normal", "jump" means ignore pieces in the way
        self.name = name
        self.pattern = pattern # list of tuples (x, y) of what to add to the current position (0, 0)
    
    def get_resulting_positions(self, location:BoardLocation): # this does not check for board limits or pieces in the way
        positions = []
        for move in self.pattern:
            new_row = location.row + move.row
            new_column = location.column + move.column
            positions.append(BoardLocation(new_row, new_column))
        return positions

    def get_movement_type(self):
        return self.movement_type

class Piece:
    def __init__(self, row, column, movement:MovementPattern, image:pygame.Surface):
        self.row = row
        self.column = column
        self.movement = movement
        self.image = image
    
    def draw(self, screen:pygame.Surface):
        pass

    def move(self, row:int, column:int):
        self.row = row
        self.column = column

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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(GAME_NAME)
    pygame.display.set_icon(icon_pawn)

    manager = gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    hello_button = gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 275), (100, 50)),
        text='Say Hello',
        manager=manager)

    # Splash Screen
    splash_screen([icon, company_logo])

    # Game Loop
    while True:
        time_delta = clock.tick(FRAME_RATE) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
            
            manager.process_events(event)
        
        manager.update(time_delta)

        screen.fill((0, 0, 0))
        manager.draw_ui(screen)

        pygame.display.update()