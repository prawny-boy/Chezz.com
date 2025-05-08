import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chezz.com")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class ChessBoard:
    def __init__(self, x, y, length, dark, light):
        self.x = x
        self.y = y
        self.s_length = length / 8
        self.dark = dark
        self.light = light
        
    def draw(self, screen):
        x = self.x
        y = self.y
        l = self.s_length
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = self.light
                else:
                    color = self.dark
                pygame.draw.rect(screen, color, (x + i * l, y + j * l, l, l))

board = ChessBoard(50, 50, 400, GREEN, WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(BLACK)
    board.draw(screen)
    pygame.display.flip()