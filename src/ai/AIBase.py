from src.Timer import Timer

import chess

class AIBase:
    
    # [getMove] is the only method that needs to be defined in all extending classes.
    # The input is a Board object from the chess module. 
    # See https://python-chess.readthedocs.io/en/latest/core.html#board
    # The output is a tuple consisting of a Move object and a list of strings.
    # See https://python-chess.readthedocs.io/en/latest/core.html#moves
    # The list of strings is for logging AI information in the side panel of the UI.
    # If no logging is desired, an empty list can be returned.
    def getMove(self, board : chess.Board, timer : Timer) -> "tuple[chess.Move, list[str]]":
        pass