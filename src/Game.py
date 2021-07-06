from random import randint
from src.ai.ExampleAI import ExampleAI
from src.ai.ryan.MiniMaxAI import MiniMaxAI
from src.Constants import Constants
from src.ui.Gui import Gui
from src.Timer import Timer

import chess
import pygame

class Game:

    def __init__(self) -> None:
        self.run = True
        self.board = chess.Board()
        self.gameOver = True
        self.gameOverStatus = None
        self.gameOverReason = None
        self.gui = Gui()
        self.timer = Timer(0.5, 0)
        self.players = 2
        self.humanColor = None
        self.halfTurnNumber = 1
        self.whiteOrientation = True
        self.promotionPending = False
        self.promotionPiece = None
        self.checkSquare = None
        self.aiLogs = []

        self.startSquare = None
        self.endSquare = None
        self.changed = True
        self.lastMoveStart = None
        self.lastMoveEnd = None
        self.lastMoves = []

        self.newGameScreen = True
        self.gameOverScreen = False

        # Change AI instantiation here to swap out AIs
        self.aiWhite = MiniMaxAI(2)
        self.aiBlack = ExampleAI()

    def play(self) -> None:
        while self.run:
            if self.__isComputerTurn() and not self.gameOver:
                if self.board.turn == chess.WHITE:
                    move, log = self.aiWhite.getMove(self.board, self.timer)
                else:
                    move, log = self.aiBlack.getMove(self.board, self.timer)
                self.timer.updateTime(self.board.turn)
                self.aiLogs.append(log)
                self.board.push(move)
                if self.lastMoveStart != None and self.lastMoveEnd != None:
                    self.lastMoves.append((self.lastMoveStart, self.lastMoveEnd))
                self.lastMoveStart = move.from_square
                self.lastMoveEnd = move.to_square
                self.halfTurnNumber += 1
                self.changed = True

                if self.board.is_check():
                    checkSquareSet = self.board.pieces(chess.KING, self.board.turn)
                    self.checkSquare = checkSquareSet.pop()
                else:
                    self.checkSquare = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    xPosition, yPosition = pygame.mouse.get_pos()

                    if self.gui.handleContainerClick(self, xPosition, yPosition):
                        self.changed = True
                    elif not self.promotionPending and not self.gameOver:
                        square = self.__getSquareFromCoordinates(xPosition, yPosition, self.whiteOrientation)

                        if self.startSquare == None:
                            if self.board.piece_at(square):
                                self.startSquare = square
                                self.changed = True
                        elif self.endSquare == None:
                            self.endSquare = square

                        if self.startSquare != None and self.endSquare != None:
                            if self.startSquare == self.endSquare:
                                self.startSquare = None
                                self.endSquare = None
                                self.changed = True
                            else:
                                try:
                                    move = self.board.find_move(self.startSquare, self.endSquare)
                                except:
                                    move = chess.Move(self.startSquare, self.endSquare)

                                if move.promotion != None:
                                    self.promotionPending = True
                                elif move in self.board.legal_moves:
                                    self.timer.updateTime(self.board.turn)
                                    self.board.push(move)
                                    if self.lastMoveStart != None and self.lastMoveEnd != None:
                                        self.lastMoves.append((self.lastMoveStart, self.lastMoveEnd))
                                    self.lastMoveStart = self.startSquare
                                    self.lastMoveEnd = self.endSquare
                                    self.halfTurnNumber += 1
                                else:
                                    print(move.uci() + " is not a valid move.")
                                self.startSquare = None
                                self.endSquare = None
                                self.changed = True

                    if self.promotionPending and self.promotionPiece != None:
                        move.promotion = self.promotionPiece
                        self.timer.updateTime(self.board.turn)
                        self.board.push(move)
                        if self.lastMoveStart != None and self.lastMoveEnd != None:
                            self.lastMoves.append((self.lastMoveStart, self.lastMoveEnd))
                        self.lastMoveStart = move.from_square
                        self.lastMoveEnd = move.to_square
                        self.halfTurnNumber += 1
                        self.promotionPiece = None
                        self.promotionPending = False
                        self.changed = True

                    if self.board.is_check():
                        checkSquareSet = self.board.pieces(chess.KING, self.board.turn)
                        self.checkSquare = checkSquareSet.pop()
                    else:
                        self.checkSquare = None

            if (color := self.timer.isOutOfTime() != None and not self.gameOver):
                self.gameOver = True
                self.gameOverStatus = not color
                self.gameOverReason = "No Time Remaining"
                self.gameOverScreen = True

            # Check for board-based game over. Avoid this logic for UI-based game over (i.e. resign button).
            if self.board.is_game_over() and not self.gameOver:
                self.gameOver = True
                self.gameOverStatus = self.board.outcome().winner
                self.gameOverScreen = True
                termination = self.board.outcome().termination
                if termination == chess.Termination.CHECKMATE:
                    self.gameOverReason = "Checkmate"
                elif termination == chess.Termination.STALEMATE:
                    self.gameOverReason = "Stalemate"
                elif termination == chess.Termination.INSUFFICIENT_MATERIAL:
                    self.gameOverReason = "Insufficient Material"
                elif termination == chess.Termination.SEVENTYFIVE_MOVES:
                    self.gameOverReason = "75 Move Rule"
                elif termination == chess.Termination.FIVEFOLD_REPETITION:
                    self.gameOverReason = "5-Fold Repition"

            if self.changed:
                highlightSquares = [self.lastMoveStart, self.lastMoveEnd, self.startSquare]
                self.gui.renderGameArea(self.board, highlightSquares, self.whiteOrientation, self.checkSquare)
                self.gui.renderContainers(self)
                self.changed = False

    def __getSquareFromCoordinates(self, x : int, y : int, whiteOrientation : bool = True) -> chess.Square:
        if x > Constants.BOARD_SIZE or y > Constants.BOARD_SIZE:
            return None
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        column = int(x / squareSize)
        row = Constants.NUM_TILES - int(y / squareSize) - 1

        if not whiteOrientation:
            column = Constants.NUM_TILES - column - 1
            row = Constants.NUM_TILES - row - 1

        return row * Constants.NUM_TILES + column

    def getTurnNumber(self) -> int:
        return (self.halfTurnNumber - 1) // 2 + 1

    def getTurnColor(self) -> chess.Color:
        return self.board.turn

    def __isComputerTurn(self) -> bool:
        return self.players < 2 and self.getTurnColor() != self.humanColor

    def newGame(self, players : int, humanColor : chess.Color = None) -> None:
        self.board = chess.Board()
        self.timer.restart()
        self.gameOver = False
        self.gameOverStatus = None
        self.players = players
        self.halfTurnNumber = 1
        self.promotionPending = False
        self.promotionPiece = None
        self.checkSquare = None
        self.startSquare = None
        self.endSquare = None
        self.changed = True
        self.lastMoveStart = None
        self.lastMoveEnd = None
        self.lastMoves = []
        if players == 1:
            if humanColor == None:
                humanColor = randint(chess.BLACK, chess.WHITE)
            self.whiteOrientation = humanColor
            self.humanColor = humanColor
        else:
            self.whiteOrientation = True
        self.gameOverScreen = False
        self.newGameScreen = False
        self.changed = True

    def isHumanMove(self) -> bool:
        return self.players == 2 or self.board.turn == self.humanColor

    def writeLog(self, log : "list[str]") -> None:
        self.aiLogMap.append(log)

    def getCurrentLog(self) -> "list[str]":
        try:
            return self.aiLogs[len(self.aiLogs) - 1]
        except:
            return [""]