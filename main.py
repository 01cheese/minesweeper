import pygame
import random
import sys
import pygame_menu

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Colors
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
MINE_COLOR = (255, 0, 0)
FLAG_COLOR = (0, 0, 255)
TEXT_COLOR = (0, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)

# Sounds
pygame.mixer.init()
CLICK_SOUND = pygame.mixer.Sound('click.wav')
MINE_SOUND = pygame.mixer.Sound('explosion.wav')


def start_the_game(difficulty='Custom', grid_size=10, mines_count=10):
    if difficulty == 'Easy':
        play_game(10, 10)
    elif difficulty == 'Medium':
        play_game(15, 40)
    elif difficulty == 'Hard':
        play_game(20, 99)
    elif difficulty == 'Custom':
        if grid_size < 5 or grid_size > 50 or mines_count < 1 or mines_count >= grid_size * grid_size:
            show_error_menu()
        else:
            play_game(grid_size, mines_count)


def custom_menu():
    menu = pygame_menu.Menu('Custom Game', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)

    size_input = menu.add.text_input('Custom size: ', default='10', textinput_id='size_input')
    mines_input = menu.add.text_input('Custom mines: ', default='10', textinput_id='mines_input')
    menu.add.button('Play',
                    lambda: start_the_game('Custom', int(size_input.get_value()), int(mines_input.get_value())))
    menu.add.button('Back to Main Menu', main_menu)

    menu.mainloop(WIN)


def show_error_menu():
    menu = pygame_menu.Menu('Error', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)
    menu.add.label('Invalid size or number of mines.')
    menu.add.label('Size must be between 5 and 50.')
    menu.add.label('Mines must be at least 1 and less than size*size.')
    menu.add.button('Back', custom_menu)
    menu.mainloop(WIN)


def main_menu():
    menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Play Easy', start_the_game, 'Easy')
    menu.add.button('Play Medium', start_the_game, 'Medium')
    menu.add.button('Play Hard', start_the_game, 'Hard')
    menu.add.button('Custom Game', custom_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(WIN)


def play_game(grid_size, mines_count):
    cell_size = WIDTH // grid_size

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    mines = set()
    revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    flags = [[False for _ in range(grid_size)] for _ in range(grid_size)]

    def place_mines():
        while len(mines) < mines_count:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                grid[x][y] = -1

    def calculate_numbers():
        for x, y in mines:
            for i in range(max(0, x - 1), min(grid_size, x + 2)):
                for j in range(max(0, y - 1), min(grid_size, y + 2)):
                    if grid[i][j] != -1:
                        grid[i][j] += 1

    def draw_grid():
        for i in range(grid_size):
            for j in range(grid_size):
                rect = pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size)
                pygame.draw.rect(WIN, BG_COLOR, rect)
                pygame.draw.rect(WIN, LINE_COLOR, rect, 1)
                if revealed[i][j]:
                    if grid[i][j] == -1:
                        pygame.draw.circle(WIN, MINE_COLOR, rect.center, cell_size // 4)
                    elif grid[i][j] > 0:
                        text = FONT.render(str(grid[i][j]), True, TEXT_COLOR)
                        WIN.blit(text, (i * cell_size + 10, j * cell_size + 5))
                    else:
                        pygame.draw.rect(WIN, (200, 200, 200), rect)
                elif flags[i][j]:
                    pygame.draw.circle(WIN, FLAG_COLOR, rect.center, cell_size // 4)

    def reveal(x, y):
        if revealed[x][y] or flags[x][y]:
            return
        revealed[x][y] = True
        CLICK_SOUND.play()
        if grid[x][y] == -1:
            MINE_SOUND.play()
            game_over()
            return
        if grid[x][y] == 0:
            for i in range(max(0, x - 1), min(grid_size, x + 2)):
                for j in range(max(0, y - 1), min(grid_size, y + 2)):
                    if not revealed[i][j]:
                        reveal(i, j)
        if check_win():
            win()

    def flag(x, y):
        if revealed[x][y]:
            return
        flags[x][y] = not flags[x][y]

    def check_win():
        for i in range(grid_size):
            for j in range(grid_size):
                if not revealed[i][j] and grid[i][j] != -1:
                    return False
        return True

    def game_over():
        for i in range(grid_size):
            for j in range(grid_size):
                if grid[i][j] == -1:
                    revealed[i][j] = True
        draw_grid()
        pygame.display.update()
        pygame.time.wait(2000)
        show_congratulations_menu("Game Over")

    def win():
        draw_grid()
        pygame.display.update()
        pygame.time.wait(2000)
        show_congratulations_menu("You Win!")

    place_mines()
    calculate_numbers()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // cell_size, event.pos[1] // cell_size
                if event.button == 1:
                    reveal(x, y)
                elif event.button == 3:
                    flag(x, y)

        WIN.fill(BG_COLOR)
        draw_grid()
        pygame.display.update()

    pygame.quit()
    sys.exit()


def show_congratulations_menu(message):
    menu = pygame_menu.Menu(message, WIDTH, HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Back to Main Menu', main_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN)


if __name__ == "__main__":
    main_menu()
