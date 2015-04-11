import random

def think(state, quip):
    moves = state.get_moves()
    maxSet = []     # maxSet is the set of all moves that maximize score in the next turn.
    maxScore = 0
    
    # Compute maximum possible score
    for i in moves:
        simState = state.copy()
        simState.apply_move(i)
        score = simState.get_score()[simState.get_whos_turn()]
        if score > maxScore:
            maxScore = score

    # Copy all moves that produce a maximum score into maxSet
    for i in moves:
        simState = state.copy()
        simState.apply_move(i)
        score = simState.get_score()[simState.get_whos_turn()]
        if score == maxScore:
            maxSet.append(i)

    move = random.choice(maxSet)
    return move