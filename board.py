import pygame
from cells import Cell

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, i, j, self.screen) for j in range(9)] for i in range(9)]
        self.picked_cell = None

    def draw(self):

        for i in range(1, 10):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width // 9, 0), (i * self.width // 9, self.height),
                             width)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height // 9), (self.width, i * self.height // 9),
                             width)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if 0 <= row < 9 and 0 <= col < 9:
            self.picked_cell = (row, col)

    def click(self, x, y):
        row = y // (self.height // 9)
        col = x // (self.width // 9)
        return (row, col) if 0 <= row < 9 and 0 <= col < 9 else None

    def clear(self):
        if self.picked_cell:
            row, col = self.picked_cell
            self.cells[row][col].clear()

    def sketch(self, value):
        if self.picked_cell:
            row, col = self.picked_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.picked_cell:
            row, col = self.picked_cell
            self.cells[row][col].set_cell_value(value)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.reset_to_original()

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.get_value() == 0:
                    return False
        return True

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].update_value()

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get_value() == 0:
                    return i, j
        return None

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if not self.cells[i][j].is_valid():
                    return False
        return True

