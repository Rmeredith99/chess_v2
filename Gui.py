from IconProvider import IconProvider
from pygame.locals import DOUBLEBUF
from typing import NewType

import chess
import Constants
import pygame

class Gui:

    def __init__(self, iconProvider : IconProvider) -> None:
        self.iconProvider = iconProvider
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Constants.BOARD_SIZE, Constants.BOARD_SIZE), DOUBLEBUF)

    def render(self, board : chess.Board, whiteOrientation : bool = True) -> None:
        self.drawBoard()
        self.addBoardLabels(whiteOrientation)
        self.drawPieces(board, whiteOrientation)
        pygame.display.flip()

    def drawBoard(self) -> None:
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        rowPosition = 0
        columnPosition = 0

        self.screen.fill(Constants.COLOR_BOARD_DARK)
        for row in range(Constants.NUM_TILES):
            for column in range(Constants.NUM_TILES):
                #creates alternating pattern
                if (row + column) % 2 == 0:
                    rectangle = [columnPosition, rowPosition, squareSize, squareSize]
                    pygame.draw.rect(self.screen, Constants.COLOR_BOARD_LIGHT, rectangle)
                columnPosition += squareSize
            columnPosition = 0
            rowPosition += squareSize

    def drawPieces(self, board : chess.Board, whiteOrientation : bool = True) -> None:
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        colors = [chess.WHITE, chess.BLACK]
        pieceTypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
        offset = (1 - Constants.ICON_RATIO) / 2 * squareSize

        for color in colors:
            for pieceType in pieceTypes:
                icon = self.iconProvider.getIcon(pieceType, color)
                for square in board.pieces(pieceType, color):
                    column, row = self.getCoordinatesFromSquare(square, whiteOrientation)
                    xPosition = column * squareSize + offset
                    yPosition = row * squareSize + offset
                    self.screen.blit(icon, (xPosition, yPosition))

    def addBoardLabels(self, whiteOrientation : bool = True) -> None:
        font = pygame.font.SysFont("Arial", Constants.RANK_FILE_FONT_SIZE)
        font.bold = True
        ranks = "87654321" if whiteOrientation else "12345678"
        files = "abcdefgh" if whiteOrientation else "hgfedcba"
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        textOffsetFileX = squareSize * Constants.TEXT_OFFSET_RATIO_FILE_X
        textOffsetFileY = squareSize * Constants.TEXT_OFFSET_RATIO_FILE_Y
        textOffsetRankX = squareSize * Constants.TEXT_OFFSET_RATIO_RANK_X
        textOffsetRankY = squareSize * Constants.TEXT_OFFSET_RATIO_RANK_Y

        for row in range(Constants.NUM_TILES):
            color = Constants.COLOR_BOARD_DARK if row % 2 == 0 else Constants.COLOR_BOARD_LIGHT
            textSurface = font.render(ranks[row], True, color)
            xPosition = textOffsetRankX
            yPosition = row * squareSize + textOffsetRankY
            self.screen.blit(textSurface, (xPosition, yPosition))

        for column in range(Constants.NUM_TILES):
            color = Constants.COLOR_BOARD_DARK if column % 2 == 1 else Constants.COLOR_BOARD_LIGHT
            textSurface = font.render(files[column], True, color)
            xPosition = column * squareSize + textOffsetFileX
            yPosition = (Constants.NUM_TILES - 1) * squareSize + textOffsetFileY
            self.screen.blit(textSurface, (xPosition, yPosition))

    def getCoordinatesFromSquare(self, square : chess.Square, whiteOrientation : bool = True) -> tuple[int, int]:
        """
        Converts a chess.Square representation to an (x, y) grid location in the current orientation
        """
        column = square % Constants.NUM_TILES
        row = Constants.NUM_TILES - 1 - square // Constants.NUM_TILES

        if not whiteOrientation:
            column = Constants.NUM_TILES - column - 1
            row = Constants.NUM_TILES - row - 1

        return (column, row)