import math, random

import pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


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
        return (
                self.valid_in_row(row, num)
                and self.valid_in_col(col, num)
                and self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num)
        )

    def fill_box(self, row_start, col_start):
        nums = [i for i in range(1, self.row_length + 1)]
        random.shuffle(nums)
        index = 0
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = nums[index]
                index += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
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


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    return sudoku.get_board()


import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.width = 50
        self.height = 50
        self.selected = False

    def get_value(self):
        return self.value

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        font = pygame.font.Font(None, 36)
        cell_color = (0, 0, 0)
        text_color = (0, 0, 0)
        cell_border = (0,0,0)
        sketch_color = (128, 128, 128)
        selected_color = (255, 0, 0)

        x = self.col * self.width
        y = self.row * self.height

        pygame.draw.rect(self.screen, cell_color, (x, y, self.width, self.height), 1)

        if self.selected:
            pygame.draw.rect(self.screen, selected_color, (x, y, self.width, self.height), 3)

        if self.value != 0:
            text = font.render(str(self.value), True, text_color)
            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            text = font.render(str(self.sketched_value), True, sketch_color)
            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            self.screen.blit(text, text_rect)


import sys


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(value=0, row=i, col=j, screen=screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None  # Store the currently selected cell

    def draw(self):
        # Draw Sudoku grid outline with bold lines for 3x3 boxes
        bold_line_thickness = 1
        box_line_thickness = 1

        for i in range(1, 10):
            line_thickness = bold_line_thickness if i % 3 == 0 else box_line_thickness

            # Draw horizontal lines
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.height / 9), (self.width, i * self.height / 9),
                             line_thickness)

            # Draw vertical lines
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.width / 9, 0), (i * self.width / 9, self.height),
                             line_thickness)

        # Draw 3x3 box outlines
        for i in range(1, 3):
            for j in range(1, 3):
                pygame.draw.rect(self.screen, (0, 0, 0), (
                j * self.width / 3 - bold_line_thickness, i * self.height / 3 - bold_line_thickness,
                self.width / 3 + bold_line_thickness, self.height / 3 + bold_line_thickness), bold_line_thickness)

        # Draw each cell on the board
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        # Mark the cell at (row, col) as the current selected cell
        if 0 <= row < 9 and 0 <= col < 9:
            if self.selected_cell:
                self.selected_cell.selected = False  # Deselect the previously selected cell
            self.selected_cell = self.cells[row][col]
            self.selected_cell.selected = True

    def click(self, x, y):
        # Convert mouse click coordinates to row and col indices
        row = int(y / (self.height / 9))
        col = int(x / (self.width / 9))
        return (row, col) if 0 <= row < 9 and 0 <= col < 9 else None

    def clear(self):
        # Clears the value of the current selected cell
        if self.selected_cell:
            if self.selected_cell.value == 0:
                self.selected_cell.set_sketched_value(0)
            else:
                self.selected_cell.set_cell_value(0)

    def sketch(self, value):
        # Sets the sketched value of the current selected cell
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        # Sets the value of the current selected cell
        if self.selected_cell:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        # Reset all cells to their original values
        for row in self.cells:
            for cell in row:
                cell.reset_to_original()

    def is_full(self):
        # Check if the board is full
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        # Update the underlying 2D board with the values in all cells
        for i in range(9):
            for j in range(9):
                self.cells[i][j].update_board()

    def find_empty(self):
        # Find an empty cell and return its row and col as a tuple (x, y)
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return i, j
        return None

    def check_board(self):
        # Check whether the Sudoku board is solved correctly
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False  # There is an empty cell

                # Check if the current cell's value is valid in its row, column, and box
                if not self.is_valid(i, j, self.cells[i][j].value):
                    return False
        return True

    def handle_events(board, sudoku_board):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if 150 <= x <= 300:
                    if 200 <= y <= 250:
                        difficulty = "easy"
                    elif 270 <= y <= 320:
                        difficulty = "medium"
                    elif 340 <= y <= 390:
                        difficulty = "hard"

                    if difficulty:
                        sudoku_board.cells = generate_sudoku(9, {"easy": 30, "medium": 40, "hard": 50}[difficulty])
                        draw_game_screen(screen, sudoku_board)
                        pygame.display.flip()

                # ... (Additional event handling for buttons on the game screen)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    board.handle_enter_key()

                elif event.key == pygame.K_BACKSPACE:
                    board.handle_backspace_key()

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    board.handle_numeric_key(event.key)

                elif event.key == pygame.K_UP:
                    if board.selected_cell:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select((row - 1) % 9, col)

                elif event.key == pygame.K_DOWN:
                    if board.selected_cell:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select((row + 1) % 9, col)

                elif event.key == pygame.K_LEFT:
                    if board.selected_cell:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(row, (col - 1) % 9)

                elif event.key == pygame.K_RIGHT:
                    if board.selected_cell:
                        row, col = board.selected_cell.row, board.selected_cell.col
                        board.select(row, (col + 1) % 9)


