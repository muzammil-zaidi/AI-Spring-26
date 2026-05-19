import math

ROWS = 6
COLS = 7

PLAYER = 1
AI = 2

def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    for row in board:
        print(row)
    print()


def is_valid(board, col):
    return board[0][col] == 0


def get_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None


def drop(board, col, piece):
    row = get_row(board, col)
    if row is not None:
        board[row][col] = piece


def check_win(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False


def get_valid_moves(board):
    return [c for c in range(COLS) if is_valid(board, c)]


def evaluate(board):
    if check_win(board, AI):
        return 100
    elif check_win(board, PLAYER):
        return -100
    return 0


def minimax(board, depth, is_max):
    if depth == 0 or check_win(board, PLAYER) or check_win(board, AI):
        return evaluate(board)

    valid_moves = get_valid_moves(board)

    if is_max:
        best = -math.inf
        for col in valid_moves:
            temp = [row[:] for row in board]
            drop(temp, col, AI)
            best = max(best, minimax(temp, depth - 1, False))
        return best

    else:
        best = math.inf
        for col in valid_moves:
            temp = [row[:] for row in board]
            drop(temp, col, PLAYER)
            best = min(best, minimax(temp, depth - 1, True))
        return best


def best_move(board):
    best_score = -math.inf
    move = 0

    for col in get_valid_moves(board):
        temp = [row[:] for row in board]
        drop(temp, col, AI)

        score = minimax(temp, 3, False)

        if score > best_score:
            best_score = score
            move = col

    return move


board = create_board()

while True:
    print_board(board)

    col = int(input("Player move (0-6): "))
    if is_valid(board, col):
        drop(board, col, PLAYER)

    if check_win(board, PLAYER):
        print_board(board)
        print("You Win!")
        break

    ai_col = best_move(board)
    drop(board, ai_col, AI)
    print("AI played:", ai_col)

    if check_win(board, AI):
        print_board(board)
        print("AI Wins!")
        break
