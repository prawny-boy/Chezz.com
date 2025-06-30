import pygame as _pygame

from settings import settings
from state import StateManager, SplashState

# Initalizations
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

if __name__ == "__main__":
    # Initialize Pygame Screen
    screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    _pygame.display.set_caption("Chezz.com")
    _pygame.display.set_icon(icon)
    clock = _pygame.time.Clock()

    # Initialize the state manager
    state_manager = StateManager(
        initial_state=SplashState(None, screen, [company_logo, logo]),
        default_variables={"theme": 1}
    )
    state_manager.state.manager = state_manager

    # Main Loop
    running = True
    while running:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                running = False
            state_manager.handle_event(event)
        
        state_manager.update()
        state_manager.draw()
        
        _pygame.display.flip()
        clock.tick(FRAME_RATE)