def draw_start_screen(screen):
    # Draw the start screen
    font = pygame.font.Font(None, 36)
    text = font.render("Click to Start", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)


def draw_game_screen(screen, sudoku_board):
    # Draw the Sudoku board
    screen.fill((255, 255, 255))  # Fill screen with white background

    # Implement the drawing logic for the Game screen
    # Display the Sudoku board and any other relevant information
    sudoku_board.draw()

    # Add code to draw buttons, messages, or other elements specific to the game screen
    font = pygame.font.Font(None, 24)
    text = font.render('', True, (0, 0, 0))
    screen.blit(text, (20, 20))

    # Update the Sudoku board with the initial values
    for i in range(9):
        for j in range(9):
            value = sudoku_board.cells[i][j].get_value()
            if value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0, 0, 0))
                center = (j * sudoku_board.width // 9 + 35, i * sudoku_board.height // 9 + 35)
                screen.blit(text, center)


def draw_game_over_screen(screen, is_winner):
    # Draw the game over screen
    font = pygame.font.Font(None, 36)
    if is_winner:
        text = font.render("Congratulations! You Win!", True, (0, 0, 0))
    else:
        text = font.render("Game Over. Try Again!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)


def main():
    pygame.init()

    # Set up the screen
    screen_width = 450
    screen_height = 450
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sudoku Game")

    # Create a Sudoku board
    sudoku_board = Board(width=screen_width, height=screen_height, screen=screen, difficulty="easy")

    # Set the initial screen
    current_screen = "start"

    # Game loop
    game_running = False  # Flag to indicate whether the game is in progress
    game_over = False  # Flag to indicate whether the game is over (win or lose)

    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Handle mouse click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_running:
                        # Start the game when clicked on the start screen
                        game_running = True
                        sudoku_board = Board(width=screen_width, height=screen_height, screen=screen, difficulty="easy")
                    else:
                        # Handle click on the game screen
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        clicked_cell = sudoku_board.click(mouse_x, mouse_y)
                        if clicked_cell:
                            sudoku_board.select(*clicked_cell)

                # Handle keyboard input for sketching and placing numbers
                if game_running and not game_over and event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                     pygame.K_8, pygame.K_9]:
                        sudoku_board.place_number(int(pygame.key.name(event.key)))
                    elif event.key == pygame.K_DELETE:
                        sudoku_board.clear()

            # Update logic here (e.g., check if the game is won, update board state)
            if game_running and not game_over:
                # Check if the game is won or lost
                if sudoku_board.is_full() and sudoku_board.check_board():
                    game_over = True  # Player wins
                # You can add more conditions for losing if needed

            # Draw the appropriate screen
            screen.fill((173, 216, 230))  # Fill the screen with white
            if not game_running:
                draw_start_screen(screen)
            elif not game_over:
                draw_game_screen(screen, sudoku_board)
            else:
                draw_game_over_screen(screen, is_winner=True)  # You can set is_winner based on the win condition

            # Update the display
            pygame.display.flip()

            # Set the frame rate
            pygame.time.Clock().tick(60)

        except Exception as e:
            print("Exception in game loop:", e)


if __name__ == "__main__":
    main()
