#com problemas a partir do segundo movimento da IA
import pygame
import random

# Constants
X = "X"
O = "O"
EMPTY = " "
BOARD_SIZE = 9
ORLIN_GAMBIT_MOVES = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2)]

# Pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (600, 600)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Ultimate Tic-Tac-Toe")

# Set up the fonts
FONT_SIZE = 50
font = pygame.font.Font(None, FONT_SIZE)

# Calculate cell dimensions
CELL_SIZE = WINDOW_SIZE[0] // BOARD_SIZE

# Variables
game_over = False
next_board_row = None
next_board_col = None
current_player = X
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]


def draw_board():
    window.fill(BLACK)

    # Draw board grid lines
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(window, WHITE, (0, i * CELL_SIZE), (WINDOW_SIZE[0], i * CELL_SIZE))
        pygame.draw.line(window, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE[1]))

    # Draw X's and O's
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell_x = col * CELL_SIZE
            cell_y = row * CELL_SIZE

            if board[row][col] == X:
                pygame.draw.line(window, RED, (cell_x, cell_y), (cell_x + CELL_SIZE, cell_y + CELL_SIZE), 3)
                pygame.draw.line(window, RED, (cell_x + CELL_SIZE, cell_y), (cell_x, cell_y + CELL_SIZE), 3)
            elif board[row][col] == O:
                pygame.draw.circle(window, BLUE, (cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2), CELL_SIZE // 2 - 5, 3)

    pygame.display.flip()


def make_move(row, col):
    if valid_move(row, col):
        board[row][col] = current_player
        return True
    return False


def valid_move(row, col):
    if board[row][col] == EMPTY and (next_board_row is None or
                                     (row // 3 == next_board_row and col // 3 == next_board_col)):
        return True
    return False


def check_winner(start_row, start_col):
    # Check rows
    for row in range(start_row, start_row + 3):
        if board[row][start_col] == board[row][start_col + 1] == board[row][start_col + 2] != EMPTY:
            return True

    # Check columns
    for col in range(start_col, start_col + 3):
        if board[start_row][col] == board[start_row + 1][col] == board[start_row + 2][col] != EMPTY:
            return True

    # Check diagonals
    if board[start_row][start_col] == board[start_row + 1][start_col + 1] == board[start_row + 2][start_col + 2] != EMPTY:
        return True

    if board[start_row][start_col + 2] == board[start_row + 1][start_col + 1] == board[start_row + 2][start_col] != EMPTY:
        return True

    return False


def check_game_over():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY:
                return False
    return True


def switch_players():
    global current_player
    current_player = O if current_player == X else X


def apply_orlin_gambit():
    if len(ORLIN_GAMBIT_MOVES) > 0:
        move = ORLIN_GAMBIT_MOVES.pop(0)
        return move[0], move[1]
    else:
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if valid_move(row, col):
                return row, col


def get_best_move():
    best_score = float('-inf')
    best_move = None

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if valid_move(row, col):
                board[row][col] = X
                score = alpha_beta_pruning(board, float('-inf'), float('inf'), False)
                board[row][col] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move


def alpha_beta_pruning(board, alpha, beta, is_maximizing):
    if check_winner(0, 0) or check_winner(0, 3) or check_winner(0, 6) or \
            check_winner(3, 0) or check_winner(3, 3) or check_winner(3, 6) or \
            check_winner(6, 0) or check_winner(6, 3) or check_winner(6, 6):
        return 1 if is_maximizing else -1
    elif check_game_over():
        return 0

    if is_maximizing:
        max_score = float('-inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if valid_move(row, col):
                    board[row][col] = X

                    score = alpha_beta_pruning(board, alpha, beta, False)
                    board[row][col] = EMPTY

                    max_score = max(max_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return max_score
    else:
        min_score = float('inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if valid_move(row, col):
                    board[row][col] = O

                    score = alpha_beta_pruning(board, alpha, beta, True)
                    board[row][col] = EMPTY

                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return min_score


def main():
    global next_board_row, next_board_col, current_player, game_over

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == X:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE

                if make_move(row, col):
                    next_board_row = row % 3
                    next_board_col = col % 3

                    if check_winner(next_board_row * 3, next_board_col * 3):
                        next_board_row = None
                        next_board_col = None

                    if not game_over:
                        switch_players()

        if current_player == O and not game_over:
            if next_board_row is None or not valid_move(next_board_row, next_board_col):
                next_board_row, next_board_col = apply_orlin_gambit()
            else:
                best_move = get_best_move()
                if best_move is not None:
                    next_board_row, next_board_col = best_move

            if make_move(next_board_row, next_board_col):
                if check_winner(next_board_row * 3, next_board_col * 3):
                    next_board_row = None
                    next_board_col = None

                switch_players()

        draw_board()

        if check_winner(0, 0) or check_winner(0, 3) or check_winner(0, 6) or \
                check_winner(3, 0) or check_winner(3, 3) or check_winner(3, 6) or \
                check_winner(6, 0) or check_winner(6, 3) or check_winner(6, 6):
            game_over = True

        if check_game_over():
            game_over = True

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
