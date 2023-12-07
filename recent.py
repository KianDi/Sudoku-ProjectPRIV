import pygame
import sys
import math
import random

# Cell class
class Cell:
    sketched_value = 0

    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def set_cell_value(self, value):
        if isinstance(value, int):  # Check if the value is an integer
            font = pygame.font.Font(None, 60)  # You can adjust the font size as needed
            if value == 0:
                self.value = None  # Treat 0 as an empty cell
            else:
                self.value = font.render(str(value), True, (0, 0, 0))
                self.draw()

        else:
            self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        center = ((self.col + 1) * 100 - 50, (self.row + 1) * 100 - 50)
        corner = (self.col * 100 - 75, self.row * 100 - 75)


        # Draw the red outline for the selected cell
        if self.selected:

            pygame.draw.rect(self.screen, (255, 0, 0),
                             pygame.Rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)

        if self.value == 0 and self.sketched_value != 0:
            self.screen.blit(self.sketched_value, corner)
        elif self.value is not None:
            #print("entered draw")
            self.screen.blit(self.value, center)
        elif self.value is None:
            color = (255, 255, 255)  # White color for empty cells
            pygame.draw.rect(self.screen, color,
                             pygame.Rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100))

        # Draw the border for the cell
        if self.selected:
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)
class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [row[col] for row in self.board]

    def valid_in_box(self, row_start, col_start, num):
        for i in range(self.box_length):
            for j in range(self.box_length):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return(self.valid_in_row(row, num) and self.valid_in_col(col, num)
               and self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num))

    def fill_box(self, row_start, col_start):
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        count = 0
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = numbers[count]
                count += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    @classmethod
    def generate_sudoku(cls, size, removed):
        sudoku = cls(size, removed)
        sudoku.fill_values()
        sudoku.remove_cells()
        return sudoku.get_board()

# Board class
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

    def move_selection(self, dx, dy):
        if self.picked_cell:
            row, col = self.picked_cell
            new_row, new_col = row + dy, col + dx
            if 0 <= new_row < 9 and 0 <= new_col < 9:
                self.picked_cell = (new_row, new_col)


# Constants
WIDTH = 900
HEIGHT = 900
BG_COLOR = (255, 255, 255)
LINE_COLOR = (100, 100, 100)

# Function to draw the game start screen
def draw_game_start(screen):

    start_title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 70)
    game_option_font = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_rectangle.collidepoint(x, y):

                    start_sudoku("easy", screen)
                    pygame.display.flip()
                    return
                elif medium_rectangle.collidepoint(x, y):
                    start_sudoku("medium", screen)
                    return
                elif hard_rectangle.collidepoint(x, y):
                    start_sudoku("hard", screen)

        screen.fill(BG_COLOR)
        title_surface = start_title_font.render("Welcome to Sudoku", 0, LINE_COLOR)
        title_rectangle = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        screen.blit(title_surface, title_rectangle)
        button_text = button_font.render("Select Game Mode:", 0, (255, 255, 255))
        easy_text = game_option_font.render("Easy", 0, (255, 255, 255))
        medium_text = game_option_font.render("Medium", 0, (255, 255, 255))
        hard_text = game_option_font.render("Hard", 0, (255, 255, 255))

        button_surface = pygame.Surface((button_text.get_size()[0] + 20, button_text.get_size()[1] + 20))
        button_surface.fill(LINE_COLOR)
        button_surface.blit(button_text, (10, 10))

        easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
        easy_surface.fill(LINE_COLOR)
        easy_surface.blit(easy_text, (10, 10))

        medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
        medium_surface.fill(LINE_COLOR)
        medium_surface.blit(medium_text, (10, 10))

        hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
        hard_surface.fill(LINE_COLOR)
        hard_surface.blit(hard_text, (10, 10))

        button_rectangle = button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        easy_rectangle = easy_surface.get_rect(center=(WIDTH // 3, HEIGHT // 2 + 150))
        medium_rectangle = medium_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        hard_rectangle = hard_surface.get_rect(center=(WIDTH // 1.5, HEIGHT // 2 + 150))

        screen.blit(button_surface, button_rectangle)
        screen.blit(easy_surface, easy_rectangle)
        screen.blit(medium_surface, medium_rectangle)
        screen.blit(hard_surface, hard_rectangle)

        pygame.display.flip()

# Function to draw the game won screen
def draw_game_won(screen):
    game_won_font = pygame.font.Font(None, 100)
    exit_font = pygame.font.Font(None, 50)
    screen.fill(BG_COLOR)
    game_won_surface = game_won_font.render("Game Won!", 0, LINE_COLOR)
    game_won_rectangle = game_won_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(game_won_surface, game_won_rectangle)

    exit_text = exit_font.render("Exit", 0, (255, 255, 255))
    exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surface.fill(LINE_COLOR)
    exit_surface.blit(exit_text, (10, 10))
    exit_rectangle = exit_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    screen.blit(exit_surface, exit_rectangle)

# Function to start Sudoku
def start_sudoku(difficulty, screen):
    screen.fill((255, 255, 255))
    pygame.init()
    pygame.display.set_caption("Sudoku")

    # Initialize the Board
    sudoku_board = Board(WIDTH, HEIGHT, screen, difficulty)

    # Generate Sudoku board based on difficulty
    if difficulty == "easy":
        removed_cells = 12  # Adjust the number of removed cells based on the difficulty level
    elif difficulty == "medium":
        removed_cells = 40
    elif difficulty == "hard":
        removed_cells = 50

    sudoku_values = SudokuGenerator.generate_sudoku(9, removed_cells)

    # Set the values of the cells in the Board instance
    for i in range(9):
        for j in range(9):
            cell_value = sudoku_values[i][j]
            sudoku_board.cells[i][j].set_cell_value(cell_value)

    # Draw the initial state of the Sudoku board
    sudoku_board.draw()
    pygame.display.flip()

    # Initial selection
    selected_row, selected_col = 0, 0
    sudoku_board.select(selected_row, selected_col)

    # Continue your game loop or handle user input as needed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                selected_row, selected_col = sudoku_board.click(x, y)
                print(selected_row, selected_col)
                sudoku_board.select(selected_row, selected_col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    sudoku_board.clear()
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    sudoku_board.place_number(int(event.unicode))
                elif event.key == pygame.K_UP:
                    selected_row = (selected_row - 1) % 9
                    sudoku_board.select(selected_row, selected_col)
                elif event.key == pygame.K_DOWN:
                    selected_row = (selected_row + 1) % 9
                    sudoku_board.select(selected_row, selected_col)
                elif event.key == pygame.K_LEFT:
                    selected_col = (selected_col - 1) % 9
                    sudoku_board.select(selected_row, selected_col)
                elif event.key == pygame.K_RIGHT:
                    selected_col = (selected_col + 1) % 9
                    sudoku_board.select(selected_row, selected_col)

        pygame.display.update()

# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    draw_game_start(screen)
