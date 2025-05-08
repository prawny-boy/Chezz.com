# IMPORTS/DEPENDENCIES
import pygame
import chess

# INITIASATIONS
pygame.init()
pygame.font.init()
pygame.mixer.init()

# SPRITES
logo = pygame.image.load("Assets/Sprites/logo.png")
icon = pygame.image.load("Assets/Sprites/icon.png")
icon_pawn = pygame.image.load("Assets/Sprites/iconpawn.png")
company_logo = pygame.image.load("Assets/Sprites/company.png")

# Constants
FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BrankN = pygame.Color('#b58863')
BEIGE = pygame.Color('#f0d9b5')

BOARD_CONFIG = [
    ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'], 
    ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'],
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn'], 
    ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
]

# CLASSES
class BoardLocation:
    def __init__(self, rank:int, file:int):
        self.rank = rank
        self.file = file

class MovementPattern:
    def __init__(self, name:str, pattern:list[BoardLocation], movement_type:str):
        self.movement_type = movement_type # "normal", "king" can move into check,"jump" means ignore pieces in the way
        self.name = name
        self.pattern = pattern # list of tuples (x, y) of what to add to the current position (0, 0)
    
    def get_resulting_positions(self, location:BoardLocation): # this does not check for board limits or pieces in the way
        positions = []
        for move in self.pattern:
            new_rank = location.rank + move.rank
            new_file = location.file + move.file
            positions.append(BoardLocation(new_rank, new_file))
        return positions

    def get_movement_type(self):
        return self.movement_type

class ChessBoard:
    def __init__(self, x, y, length, dark, light):
        self.x = x - length / 2
        self.y = y - length / 2
        self.s_length = length / 8
        self.dark = dark
        self.light = light
        self.ranks_locations, self.files_locations = self.calculate_positions()

    def calculate_positions(self):
        """Generate RANKS and FILES dictionaries based on board position."""
        ranks = {i + 1: int(self.y + (7 - i) * self.s_length + self.s_length / 2) for i in range(8)}
        files = {chr(97 + j): int(self.x + j * self.s_length + self.s_length / 2) for j in range(8)}
        return ranks, files
        
    def draw(self, screen):
        x = self.x
        y = self.y
        l = self.s_length
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.dark
                else:
                    color = self.light
                pygame.draw.rect(screen, color, (x + i * l, y + j * l, l, l))

class Piece:
    def __init__(self, rank, file, movement:MovementPattern, image:pygame.Surface):
        self.rank = rank
        self.file = file
        self.movement = movement
        self.image = image
    
    def draw(self, screen:pygame.Surface):
        pass

    def move(self, rank:int, file:int):
        self.rank = rank
        self.file = file

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

def central_rect(x, y, length, width):
    return pygame.Rect(x - width / 2, y - length / 2, length, width)

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chezz.com")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    splash_screen([company_logo, logo])

    # Create the chessboard and pieces
    chessboard = ChessBoard(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, length=400, dark=BrankN, light=BEIGE)

    while True:
        clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        chessboard.draw(screen)
        pygame.draw.rect(screen, GREEN, central_rect(chessboard.files_locations["a"], chessboard.ranks_locations[1], 10, 10))
        pygame.display.flip()