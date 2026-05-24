import math

def create_board():
    return {
        "player": [4, 4, 4, 4, 4, 4],
        "ai": [4, 4, 4, 4, 4, 4],
        "store_player": 0,
        "store_ai": 0
    }


def evaluate(state):
    return state["store_ai"] - state["store_player"]


def is_game_over(state):
    return sum(state["player"]) == 0 or sum(state["ai"]) == 0


def make_move(state, side, pit):
    new_state = {
        "player": state["player"][:],
        "ai": state["ai"][:],
        "store_player": state["store_player"],
        "store_ai": state["store_ai"]
    }

    if side == "ai":
        stones = new_state["ai"][pit]
        new_state["ai"][pit] = 0
        new_state["store_ai"] += stones
    else:
        stones = new_state["player"][pit]
        new_state["player"][pit] = 0
        new_state["store_player"] += stones

    return new_state


def minimax(state, depth, is_max):
    if depth == 0 or is_game_over(state):
        return evaluate(state)

    if is_max:
        best = -math.inf
        for i in range(6):
            if state["ai"][i] > 0:
                new_state = make_move(state, "ai", i)
                best = max(best, minimax(new_state, depth-1, False))
        return best

    else:
        best = math.inf
        for i in range(6):
            if state["player"][i] > 0:
                new_state = make_move(state, "player", i)
                best = min(best, minimax(new_state, depth-1, True))
        return best


def best_move(state):
    best_score = -math.inf
    move = 0

    for i in range(6):
        if state["ai"][i] > 0:
            new_state = make_move(state, "ai", i)
            score = minimax(new_state, 3, False)

            if score > best_score:
                best_score = score
                move = i

    return move


state = create_board()

while True:
    print("\nPlayer pits:", state["player"])
    print("AI pits:", state["ai"])
    print("Stores -> Player:", state["store_player"], "AI:", state["store_ai"])

    move = int(input("Pick your pit (0-5): "))
    if state["player"][move] > 0:
        state = make_move(state, "player", move)

    if is_game_over(state):
        break

    ai_move = best_move(state)
    state = make_move(state, "ai", ai_move)
    print("AI played:", ai_move)

    if is_game_over(state):
        break


print("\nGame Over!")
print("Final Score -> Player:", state["store_player"], "AI:", state["store_ai"])

if state["store_ai"] > state["store_player"]:
    print("AI Wins!")
elif state["store_ai"] < state["store_player"]:
    print("You Win!")
else:
    print("Draw!")
