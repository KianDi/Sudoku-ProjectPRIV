import pygame
class Cell:

    sketched_value = 0
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.width = 100
        self.height = 100

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        valueFont = pygame.font.Font(None, 50)
        valueSurf = valueFont.render(str(self.value), False, (0,0,0), (255,255,255))
        sketchSurf = valueFont.render(str(self.sketched_value), False, (0,0,0), (255,255,255))
        center = (self.col * 100-50, self.row*100-50)
        corner = (self.col * 100-75, self.row*100-75)
        if self.value == 0 and self.sketched_value != 0:
            self.screen.blit(sketchSurf, corner)
        elif self.value != 0:
            self.screen.blit(valueSurf, center)
        if self.selected:
            color = (255, 0, 0)
            pygame.draw.rect(self.screen, color, pygame.rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)
        else:
            color = (0, 0, 0)
            pygame.draw.rect(self.screen, color, pygame.rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)

