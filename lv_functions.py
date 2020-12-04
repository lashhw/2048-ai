import board as bd
import numpy as np
import ai
import os
import subprocess

zero_list = [[0 for _ in range(4)] for _ in range(4)]

def get_new_board(data_tuple):
    tmp_board = bd.Board()
    for _ in range(2):
        tmp_board.randomly_add_tile()
    return (tmp_board.get_data().tolist(), 0, 0, 0, "")

def randomly_add_tile(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    tmp_board.randomly_add_tile()
    return (tmp_board.get_data().tolist(), 0, 0, 0, "")

def move_up(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    success, score_add = tmp_board.move_up()
    return (tmp_board.get_data().tolist(), success, score_add, 0, "")

def move_left(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    success, score_add = tmp_board.move_left()
    return (tmp_board.get_data().tolist(), success, score_add, 0, "")

def move_down(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    success, score_add = tmp_board.move_down()
    return (tmp_board.get_data().tolist(), success, score_add, 0, "")

def move_right(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    success, score_add = tmp_board.move_right()
    return (tmp_board.get_data().tolist(), success, score_add, 0, "")

def move_by_id(data_tuple):
    return { 0: move_up,
             1: move_down,
             2: move_left,
             3: move_right }[data_tuple[1]](data_tuple)

def is_dead(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    return (tmp_board.get_data().tolist(), tmp_board.is_dead(), 0, 0, "")

def get_optimal_move(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    return (tmp_board.get_data().tolist(), ai.get_optimal_move(tmp_board), 0, 0, "")

def get_move_expected_score(data_tuple):
    tmp_board = bd.Board(np.array(data_tuple[0], dtype="uint8"))
    return ai.get_move_expected_score(tmp_board, data_tuple[1], data_tuple[2], data_tuple[3])

def get_strong_optimal_move(data_tuple):
    board = __to_c_board(data_tuple[0])
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/strong-ai/bin")
    output = subprocess.Popen(["2048.exe", str(board)], stdout=subprocess.PIPE).communicate()[0]
    return (data_tuple[0], int(output.decode("utf-8")), 0, 0, "")

def get_strong_move_expected_score(data_tuple):
    board = __to_c_board(data_tuple[0])
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/strong-ai/bin")
    output = subprocess.Popen(["2048_get_score.exe", str(board), str(data_tuple[1])], stdout=subprocess.PIPE).communicate()[0]
    return float(output.decode("utf-8"))

def get_readable_board(data_tuple):
    converted_np = 2 ** np.array(data_tuple[0], dtype="uint")
    converted_np[converted_np == 1] = 0
    return (converted_np.tolist(), 0, 0, 0, "")

def __to_c_board(board_list):
    board = 0
    i = 0
    for row in board_list:
        for c in row:
            board |= int(c) << (4*i)
            i += 1
    return board