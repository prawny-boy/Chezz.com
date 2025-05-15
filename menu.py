import pygame
import sys

pygame.init()
pygame.font.init()


centered_rect = lambda x, y, width, height: pygame.Rect(x - width // 2, y - height // 2, width, height)

class Text:
    def __init__(self, text, x, y, font_filepath, font_size, colour):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_filepath, font_size)
        self.colour = colour

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)
        

class Button:
    def __init__(self, text, x, y, width, height, font_filepath, font_size, text_colour, button_colour, outline_colour):
        self.text = Text(text = text,
                               x = x,
                               y = y,
                               font_filepath = font_filepath,
                               font_size = font_size,
                               colour = text_colour)
        self.rect = centered_rect(x, y, width, height)
        self.colour = button_colour
        self.outline = outline_colour
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
        pygame.draw.rect(surface, self.outline, self.rect, 3)
        self.text.draw(surface)
        
        
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chezz.com")
clock = pygame.time.Clock()

text = Text(text = "Chezz.com", 
                  x = 400, 
                  y = 300, 
                  font_filepath = 'Assets/Fonts/AovelSansRounded-rdDL.ttf', 
                  font_size = 100, 
                  colour = (255, 255, 255))

button = Button(text = "Start Game",
                x = 400,
                y = 400,
                width = 300,
                height = 100,
                font_filepath = 'Assets/Fonts/AovelSansRounded-rdDL.ttf',
                font_size = 50,
                text_colour = (0, 0, 255),
                button_colour = (0, 255, 0),
                outline_colour = (255, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((0, 0, 0))
    
    text.draw(screen)
    button.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)