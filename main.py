import pygame
import chess

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
SCREEN_HEIGHT = 800

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = pygame.Color('#b58863')
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

RANKS = {1: 575, 2: 525, 3: 475, 4: 425, 5: 375, 6: 325, 7: 275, 8: 225}
FILES = {'a': 225, 'b': 275, 'c': 325, 'd': 375, 'e': 425, 'f': 475, 'g': 525, 'h': 575}

class ChessBoard:
    def __init__(self, x, y, length, dark, light):
        self.x = x + length / 2
        self.y = y + length / 2
        self.s_length = length / 8
        self.dark = dark
        self.light = light
        
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

def central_rect(x, y, length, width):
    return pygame.Rect(x - width / 2, y - length / 2, length, width)

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Chezz.com")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

chessboard = ChessBoard(x=0, y=0, length=400, dark=BROWN, light=BEIGE)
board = chess.Board()
piece = Piece(50, 50, "white", "pawn")

if __name__ == "__main__":
    #splash_screen([company_logo, logo])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        chessboard.draw(screen)
        pygame.draw.rect(screen, GREEN, central_rect(FILES['a'], RANKS[1], 10, 10))
        pygame.display.flip()