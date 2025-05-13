"""
Implements the gui elements of pygame such as button and slider
"""

import pygame as _pygame
from typing import Optional, Tuple, List


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        font: Optional[_pygame.font.Font] = None,
    ):
        """
        Initializes a button with position, size, text, colors, and font.

        Args:
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text to display on the button.
            color (Tuple[int, int, int]): The button's background color as an RGB tuple.
            text_color (Tuple[int, int, int]): The text color as an RGB tuple.
            font (Optional[_pygame.font.Font]): An optional font object for the button's text.
                If None, the default font with size 36 is used.
        """
        self.rect: _pygame.Rect = _pygame.Rect(x, y, width, height)
        self.text: str = text
        self.color: Tuple[int, int, int] = color
        self.text_color: Tuple[int, int, int] = text_color

        # Use default font if none is provided
        if font is None:
            font = _pygame.font.Font(None, 36)

        self.text_surface: _pygame.Surface = font.render(
            self.text, True, self.text_color
        )
        self.text_rect: _pygame.Rect = self.text_surface.get_rect(
            center=self.rect.center
        )

    def draw(self, surface: _pygame.Surface) -> None:
        """
        Draws the button on the given surface.

        Args:
            surface (_pygame.Surface): The Pygame surface on which to draw the button.
        """
        _pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if the mouse is hovering over the button.

        Args:
            pos (Tuple[int, int]): A tuple representing the mouse position (x, y).

        Returns:
            bool: True if the mouse is over the button, False otherwise.
        """
        return self.rect.collidepoint(pos)


class Slider:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        labels: List[str],
        color: Tuple[int, int, int],
        handle_color: Tuple[int, int, int],
    ):
        """
        Initializes the slider with labeled values.

        Args:
            x (int): The x-coordinate of the slider's top-left corner.
            y (int): The y-coordinate of the slider's top-left corner.
            width (int): The width of the slider.
            height (int): The height of the slider.
            labels (List[str]): A list of labels to represent the slider values.
            color (Tuple[int, int, int]): The color of the slider background.
            handle_color (Tuple[int, int, int]): The color of the slider handle.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.labels = labels
        self.color = color
        self.handle_color = handle_color

        # Calculate the positions for the labels
        self.label_positions = [
            x + (i * (width // (len(labels) - 1))) for i in range(len(labels))
        ]

        # Create the handle's rectangle
        self.handle_width = 20
        self.handle_rect = _pygame.Rect(
            self.x, self.y + (self.height // 4), self.handle_width, self.height // 2
        )
        self.is_dragging = False
        self.value_index = 0

    def draw(self, surface):
        """
        Draw the slider on the given surface.

        Args:
            surface: The Pygame surface to draw on.
        """
        # Draw the slider background
        _pygame.draw.rect(
            surface, self.color, _pygame.Rect(self.x, self.y, self.width, self.height)
        )

        # Draw the handle
        _pygame.draw.rect(surface, self.handle_color, self.handle_rect)

        # Draw labels
        font = _pygame.font.Font(None, 30)
        for i, label in enumerate(self.labels):
            label_surface = font.render(label, True, (255, 255, 255))
            label_rect = label_surface.get_rect(
                center=(self.label_positions[i], self.y + self.height + 10)
            )
            surface.blit(label_surface, label_rect)

    def update(self, event):
        """
        Update the slider based on mouse events.

        Args:
            event: The Pygame event to process.
        """
        if event.type == _pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.is_dragging = True
        elif event.type == _pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == _pygame.MOUSEMOTION:
            if self.is_dragging:
                new_x = max(
                    self.x, min(event.pos[0], self.x + self.width - self.handle_width)
                )
                self.handle_rect.x = new_x
                self.update_value()

    def update_value(self):
        """
        Update the slider's value based on the handle's position.
        """
        # Get the relative position of the handle within the slider
        rel_pos = self.handle_rect.centerx - self.x
        # Calculate the index of the label based on the position of the handle
        self.value_index = min(
            len(self.labels) - 1,
            max(0, rel_pos // (self.width // (len(self.labels) - 1))),
        )

    @property
    def value(self):
        """
        Get the current value of the slider, represented by the label at the handle's position.

        Returns:
            str: The label corresponding to the current slider value.
        """
        return self.labels[self.value_index]
