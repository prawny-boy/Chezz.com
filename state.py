import pygame as _pygame
from sys import exit as _exit

from gui import Button, Slider
from settings import settings # still need to push these values into states stuff below
from chess import initialize_classic_game

BOARD_SIZE = settings["board"]["size"]
SCREEN_WIDTH = settings["screen"]["width"]
SCREEN_HEIGHT = settings["screen"]["height"]
BLACK = settings["colors"]["black"]

class State:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen:_pygame.Surface = screen

    def handle_event(self, event:_pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class StateManager:
    def __init__(self, initial_state:State):
        self.state = initial_state

    def set_state(self, new_state):
        self.state = new_state

    def handle_event(self, event):
        self.state.handle_event(event)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()

class SplashState(State):
    def __init__(self, manager, screen, icons_to_show):
        super().__init__(manager, screen)
        self.icons_to_show = [_pygame.transform.scale(icon, (200, 200)) for icon in icons_to_show]
        self.icon_idx = 0
        self.alpha = 0
        self.dir = "+"
        self.icon = self.icons_to_show[self.icon_idx]

    def handle_event(self, event):
        if event.type == _pygame.MOUSEBUTTONDOWN:
            self.dir = "-"

    def update(self):
        if self.dir == "+":
            self.alpha += 2
            if self.alpha >= 300:
                self.dir = "-"
        else:
            self.alpha -= 2
            if self.alpha <= 0:
                self.icon_idx += 1
                if self.icon_idx < len(self.icons_to_show):
                    self.icon = self.icons_to_show[self.icon_idx]
                    self.dir = "+"
                else:
                    self.manager.set_state(MenuState(self.manager, self.screen)) # Set state to menu

    def draw(self):
        self.screen.fill(BLACK)
        self.icon.set_alpha(self.alpha)
        self.screen.blit(self.icon, (self.screen.get_width() / 2 - self.icon.get_width() / 2,
                                     self.screen.get_height() / 2 - self.icon.get_height() / 2))

class MenuState(State):
    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.center_x = self.screen.get_width() / 2
        self.center_y = self.screen.get_height() / 2
        self.new_game_button = Button(self.center_x - 100, self.center_y - 100, 200, 50, "New Game", (0, 255, 0), (255, 255, 255))
        self.options_button = Button(self.center_x - 100, self.center_y, 200, 50, "Options", (0, 0, 255), (255, 255, 255))
        self.quit_button = Button(self.center_x - 100, self.center_y + 100, 200, 50, "Quit", (255, 0, 0), (255, 255, 255))

    def handle_event(self, event):
        if event.type == _pygame.MOUSEBUTTONDOWN:
            pos = _pygame.mouse.get_pos()
            if self.new_game_button.is_hovered(pos):
                self.manager.set_state(ClassicChessGameState(self.manager, self.screen))
            elif self.options_button.is_hovered(pos):
                self.manager.set_state(OptionsState(self.manager, self.screen))
            elif self.quit_button.is_hovered(pos):
                _pygame.quit()
                _exit()

    def draw(self):
        self.screen.fill(BLACK)
        self.new_game_button.draw(self.screen)
        self.options_button.draw(self.screen)
        self.quit_button.draw(self.screen)

class OptionsState(State):
    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.center_x = self.screen.get_width() / 2
        self.center_y = self.screen.get_height() / 2
    
        self.difficulty_slider = Slider(self.center_x - 200, self.center_y - 100, 400, 50, 0, 2, 1, ["Easy", "Medium", "Hard"], (100, 100, 100), (255, 0, 0))
        self.back_button = Button(self.center_x - 100, self.center_y + 50, 200, 50, "Back", (0, 200, 0), (255, 255, 255))

    def handle_event(self, event):
        self.difficulty_slider.update(event)
        if event.type == _pygame.MOUSEBUTTONDOWN and self.back_button.is_hovered(event.pos):
            self.manager.set_state(MenuState(self.manager, self.screen))

    def draw(self):
        self.screen.fill(BLACK)
        self.difficulty_slider.draw(self.screen)
        self.back_button.draw(self.screen)

class ClassicChessGameState(State):
    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.chessboard = initialize_classic_game(SCREEN_WIDTH / 2 - BOARD_SIZE / 2, SCREEN_HEIGHT / 2 - BOARD_SIZE / 2)
    
    def handle_event(self, event):
        if event.type == _pygame.MOUSEBUTTONDOWN:
            mouse_pos = _pygame.mouse.get_pos()
            self.chessboard.handle_click(mouse_pos)
        if event.type == _pygame.KEYDOWN:
            if event.key == _pygame.K_LEFT:
                self.chessboard.pop(1)
                self.chessboard.deselect_square()
    
    def update(self):
        self.chessboard.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.chessboard.draw(self.screen)