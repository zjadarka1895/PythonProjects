from exceptions import AgentException
from connect4 import Connect4
from copy import deepcopy
from typing import Tuple


class AlphaBetaAgent:
    def __init__(self, my_token, d=5):
        self.my_token = my_token
        self.d = d

    def decide(self, board: 'Connect4') -> list[int]:
        if board.who_moves != self.my_token:
            raise AgentException('Not my move')
        _, move = self.alphabeta(board, True, self.d, float('-inf'), float('inf'))
        return move

    def heuristic(self, board, move):
        # HEURYSTYKA
        bonus = 0
        if (board.find_n_with_move(move, 3)):
            bonus += 12
        elif (board.find_enemys_three(move)):
            bonus += 8
        elif (board.find_n_with_move(move, 2)):
            bonus += 4
        bonus += 3 - abs(move - 3)
        return bonus

    def decide(self, board: 'Connect4') -> list[int]:
        if board.who_moves != self.my_token:
            raise AgentException('Not my move')
        _, move = self.alphabeta(board, True, self.d, float('-inf'), float('inf'))
        if move not in board.possible_drops():
            raise AgentException(f'Chosen invalid move: {move}')
        return move

    def alphabeta(self, board, x: int, d, alpha, beta):
        if board.game_over:
            if board.wins == self.my_token:
                return 10000, -1
            elif board.wins is None:
                return 0, -1
            else:
                return -10000, -1

        if d == 0:
            return self.heuristic(board, -1), -1

        best_move=board.possible_drops()[0]
        if x == 1:
            best_score = float('-inf')
            for move in board.possible_drops():
                simulation = deepcopy(board)
                simulation.drop_token(move)
                score, _ = self.alphabeta(simulation, 0, d - 1, alpha, beta)
                #score += self.heuristic(simulation, move)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break

        else:
            best_score = float('inf')
            for move in board.possible_drops():
                simulation = deepcopy(board)
                simulation.drop_token(move)
                score, _ = self.alphabeta(simulation, 1, d - 1, alpha, beta)
                #score -= self.heuristic(simulation, move)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best_score, best_move


"""
        if maximizing_player:
            best_score = float('-inf')
            best_move = board.possible_drops()[0]
            for move in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(move)
                score, _ = self.alphabeta(new_board, False, d - 1, alpha, beta)
                score += self.heuristic(new_board, move)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

        else:
            best_score = float('inf')
            best_move = board.possible_drops()[0]
            for move in board.possible_drops():
                new_board = deepcopy(board)
                new_board.drop_token(move)
                score, _ = self.alphabeta(new_board, True, d - 1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move
        """


