import math

board = [" "] * 9

def print_board():
    for i in range(0, 9, 3):
        print(board[i], board[i+1], board[i+2])
    print()

def check_winner(b, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(b[a]==b[b1]==b[c]==player for a,b1,c in wins)

def is_full():
    return " " not in board

def minimax(b, is_max):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if " " not in b:
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = max(best, minimax(b, False))
                b[i] = " "
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                best = min(best, minimax(b, True))
                b[i] = " "
        return best

def best_move():
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            val = minimax(board, False)
            board[i] = " "
            if val > best_val:
                best_val = val
                move = i
    return move

while True:
    print_board()
    pos = int(input("Enter position (0-8): "))
    board[pos] = "X"

    if check_winner(board, "X"):
        print_board()
        print("You win!")
        break

    if is_full():
        print("Draw!")
        break

    ai = best_move()
    board[ai] = "O"

    if check_winner(board, "O"):
        print_board()
        print("AI wins!")
        break
