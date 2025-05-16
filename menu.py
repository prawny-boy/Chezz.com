"""
The starting point of the application which opens up main and option menus.
"""

import pygame as _pygame
import sys
from gui import Button, Slider
from settings import settings
from main import initiate_game

# Initialize Pygame and Settings
_pygame.init()

# Constants for the screen
SCREEN_WIDTH = settings["screen"]["width"]
SCREEN_HEIGHT = settings["screen"]["height"]
FPS = settings["screen"]["fps"]

# Create the screen
screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Chezz.com")
icon = _pygame.image.load("Assets/Sprites/Icon.png")
_pygame.display.set_icon(icon)
clock = _pygame.time.Clock()


class OptionMenu:
    def __init__(self, screen: _pygame.Surface):
        """Initializes the option menu with a difficulty slider."""
        self.screen = screen

        # Center positions
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        # Initialize slider for difficulty
        self.difficulty_slider = Slider(
            x=self.center_x - 200,  # Centered slider horizontally
            y=self.center_y - 100,  # Adjusted for vertical positioning
            width=400,
            height=50,
            labels=["Easy", "Medium", "Hard"],
            color=(100, 100, 100),
            handle_color=(255, 0, 0),
            min_value=0,  # Minimum value for the slider
            max_value=2,  # Maximum value for the slider (corresponding to the number of labels - 1)
            initial_value=1,  # The initial value (e.g., "Medium")
        )

        # Create the "Back" button, positioned below the slider
        self.back_button = Button(
            x=self.center_x - 100,  # Centered button horizontally
            y=self.center_y + 50,  # Positioned below the slider
            width=200,
            height=50,
            text="Back",
            color=(0, 200, 0),
            text_color=(255, 255, 255),
        )

    def draw(self):
        """Draw the option menu on the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Draw the difficulty slider
        self.difficulty_slider.draw(self.screen)

        # Draw the back button
        self.back_button.draw(self.screen)

        # Display the current difficulty on the screen
        font = _pygame.font.Font(None, 36)
        difficulty_text = font.render(
            f"Difficulty: {self.difficulty_slider.value}", True, (255, 255, 255)
        )
        self.screen.blit(
            difficulty_text,
            (self.center_x - difficulty_text.get_width() // 2, self.center_y - 150),
        )

    def handle_events(self, event):
        """Handle the events like mouse clicks and motion."""
        # Update slider based on events
        self.difficulty_slider.update(event)

        # Check if the "Back" button is clicked
        if event.type == _pygame.MOUSEBUTTONDOWN:
            if self.back_button.is_hovered(event.pos):
                print("Back button clicked!")
                # saving the difficulty
                settings["game"]["difficulty"] = self.difficulty_slider.value
                settings.save()
                print(f"Difficulty was saved to {self.difficulty_slider.value}")
                return True  # This signals that the menu should return to the main menu

        return False

    def update(self):
        """Update the menu state."""
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                sys.exit()

            # Handle events and check if back button was pressed
            if self.handle_events(event):
                return True  # Return to main menu after "Back" is pressed

        # Draw the updated screen
        self.draw()
        _pygame.display.flip()
        return False  # Keep in the option menu if "Back" isn't clicked


class Menu:
    def __init__(self):
        """Initializes the menu with buttons."""
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.new_game_button = Button(
            x=self.center_x - 100,  # Centered button horizontally
            y=self.center_y - 100,  # Positioned above the options button
            width=200,
            height=50,
            text="New Game",
            color=(0, 255, 0),
            text_color=(255, 255, 255),
        )
        self.options_button = Button(
            x=self.center_x - 100,  # Centered button horizontally
            y=self.center_y,  # Positioned below the "New Game" button
            width=200,
            height=50,
            text="Options",
            color=(0, 0, 255),
            text_color=(255, 255, 255),
        )
        self.quit_button = Button(
            x=self.center_x - 100,  # Centered button horizontally
            y=self.center_y + 100,  # Positioned below the options button
            width=200,
            height=50,
            text="Quit",
            color=(255, 0, 0),
            text_color=(255, 255, 255),
        )

    def draw(self, surface):
        """Draws all the buttons on the screen."""
        self.new_game_button.draw(surface)
        self.options_button.draw(surface)
        self.quit_button.draw(surface)

    def handle_event(self, event):
        """Handles events like mouse clicks on the buttons."""
        if event.type == _pygame.MOUSEBUTTONDOWN:
            if self.new_game_button.is_hovered(event.pos):
                print("New Game clicked!")
                return "new_game"
            elif self.options_button.is_hovered(event.pos):
                return "options"  # Switch to options menu
            elif self.quit_button.is_hovered(event.pos):
                print("Quit clicked!")
                _pygame.quit()
                sys.exit()
        return None


def splash_screen(icons_to_show: list[_pygame.Surface]):
    alpha = 0
    dir = "+"
    icon_idx = 0
    for icon in icons_to_show:
        icons_to_show[icons_to_show.index(icon)] = _pygame.transform.scale(
            icon, (200, 200)
        )
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
        screen.blit(
            icon,
            (
                SCREEN_WIDTH / 2 - icon.get_width() / 2,
                SCREEN_HEIGHT / 2 - icon.get_height() / 2,
            ),
        )
        _pygame.display.flip()
        clock.tick(FPS)


def main():

    # splash_screen([company_logo, logo])

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
        clock.tick(FPS)

    _pygame.quit()


# Start the main loop
if __name__ == "__main__":
    main()
