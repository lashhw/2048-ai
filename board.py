import numpy as np
import constants as c
import random

class Board():
    def __init__(self, data = np.zeros((c.GAME_SIZE, c.GAME_SIZE), dtype="uint8")):
        self.__data = data

    def randomly_add_tile(self):
        possible_selections = np.where(self.__data == 0)
        possible_selections_count = len(possible_selections[0])
        if possible_selections_count == 0:
            return
        random_index = random.randint(0, possible_selections_count - 1)
        to_addr = possible_selections[0][random_index]
        to_addc = possible_selections[1][random_index]
        self.__data[to_addr][to_addc] = 1 if random.random() <= 0.9 else 2

    def __stack_left(self):
        tmp_data = np.zeros((c.GAME_SIZE, c.GAME_SIZE), dtype="uint8")
        success = False
        for i in range(c.GAME_SIZE):
            col = 0
            for j in range(c.GAME_SIZE):
                if self.__data[i][j] != 0:
                    tmp_data[i][col] = self.__data[i][j]
                    if col != j:
                        success = True
                    col += 1
        self.__data = tmp_data
        return success

    def __merge_left(self):
        score_add = 0
        success = False
        for i in range(c.GAME_SIZE):
            for j in range(c.GAME_SIZE - 1):
                if self.__data[i][j] == self.__data[i][j + 1] and self.__data[i][j] != 0:
                    self.__data[i][j] += 1
                    score_add += (1 << self.__data[i][j])
                    self.__data[i][j + 1] = 0
                    success = True
        return success, score_add
    
    def move_left(self):
        stack_success = self.__stack_left()
        merge_success, score_add = self.__merge_left()
        self.__stack_left()
        return (stack_success or merge_success), score_add

    def move_right(self):
        self.__data = np.flip(self.__data, 1)
        success, score_add = self.move_left()
        self.__data = np.flip(self.__data, 1)
        return success, score_add

    def move_up(self):
        self.__data = np.rot90(self.__data)
        success, score_add = self.move_left()
        self.__data = np.rot90(self.__data, 3)
        return success, score_add

    def move_down(self):
        self.__data = np.rot90(self.__data, 3)
        success, score_add = self.move_left()
        self.__data = np.rot90(self.__data)
        return success, score_add

    def move_by_id(self, move_id):
        return { 0: self.move_up,
                 1: self.move_left,
                 2: self.move_down,
                 3: self.move_right }[move_id]()

    def is_dead(self):
        if 0 in self.__data:
            return False
        for i in range(4):
            try_board = Board(self.__data)
            success, _ = try_board.move_by_id(i)
            if success:
                return False
        return True
    
    def get_data(self):
        return self.__data
            
    
    def print(self):
        data_converted = 2 ** self.__data.astype('uint')
        data_converted[data_converted == 1] = 0
        for i in range(c.GAME_SIZE):
            for j in range(c.GAME_SIZE):
                print("[%5s]" % data_converted[i][j], end=" ")
            print()