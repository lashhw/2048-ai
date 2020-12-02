import numpy as np
import constants as c
import board as bd
import ai
import time

class Game():
    def __init__(self):
        self.board = bd.Board()
        for _ in range(2):
            self.board.randomly_add_tile()
        self.score = 0

    def start_interactively(self):
        while True: 
            self.print()
            if self.board.is_dead():
                break
            key_entered = input()
            if key_entered == "e":
                break
            direction_keys = { "w": self.board.move_up,
                               "a": self.board.move_left,
                               "s": self.board.move_down,
                               "d": self.board.move_right }
            if key_entered in direction_keys.keys():
                _, add_score = direction_keys[key_entered]()
                self.score += add_score
                self.board.randomly_add_tile()
    
    def perform_move(self, move_id):
        _, add_score = self.board.move_by_id(move_id)
        self.score += add_score

    def print(self):
        print("----------")
        print("Score:", self.score)
        self.board.print()



def main():
    g = Game()
    # g.start_interactively()
    for x in range(10000):
        g.print()
        if g.board.is_dead():
            print(x, "No possible move.")
            break
        start = time.perf_counter()
        optimal_move = ai.get_optimal_move(g.board)
        end = time.perf_counter()
        print(c.MOVE_ID_DICT[optimal_move], round(end - start, 2))
        g.perform_move(optimal_move)
        g.board.randomly_add_tile()

if __name__ == "__main__":
    main()