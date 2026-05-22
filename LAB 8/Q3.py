import math

def minimax(n, is_max):
    if n == 0:
        return -1 if is_max else 1

    if is_max:
        best = -math.inf
        for i in [1,2,3]:
            if n - i >= 0:
                best = max(best, minimax(n-i, False))
        return best
    else:
        best = math.inf
        for i in [1,2,3]:
            if n - i >= 0:
                best = min(best, minimax(n-i, True))
        return best

def best_move(n):
    best_val = -math.inf
    move = 1

    for i in [1,2,3]:
        if n - i >= 0:
            val = minimax(n-i, False)
            if val > best_val:
                best_val = val
                move = i

    return move

n = int(input("Enter total objects: "))

while n > 0:
    print("Remaining:", n)
    user = int(input("Take 1-3: "))
    n -= user

    if n == 0:
        print("User wins!")
        break

    ai = best_move(n)
    print("AI takes:", ai)
    n -= ai

    if n == 0:
        print("AI wins!")
        break
