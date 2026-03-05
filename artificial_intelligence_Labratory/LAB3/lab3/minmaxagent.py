from exceptions import AgentException
from connect4 import Connect4
from copy import deepcopy
from typing import Tuple


class MinMaxAgent:
    def __init__(self, my_token, d=5):
        self.my_token = my_token
        self.d = d

    def decide(self, board: 'Connect4') -> list[int]:
        if board.who_moves != self.my_token:
            raise AgentException('Not my move')
        _, move = self.minmax(board, 1, self.d)
        return move

    def minmax(self, board: 'Connect4', x: int, d: int) -> Tuple[int, int]:
        #zwyciestwo
        if board.game_over and board.wins == self.my_token:
            return float('inf'), -1
        #remis
        if board.game_over and board.wins == None:
            return 0, -1
        #przegrana
        if board.game_over and board.wins != self.my_token:
            return float('-inf'), -1

        if d == 0:
            return 0, -1

        if x == 1:
            best_score = float('-inf')
        else:
            best_score = float('inf')
        best_move = 3
        for possible_move in board.possible_drops():
            simulation = deepcopy(board)
            simulation.drop_token(possible_move)
            if x == 1:
                score, _ = self.minmax(simulation, 0, d - 1)
                if score > best_score:
                    best_score = score
                    best_move = possible_move
            else:
                score, _ = self.minmax(simulation, 1, d - 1)
                if score < best_score:
                    best_score = score
                    best_move = possible_move
        return [best_score, best_move]

