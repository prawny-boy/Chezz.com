import pygame as _pygame

centered_rect = lambda x, y, width, height: _pygame.Rect(x - width // 2, y - height // 2, width, height) 

class Text:
    def __init__(self, text, x, y, font_filepath, font_size, colour):
        self.text = text
        self.x = x
        self.y = y
        self.font = _pygame.font.Font(font_filepath, font_size)
        self.colour = colour

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)

class Button(_pygame.sprite.Sprite):
    def __init__(
        self,
        x:int,
        y:int, 
        width:int, 
        height:int,
        text:str,
        colour:tuple, 
        text_colour:tuple,
        text_font:_pygame.font.Font = None,
        border_colour:tuple = (0, 0, 0), # this is the colour of the border
        disabled:bool = False,
        border_width:int = 5, # this is thickness of the border
        border_radius:int = -1, # this is curving of edges
        accent_type:str = "size", # 3 modes, colour, size and opacity
        accent_value:tuple|int = (1.2, 1.2) # this is the value of the accent, it can be a rgb value, size added (int) or the opacity of accented (int)
    ):
        super().__init__()
        offset = (width / 2, height / 2)
        self.coordinates = (x - offset[0], y - offset[1])
        self.size = (width, height)
        self.colour = colour
        self.text = text
        self.disabled = disabled
        self.text_colour = text_colour
        if text_font is None:
            text_font = _pygame.font.Font(None, 36)
        self.text_font = text_font
        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.accent_type = accent_type
        self.accent_value = accent_value
    
    def is_hovered(self, mouse_pos) -> bool:
        if self.disabled:
            return False
        button_rect = _pygame.rect.Rect(self.coordinates, self.size)
        if button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def draw(self, screen: _pygame.Surface):
        mouse_pos = _pygame.mouse.get_pos()
        hover = self.is_hovered(mouse_pos)
        if self.disabled:
            hover = False
        if self.accent_type == "size" and hover:
            size = (self.size[0] * self.accent_value[0], self.size[1] * self.accent_value[1])
        else:
            size = self.size
        self.image = _pygame.Surface(size)
        if self.disabled:
            self.image.set_alpha(128)
        if self.accent_type == "size" and hover:
            self.rect = self.image.get_rect(topleft=(self.coordinates[0]+(self.size[0]-size[0])/2, self.coordinates[1]+(self.size[1]-size[1])/2))
        else:
            self.rect = self.image.get_rect(topleft=self.coordinates)
        if self.accent_type == "colour" and hover:
            _pygame.draw.rect(self.image, self.accent_value, self.image.get_rect())
        elif self.accent_type == "opacity" and hover:  # no work :(
            _pygame.draw.rect(self.image, (self.colour[0], self.colour[1], self.colour[2], self.accent_value), self.image.get_rect())
        else:
            _pygame.draw.rect(self.image, self.colour, self.image.get_rect())
        _pygame.draw.rect(self.image, self.border_colour, self.image.get_rect(), self.border_width, self.border_radius)
        text_surface = self.text_font.render(self.text, True, self.text_colour)
        offset = (self.image.get_width() / 2 - text_surface.get_width() / 2, self.image.get_height() / 2 - text_surface.get_height() / 2)
        text_rect = text_surface.get_rect(topleft=offset)
        self.image.blit(text_surface, text_rect)
        # Blit the button onto the surface
        screen.blit(self.image, self.rect)

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
        labels,
        color,
        handle_color,
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
    
