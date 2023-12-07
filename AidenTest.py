import math, random, pygame
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
        pass
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

def draw_game_start(screen):
    start_title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 70)
    game_option_font = pygame.font.Font(None, 50)

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    return 30
                elif medium_rectangle.collidepoint(event.pos):
                    return 40
                elif hard_rectangle.collidepoint(event.pos):
                    return 50
        pygame.display.update()

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rectangle.collidepoint(event.pos):
                    return
        pygame.display.update()

def draw_game_lost(screen):
    game_won_font = pygame.font.Font(None, 100)
    exit_font = pygame.font.Font(None, 50)
    screen.fill(BG_COLOR)
    game_won_surface = game_won_font.render("Game Over :(", 0, LINE_COLOR)
    game_won_rectangle = game_won_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(game_won_surface, game_won_rectangle)

    restart_text = exit_font.render("Restart", 0, (255, 255, 255))
    restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surface.fill(LINE_COLOR)
    restart_surface.blit(restart_text, (10, 10))
    restart_rectangle = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    screen.blit(restart_surface, restart_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rectangle.collidepoint(event.pos):
                    return
        pygame.display.update()

class Cell:

    def __init__(self, row, col, value, screen):
        self.row = row
        self.col = col
        self.value = value
        self.sketched_value = 0
        self.screen = screen
        self.selected = False

    def set_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.value = value

    def draw(self):
        valueFont = pygame.font.Font(None, 50)
        valueSurf = valueFont.render(str(self.value), False, (0, 0, 0), (255, 255, 255))
        sketchSurf = valueFont.render(str(self.sketched_value), False, (0, 0, 0), (255, 255, 255))
        center = (self.col * 100 - 50, self.row * 100 - 50)
        corner = (self.col * 100 - 75, self.row * 100 - 75)
        if self.value == 0 and self.sketched_value != 0:
            self.screen.blit(sketchSurf, corner)
        elif self.value != 0:
            self.screen.blit(valueSurf, center)
        if self.selected:
            color = (255, 0, 0)
            pygame.draw.rect(self.screen, color,(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)
        else:
            color = (0, 0, 0)
            pygame.draw.rect(self.screen, color,(self.col * 100 - 100, self.row * 100 - 100, self.col * 100, self.row * 100), 3)

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
            self.cells[row][col].set_value(value)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                cell.set_value(0)

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value() == 0:
                    return i, j
        return None

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if not SudokuGenerator.is_valid(i, j, self.cells[i][j].value):
                    return False
        return True


def main()
    WIDTH = 900
    HEIGHT = 900
    BG_COLOR = (255, 255, 255)
    LINE_COLOR = (100, 100, 100)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    difficulty = draw_game_start(screen)
    pygame.display.flip()
    correct_board = SudokuGenerator(9, difficulty)
    game_board = Board(9, 9, screen, difficulty)
    Board.draw(game_board)
    while True:
        Board.draw(game_board)
        posx = 1
        posy = 1
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                cellcol = posx // 100 + 1
                cellrow = posy // 100 + 1
                Board.select(game_board, cellcol, cellrow)
            elif event.type == pygame.KEYDOWN:
                posy -= 1
            elif event.type == pygame.KEYUP:
                posy += 1
            elif event.type == pygame.K_RIGHT:
                posx += 1
            elif event.type == pygame.K_LEFT:
                posx -= 1