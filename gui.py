"""
Implements the gui elements of pygame such as button and slider
"""
import pygame as _pygame
from typing import Optional, Tuple

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
        _pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_hovered(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        min_value,
        max_value,
        initial_value,
        labels=None,
        color=(100, 100, 100),
        handle_color=(255, 0, 0),
    ):
        """
        Initializes the slider with a specific range and initial value.

        Args:
            x (int): The x-coordinate of the slider's position.
            y (int): The y-coordinate of the slider's position.
            width (int): The width of the slider.
            height (int): The height of the slider.
            min_value (int): The minimum value of the slider.
            max_value (int): The maximum value of the slider.
            initial_value (int): The initial value of the slider (within min_value and max_value).
            labels (list): Optional labels for the slider (e.g., ["Low", "High"]).
            color (tuple): The color of the slider's track.
            handle_color (tuple): The color of the slider's handle.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.labels = labels
        self.color = color
        self.handle_color = handle_color
        self.handle_width = 20
        self.handle_x = self.calculate_handle_position()

    def calculate_handle_position(self):
        """Calculates the x-coordinate of the slider handle based on the current value."""
        return self.x + (
            (self.value - self.min_value) / (self.max_value - self.min_value)
        ) * (self.width - self.handle_width)

    def draw(self, screen):
        """Draw the slider on the screen."""
        # Draw the track
        _pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Draw the handle
        _pygame.draw.rect(
            screen,
            self.handle_color,
            (
                self.handle_x,
                self.y - self.height // 2,
                self.handle_width,
                self.height * 2,
            ),
        )

        # Draw labels if provided
        if self.labels:
            font = _pygame.font.Font(None, 24)
            label_font = _pygame.font.Font(None, 20)
            label_width = self.width // (len(self.labels) - 1)
            for i, label in enumerate(self.labels):
                label_surface = label_font.render(label, True, (255, 255, 255))
                label_x = self.x + i * label_width
                screen.blit(
                    label_surface,
                    (label_x - label_surface.get_width() // 2, self.y + self.height),
                )

        # Draw the current value next to the slider
        font = _pygame.font.Font(None, 36)
        value_text = font.render(str(self.value), True, (255, 255, 255))
        screen.blit(
            value_text,
            (self.x + self.width + 10, self.y - value_text.get_height() // 2),
        )

    def update(self, event):
        """Update the handle's position based on mouse drag events."""
        if event.type == _pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos):
                self.is_dragging = True
        elif event.type == _pygame.MOUSEMOTION:
            if hasattr(self, "is_dragging") and self.is_dragging:
                # Restrict the handle's movement to the width of the slider
                mouse_x = max(
                    self.x, min(event.pos[0], self.x + self.width - self.handle_width)
                )
                self.handle_x = mouse_x
                # Calculate the new value based on the handle's position
                self.value = int(
                    self.min_value
                    + ((self.handle_x - self.x) / (self.width - self.handle_width))
                    * (self.max_value - self.min_value)
                )
        elif event.type == _pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def is_hovered(self, pos):
        """Check if the mouse is over the slider handle."""
        return (
            self.x <= pos[0] <= self.x + self.width
            and self.y - self.height // 2 <= pos[1] <= self.y + self.height // 2
        )
