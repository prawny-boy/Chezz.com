import pygame as _pygame

from chess import ChessBoard, ClassicPiecesMovement, BOARD_CONFIG
from gui import splash_screen
from settings import settings
from menu import Menu, OptionMenu

# Pygame Initalization
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
SCREEN_WIDTH = settings["screen"]["width"]
SCREEN_HEIGHT = settings["screen"]["height"]
FRAME_RATE = settings["screen"]["fps"]
PIECE_SIZE = settings["board"]["piece_size"]
BOARD_SIZE = settings["board"]["size"]
WHITE = tuple(settings["colors"]["white"])
BLACK = tuple(settings["colors"]["black"])
RED = tuple(settings["colors"]["red"])
GREEN = tuple(settings["colors"]["green"])

BROWN = _pygame.Color("#b58863")
BEIGE = _pygame.Color("#f0d9b5")
HIGHLIGHT = _pygame.Color("#8877DD99")
MOVE_HIGHLIGHT = _pygame.Color("#5fa14460")
CAPTURE_HIGHLIGHT = _pygame.Color("#d42a2a60")

screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Chezz.com")
_pygame.display.set_icon(icon)
clock = _pygame.time.Clock()

def initiate_game():
    chessboard = ChessBoard(
        x=SCREEN_WIDTH / 2 - BOARD_SIZE / 2,
        y=SCREEN_HEIGHT / 2 - BOARD_SIZE / 2,
        size=BOARD_SIZE,
        starting_configuration=BOARD_CONFIG,
        pieces={
            "p": {
                "pattern": ClassicPiecesMovement.pawn_movement,
                "sprite": None,
                "worth": 1,
            },
            "r": {
                "pattern": ClassicPiecesMovement.rook_movement,
                "sprite": None,
                "worth": 5,
            },
            "n": {
                "pattern": ClassicPiecesMovement.knight_movement,
                "sprite": None,
                "worth": 3,
            },
            "b": {
                "pattern": ClassicPiecesMovement.bishop_movement,
                "sprite": None,
                "worth": 3,
            },
            "q": {
                "pattern": ClassicPiecesMovement.queen_movement,
                "sprite": None,
                "worth": 9,
            },
            "k": {
                "pattern": ClassicPiecesMovement.king_movement,
                "sprite": None,
                "worth": 0,
            },
        },
    )

if __name__ == "__main__":
    splash_screen(
        [company_logo, logo],
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        screen=screen,
        framerate=FRAME_RATE,
        clock=clock,
    )
    # Show Menu
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