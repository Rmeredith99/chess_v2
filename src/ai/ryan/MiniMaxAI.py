from enum import auto
from random import uniform
from src.ai.AIBase import AIBase
from src.ai.ryan.AiUtil import AiUtil
from time import time
from src.Timer import Timer

import chess

class MiniMaxAI(AIBase):

    def __init__(self, depth : int):
        self.depth = depth
        self.evalFunction = AiUtil.pieceEvaluationScore

    def getMove(self, board : chess.Board, timer : Timer) -> "tuple[chess.Move, list[str]]":
        startTime = time()
        bestValue = -10000
        bestMove = None
        valueModifier = 1 if board.turn == chess.WHITE else -1
        for move in board.legal_moves:
            board.push(move)
            value = AiUtil.minimax(board, self.depth, self.evalFunction) * valueModifier
            _ = board.pop()
            if value + uniform(0, 0.005) > bestValue:
                bestMove = move
                bestValue = value

        log = [
            "Minimax AI:",
            "Depth: " + str(self.depth),
            "Chosen Move: " + board.san(bestMove),
            "Score: " + str(bestValue * valueModifier),
            "Time Elapsed: " + str(time() - startTime)[:5] + " seconds",
            "Nodes Checked: " + str(AiUtil.nodesChecked)
        ]

        AiUtil.nodesChecked = 0

        return (bestMove, log)
