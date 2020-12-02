import board as bd
import constants as c
import numpy as np
import math
import random

def get_optimal_move(board):
    expected_score = np.zeros((4), dtype="int")
    for i in range(4):
        expected_score[i] = get_expected_score(board, i)
    print(expected_score)
    return np.argmax(expected_score)

def get_expected_score(board, move_id):
    expected_score = 0
    # first move
    first_move_board = bd.Board(board.get_data())
    success, score_add = first_move_board.move_by_id(move_id)
    if not success:
        return 0
    else:
        expected_score += score_add
        first_move_board.randomly_add_tile()
    # simulations (random move)
    for _ in range(c.SIMULATIONS_PER_MOVE):
        tmp_board = bd.Board(first_move_board.get_data())
        for _ in range(c.MAX_SIMULATION_DEPTH):
            try_move_ids = random.sample(range(4), 4)
            has_move = False
            for j in try_move_ids:
                success, score_add = tmp_board.move_by_id(j)
                if (success):
                    expected_score += score_add
                    tmp_board.randomly_add_tile()
                    has_move = True
                    break
            if not has_move:
                break
    return expected_score