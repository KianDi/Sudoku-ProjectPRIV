import pygame, sys
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
    easy_rectangle = easy_surface.get_rect(center = (WIDTH // 3, HEIGHT // 2 + 150))
    medium_rectangle = medium_surface.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 150))
    hard_rectangle = hard_surface.get_rect(center=(WIDTH // 1.5, HEIGHT // 2 + 150))

    screen.blit(button_surface, button_rectangle)
    screen.blit(easy_surface, easy_rectangle)
    screen.blit(medium_surface, medium_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    return
                elif medium_rectangle.collidepoint(event.pos):
                    return
                elif hard_rectangle.collidepoint(event.pos):
                    return
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


WIDTH = 900
HEIGHT = 900
BG_COLOR = (255, 255, 255)
LINE_COLOR = (100, 100, 100)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
#draw_game_start(screen)
#draw_game_won(screen)
#draw_game_lost(screen)
