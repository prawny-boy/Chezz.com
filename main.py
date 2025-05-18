import pygame as _pygame
from sys import exit as _exit

from chess import ChessBoard, ClassicPiecesMovement, BOARD_CONFIG
from gui import splash_screen
from settings import settings
from menu import Menu, OptionMenu

# pygame initalization
_pygame.init()
_pygame.font.init()
_pygame.mixer.init()

# ASSETS
# Sounds
# click_sound = _pygame.mixer.Sound("Assets/Sounds/click.wav")
# move_sound = _pygame.mixer.Sound("Assets/Sounds/move.wav")
# Sprites
logo = _pygame.image.load("Assets/Sprites/Logo.png")
icon = _pygame.image.load("Assets/Sprites/Icon.png")
company_logo = _pygame.image.load("Assets/Sprites/Company.png")

# CONSTANTS
FRAME_RATE = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVE_HIGHLIGHT_RADIUS = 7.5
CAPTURE_HIGHLIGHT_RADIUS = 30
CAPTURE_HIGHLIGHT_WIDTH = 3
PIECE_SIZE = 50
BOARD_SIZE = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = _pygame.Color('#b58863')
BEIGE = _pygame.Color('#f0d9b5')
HIGHLIGHT = _pygame.Color('#8877DD99')
MOVE_HIGHLIGHT = _pygame.Color('#5fa14460')
CAPTURE_HIGHLIGHT = _pygame.Color('#d42a2a60')

BOARD_CONFIG = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

PIECE_SCALING = {
    "p": 60,
    "n": 52,
    "b": 70,
    "r": 80,
    "q": 50,
    "k": 50
}

# Variables
show_debug_info = True

# CLASSES


# FUNCTIONS
def splash_screen(icons_to_show:list[_pygame.Surface]):
    alpha = 0
    dir = "+"
    icon_idx = 0
    for icon in icons_to_show:
        icons_to_show[icons_to_show.index(icon)] = _pygame.transform.scale(icon, (200, 200))
    icon = icons_to_show[icon_idx]
    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                exit()
            if event.type == _pygame.MOUSEBUTTONDOWN:
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
        _pygame.display.flip()
        clock.tick(FRAME_RATE)

screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Chezz.com")
_pygame.display.set_icon(icon)
clock = _pygame.time.Clock()

if __name__ == "__main__":
    splash_screen([company_logo, logo])

    # Create Chess Board and Pieces
    chessboard = ChessBoard(x = SCREEN_WIDTH / 2 - BOARD_SIZE / 2, 
                            y = SCREEN_HEIGHT / 2 - BOARD_SIZE / 2, 
                            size = BOARD_SIZE, starting_configuration=BOARD_CONFIG, 
                            pieces={
                                'p': {'pattern': ClassicPiecesMovement.pawn_movement, 'sprite': None, 'worth': 1},
                                'r': {'pattern': ClassicPiecesMovement.rook_movement, 'sprite': None, 'worth': 5},
                                'n': {'pattern': ClassicPiecesMovement.knight_movement, 'sprite': None, 'worth': 3},
                                'b': {'pattern': ClassicPiecesMovement.bishop_movement, 'sprite': None, 'worth': 3},
                                'q': {'pattern': ClassicPiecesMovement.queen_movement, 'sprite': None, 'worth': 9},
                                'k': {'pattern': ClassicPiecesMovement.king_movement, 'sprite': None, 'worth': 0}
                            })
    
    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                _exit()

            if event.type == _pygame.MOUSEBUTTONDOWN:
                mouse_pos = _pygame.mouse.get_pos()
                chessboard.handle_click(mouse_pos)
            if event.type == _pygame.KEYDOWN:
                if event.key == _pygame.K_LEFT:
                    chessboard.pop(1)
                    chessboard.deselect_square()

        # Updates
        chessboard.update()

        # Drawing the screen
        screen.fill(BLACK)
        chessboard.draw(screen)

        _pygame.display.flip()
        clock.tick(FRAME_RATE)


if __name__ == "__main__":

    splash_screen(
        [company_logo, logo],
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        screen=screen,
        framerate=FRAME_RATE,
        clock=clock,
    )

    # show menu
    menu = Menu()
    options_menu = OptionMenu(screen)

    running = True
    in_options_menu = False  # Flag to track if we're in the options menu

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        if in_options_menu:
            # Handle the option menu
            if options_menu.update():  # If "Back" is clicked in OptionMenu
                in_options_menu = False  # Go back to main menu
        else:
            # Handle the main menu
            menu.draw(screen)

            # Handle events for the main menu
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    running = False
                result = menu.handle_event(event)
                if result == "new_game":
                    initiate_game()
                if result == "options":
                    in_options_menu = True  # Switch to options menu
        # Update the screen
        _pygame.display.flip()

        # Frame rate
        clock.tick(FRAME_RATE)

    _pygame.quit()
