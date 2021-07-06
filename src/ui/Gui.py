from pygame.locals import DOUBLEBUF
from src.Constants import Constants
from src.ui.containers.BeginNewGameContainer import getBeginNewGameContainer
from src.ui.containers.Container import Container
from src.ui.containers.GameOverContainer import getGameOverContainer
from src.ui.IconProvider import IconProvider
from src.ui.containers.PromotionSelectionContainer import getPromotionSelectionContainer
from src.ui.containers.SidePanelContainer import getSidePanelContainer

import chess
import pygame

class Gui:

    def __init__(self) -> None:
        self.iconProvider = IconProvider()
        self.screen = pygame.display.set_mode((Constants.BOARD_SIZE + Constants.SIDE_PANEL_WIDTH, Constants.BOARD_SIZE), DOUBLEBUF)
        pygame.init()
        pygame.font.init()

        self.mainContainer = None

    def renderGameArea(self, board : chess.Board, highlightSquares : "list[chess.Square]", whiteOrientation : bool = True, checkSquare : chess.Square = None) -> None:
        self.__drawBoard()
        self.__addBoardLabels(whiteOrientation)
        self.__drawPieces(board, whiteOrientation)
        self.__drawHighlight(highlightSquares, whiteOrientation, checkSquare)
        pygame.display.flip()

    def renderContainers(self, game) -> None:
        self.mainContainer = Container(Constants.BOARD_SIZE + Constants.SIDE_PANEL_WIDTH, Constants.BOARD_SIZE, x=0, y=0)
        self.__addSidePanel(game)
        if game.promotionPending:
            self.__addPromotionSelection(game)
        if game.gameOverScreen:
            self.__addGameOverScreen(game)
        elif game.newGameScreen:
            self.__addBeginNewGameScreen(game)
        self.mainContainer.draw(self.screen)
        pygame.display.flip()

    def __drawBoard(self) -> None:
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        rowPosition = 0
        columnPosition = 0

        self.screen.fill(Constants.COLOR_BOARD_DARK)
        for row in range(Constants.NUM_TILES):
            for column in range(Constants.NUM_TILES):
                # creates alternating pattern
                if (row + column) % 2 == 0:
                    rectangle = [columnPosition, rowPosition, squareSize, squareSize]
                    pygame.draw.rect(self.screen, Constants.COLOR_BOARD_LIGHT, rectangle)
                columnPosition += squareSize
            columnPosition = 0
            rowPosition += squareSize

    def __drawPieces(self, board : chess.Board, whiteOrientation : bool = True) -> None:
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        colors = [chess.WHITE, chess.BLACK]
        pieceTypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
        offset = (1 - Constants.ICON_RATIO) / 2 * squareSize

        for color in colors:
            for pieceType in pieceTypes:
                icon = self.iconProvider.getIcon(pieceType, color)
                for square in board.pieces(pieceType, color):
                    column, row = self.__getCoordinatesFromSquare(square, whiteOrientation)
                    xPosition = column * squareSize + offset
                    yPosition = row * squareSize + offset
                    self.screen.blit(icon, (xPosition, yPosition))

    def __addBoardLabels(self, whiteOrientation : bool = True) -> None:
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

    def __getCoordinatesFromSquare(self, square : chess.Square, whiteOrientation : bool = True) -> "tuple[int, int]":
        """
        Converts a chess.Square representation to an (x, y) grid location in the current orientation
        """
        column = square % Constants.NUM_TILES
        row = Constants.NUM_TILES - 1 - square // Constants.NUM_TILES

        if not whiteOrientation:
            column = Constants.NUM_TILES - column - 1
            row = Constants.NUM_TILES - row - 1

        return (column, row)

    def __drawHighlight(self, squares : "list[chess.Square]", whiteOrientation : bool = True, checkSquare : chess.Square = None) -> None:
        squareSize = Constants.BOARD_SIZE / Constants.NUM_TILES
        if checkSquare != None:
            column, row = self.__getCoordinatesFromSquare(checkSquare, whiteOrientation)
            self.__drawOutline(column * squareSize, row * squareSize, squareSize, Constants.COLOR_CHECK_HIGHLIGHT)

        for square in squares:
            if square != None:
                column, row = self.__getCoordinatesFromSquare(square, whiteOrientation)
                self.__drawOutline(column * squareSize, row * squareSize, squareSize, Constants.COLOR_BOARD_HIGHLIGHT)

    def __drawOutline(self, x : int, y : int, size : int, color : "tuple[int, int, int]") -> None:
        rectangles = [
            [x, y, size, Constants.HIGHLIGHT_WIDTH],
            [x, y, Constants.HIGHLIGHT_WIDTH, size],
            [x, y + size - Constants.HIGHLIGHT_WIDTH, size, Constants.HIGHLIGHT_WIDTH],
            [x + size - Constants.HIGHLIGHT_WIDTH, y, Constants.HIGHLIGHT_WIDTH, size]
        ]
        for rectangle in rectangles:
            pygame.draw.rect(self.screen, color, rectangle)

    def __addSidePanel(self, game) -> None:
        self.mainContainer.addContainer(getSidePanelContainer(game), Constants.BOARD_SIZE, 0)

    def __addPromotionSelection(self, game) -> None:
        boxXPosition = (Constants.BOARD_SIZE - Constants.PROMOTION_BOX_WIDTH) // 2
        boxYPosition = (Constants.BOARD_SIZE - Constants.PROMOTION_BOX_HEIGHT) // 2
        self.mainContainer.addContainer(getPromotionSelectionContainer(game), boxXPosition, boxYPosition)

    def __addGameOverScreen(self, game):
        boxXPosition = (Constants.BOARD_SIZE - Constants.GAME_OVER_CONTAINER_WIDTH) // 2
        boxYPosition = (Constants.BOARD_SIZE - Constants.GAME_OVER_CONTAINER_HEIGHT) // 2
        self.mainContainer.addContainer(getGameOverContainer(game), boxXPosition, boxYPosition)

    def __addBeginNewGameScreen(self, game):
        boxXPosition = (Constants.BOARD_SIZE - Constants.NEW_GAME_SELECTION_CONTAINER_WIDTH) // 2
        boxYPosition = (Constants.BOARD_SIZE - Constants.NEW_GAME_SELECTION_CONTAINER_HEIGHT) // 2
        self.mainContainer.addContainer(getBeginNewGameContainer(game), boxXPosition, boxYPosition)

    def handleContainerClick(self, game, x : int, y : int) -> bool:
        return self.mainContainer.tryClick(game, x, y)
