#Ultimate Tic tac toe v2
import random

# Constants
X = "X"
O = "O"
EMPTY = " "
BOARD_SIZE = 9
ORLIN_GAMBIT_MOVES = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2)]
game_over = False
next_board_row = None
next_board_col = None
current_player = X
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]


def print_board():
    print("Current Board:")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")
            if col % 3 == 2 and col != BOARD_SIZE - 1:
                print("|", end=" ")
        print()
        if row % 3 == 2 and row != BOARD_SIZE - 1:
            print("-" * (BOARD_SIZE * 2 - 1))


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

    if board[start_row + 2][start_col] == board[start_row + 1][start_col + 1] == board[start_row][start_col + 2] != EMPTY:
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
    if next_board_row is None:
        return random.choice(ORLIN_GAMBIT_MOVES)
    else:
        for move in ORLIN_GAMBIT_MOVES:
            row = move[0] + next_board_col * 3
            col = move[1] + next_board_row * 3
            if valid_move(row, col):
                return row, col


def get_best_move():
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if valid_move(row, col):
                board[row][col] = current_player

                score = alpha_beta_pruning(board, alpha, beta, False)
                board[row][col] = EMPTY

                if score > alpha:
                    alpha = score
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

    while not game_over:
        print_board()

        if current_player == X:
            print("Player X:")
            row = int(input("Enter row (0-8): "))
            col = int(input("Enter column (0-8): "))

            if make_move(row, col):
                if check_winner(row // 3 * 3, col // 3 * 3):
                    print_board()
                    print("Player X wins!")
                    game_over = True
                elif check_game_over():
                    print_board()
                    print("It's a tie!")
                    game_over = True
                else:
                    if board[col // 3][row // 3] != EMPTY:
                        next_board_row, next_board_col = None, None
                    else:
                        next_board_row, next_board_col = col % 3, row % 3
            else:
                print("Invalid move! Try again.")
                continue
        else:
            print("AI player ({}):".format(current_player))
            if next_board_row is None:
                row, col = apply_orlin_gambit()
            else:
                row, col = get_best_move()
            make_move(row, col)
            if check_winner(row // 3 * 3, col // 3 * 3):
                print_board()
                print("Player O wins!")
                game_over = True
            if board[col // 3][row // 3] != EMPTY:
                next_board_row, next_board_col = None, None
            else:
                next_board_row, next_board_col = col % 3, row % 3

        switch_players()


if __name__ == "__main__":
    main()
