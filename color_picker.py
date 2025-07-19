import pygame

class ColorPicker:
    def __init__(self, image_path, coords):
        pygame.display.init()
        self.image = pygame.image.load(image_path)
        self.img_rect = self.image.get_rect(center=coords)
        self.selected_color = (0, 0, 0, 255)
        self.running = True

    def get_color_at_mouse(self, pos):
        x, y = pos
        # Map screen coordinates to image coordinates if your picker can be drawn anywhere
        x_rel = x - self.img_rect.left
        y_rel = y - self.img_rect.top
        if 0 <= x_rel < self.image.get_width() and 0 <= y_rel < self.image.get_height():
            return self.image.get_at((int(x_rel), int(y_rel)))
        else:
            return None


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    color = self.get_color_at_mouse()
                    if color:  # Only update if mouse is over the image
                        self.selected_color = color
                        print("Last selected color:", self.selected_color)
            self.draw()
        pygame.quit()

    def draw(self, screen):
        screen.blit(self.image, self.img_rect)
        
    def is_hovered(self, pos):
        return self.img_rect.collidepoint(pos)

# Usage example:
if __name__ == "__main__":
    picker = ColorPicker("Assets\\Sprites\\color_hex.png")
    picker.run()
