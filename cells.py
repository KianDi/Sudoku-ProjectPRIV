import pygame
class Cell:

    sketched_value = 0
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        center = (self.col * 100-50, self.row*100-50)
        corner = (self.col * 100-75, self.row*100-75)
        if self.value == 0 and self.sketched_value != 0:
            self.screen.blit(self.sketched_value, corner)
        elif self.value != 0:
            self.screen.blit(self.value, center)
        if self.selected:
            color = (255, 0, 0)
            pygame.draw.rect(self.screen, color, pygame.rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)
        else:
            color = (0, 0, 0)
            pygame.draw.rect(self.screen, color, pygame.rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)

