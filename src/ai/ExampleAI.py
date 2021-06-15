from random import randint
from src.ai.AIBase import AIBase

import chess

class ExampleAI(AIBase):

    def __init__(self):
        pass

    def getMove(self, board : chess.Board) -> tuple[chess.Move, list[str]]:
        possibleMoves = list(board.legal_moves)
        randomMove = possibleMoves[randint(0, len(possibleMoves) - 1)]
        logMessage = [
            "This is a random move.", 
            "It probably isn't very good.",
            board.san(randomMove)
        ]
        return randomMove, logMessage