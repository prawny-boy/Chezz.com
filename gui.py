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
        handle_diameter=20,
        snap_to_values=True,
    ):
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
        self.handle_diameter = handle_diameter
        self.handle_x = self.calculate_handle_position()
        self.snap_to_values = snap_to_values
        self.is_dragging = False

    def calculate_handle_position(self):
        handle_radius = self.handle_diameter / 2
        return self.x + handle_radius + (
            (self.value - self.min_value) / (self.max_value - self.min_value)
        ) * (self.width - self.handle_diameter)

    def draw(self, screen:_pygame.Surface):
        _pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, border_radius=round(self.height / 4))
        _pygame.draw.circle(
            screen,
            self.handle_color,
            (self.handle_x, self.y + self.height // 2),
            self.handle_diameter // 2,
        )
        if self.labels:
            font = _pygame.font.Font(None, 24)
            label_font = _pygame.font.Font(None, 20)
            label_width = self.width // (len(self.labels) - 1)
            for i, label in enumerate(self.labels):
                label_surface = label_font.render(label, True, (255, 255, 255))
                label_x = self.x + i * label_width
                screen.blit(
                    label_surface,
                    (label_x - label_surface.get_width() // 2, self.y + self.height + max((self.handle_diameter - self.height)/2, 0)),
                )
        font = _pygame.font.Font(None, 36)
        value_text = font.render(str(self.value), True, (255, 255, 255))
        screen.blit(
            value_text,
            (self.x + self.width + self.handle_diameter/2 + 10, self.y - value_text.get_height() // 2),
        )

    def update(self, event):
        if event.type == _pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos):
                self.is_dragging = True
        elif event.type == _pygame.MOUSEMOTION:
            if hasattr(self, "is_dragging") and self.is_dragging:
                handle_radius = self.handle_diameter / 2
                mouse_x = max(
                    self.x,
                    min(event.pos[0], self.x + self.width)
                )
                self.handle_x = mouse_x
                raw_value = self.min_value + (
                    (self.handle_x - self.x)
                    / (self.width - self.handle_diameter)
                ) * (self.max_value - self.min_value)
                self.value = max(self.min_value, min(int(raw_value + 0.5), self.max_value))
                if self.snap_to_values:
                    self.handle_x = self.calculate_handle_position()
        elif event.type == _pygame.MOUSEBUTTONUP:
            self.is_dragging = False

    def is_hovered(self, pos):
        handle_radius = self.handle_diameter // 2
        handle_center = (self.handle_x, self.y + self.height // 2)
        dx = pos[0] - handle_center[0]
        dy = pos[1] - handle_center[1]
        return dx ** 2 + dy ** 2 <= handle_radius ** 2