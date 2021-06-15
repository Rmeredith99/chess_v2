from src.Constants import Constants
from src.ui.containers.Container import Container
from src.ui.containers.LoggingContainer import getLoggingContainers

import pygame

def getSidePanelContainer(game) -> Container:
    sidePanelContainer = Container(Constants.SIDE_PANEL_WIDTH, Constants.BOARD_SIZE, x = Constants.BOARD_SIZE, y = 0)
    sidePanelContainer.setFillColor(Constants.SIDE_PANEL_COLOR)

    turnContainer = Container(Constants.SIDE_PANEL_WIDTH, Constants.TURN_CONTAINER_HEIGHT)
    turnContainer.setFillColor(Constants.TURN_CONTAINER_COLOR)
    if game.gameOver:
        turnText = "Game Over"
        turnTextColor = Constants.TURN_TEXT_GAME_OVER_COLOR
    else:
        turnColor = "White" if game.getTurnColor() else "Black"
        turnText = "{}. {} to move".format(str(game.getTurnNumber()), turnColor)
        turnTextColor = Constants.WHITE if game.getTurnColor() else Constants.BLACK
    turnTextFont = pygame.font.SysFont("Arial", Constants.TURN_TEXT_SIZE)
    turnContainer.setText([turnText], turnTextFont, turnTextColor, (0, 0), centered = True)
    sidePanelContainer.addContainer(turnContainer, 0, 0)

    buttonWidth = (Constants.SIDE_PANEL_WIDTH - 3 * Constants.BUTTON_OFFSET) // 2

    flipBoardContainer = Container(buttonWidth, Constants.FLIP_BOARD_CONTAINER_HEIGHT)
    flipBoardContainer.setFillColor(Constants.FLIP_BOARD_CONTAINER_COLOR)
    flipTextFont = pygame.font.SysFont("Arial", Constants.FLIP_BOARD_TEXT_SIZE)
    flipBoardContainer.setText(["Flip Board"], flipTextFont, Constants.WHITE, (0, 0), centered = True)
    def flipBoardFunction(game):
        if not game.newGameScreen and not game.gameOverScreen and not game.gameOver:
            game.whiteOrientation = not game.whiteOrientation
    flipBoardContainer.setOnClickFunction(flipBoardFunction)
    sidePanelContainer.addContainer(
        flipBoardContainer, 
        Constants.BUTTON_OFFSET, 
        Constants.TURN_CONTAINER_HEIGHT + Constants.BUTTON_OFFSET
    )

    undoMoveContainer = Container(buttonWidth, Constants.FLIP_BOARD_CONTAINER_HEIGHT)
    undoMoveContainer.setFillColor(Constants.UNDO_CONTAINER_COLOR)
    undoTextFont = pygame.font.SysFont("Arial", Constants.UNDO_TEXT_SIZE)
    undoMoveContainer.setText(["Undo Move"], undoTextFont, Constants.WHITE, (0, 0), centered = True)
    def undoMoveFunction(game):
        if not game.newGameScreen and not game.gameOverScreen:
            try:
                _ = game.board.pop()
                game.halfTurnNumber -= 1
                game.startSquare = None
                game.endSquare = None
                newLastStart, newLastEnd = game.lastMoves.pop()
                game.lastMoveStart = newLastStart
                game.lastMoveEnd = newLastEnd
                if not game.isHumanMove():
                    _ = game.board.pop()
                    game.halfTurnNumber -= 1
                    game.startSquare = None
                    game.endSquare = None
                    newLastStart, newLastEnd = game.lastMoves.pop()
                    game.lastMoveStart = newLastStart
                    game.lastMoveEnd = newLastEnd
            except:
                game.lastMoveStart = None
                game.lastMoveEnd = None
                print("There are either no moves to undo or no previous moves to highlight.")
            game.gameOver = False
            game.gameOverStatus = None
            game.gameOverReason = None
            game.gameOverScreen = False
            game.newGameScreen = False
            game.promotionPending = False
    undoMoveContainer.setOnClickFunction(undoMoveFunction)
    sidePanelContainer.addContainer(
        undoMoveContainer, 
        Constants.BUTTON_OFFSET * 2 + buttonWidth, 
        Constants.TURN_CONTAINER_HEIGHT + Constants.BUTTON_OFFSET
    )

    resignContainer = Container(buttonWidth, Constants.RESIGN_CONTAINER_HEIGHT)
    resignContainer.setFillColor(Constants.RESIGN_CONTAINER_COLOR)
    resignTextFont = pygame.font.SysFont("Arial", Constants.RESIGN_TEXT_SIZE)
    resignContainer.setText(["Resign"], resignTextFont, Constants.WHITE, (0, 0), centered = True)
    def resignFunction(game):
        if not game.newGameScreen and not game.gameOverScreen and not game.gameOver:
            game.gameOver = True
            game.gameOverStatus = not game.board.turn
            game.gameOverReason = "Resignation"
            game.gameOverScreen = True
            game.promotionPending = False
    resignContainer.setOnClickFunction(resignFunction)
    sidePanelContainer.addContainer(
        resignContainer, 
        Constants.BUTTON_OFFSET, 
        Constants.BOARD_SIZE - Constants.RESIGN_CONTAINER_HEIGHT - Constants.BUTTON_OFFSET
    )

    newGameContainer = Container(buttonWidth, Constants.NEW_GAME_BUTTON_HEIGHT)
    newGameContainer.setFillColor(Constants.NEW_GAME_BUTTON_COLOR)
    newGameTextFont = pygame.font.SysFont("Arial", Constants.NEW_GAME_BUTTON_TEXT_SIZE)
    newGameContainer.setText(["New Game"], newGameTextFont, Constants.WHITE, (0, 0), centered = True)
    def newGameFunction(game):
        if not game.newGameScreen:
            game.newGameScreen = True
            game.gameOverScreen = False
            game.gameOver = True
            game.promotionPending = False
    newGameContainer.setOnClickFunction(newGameFunction)
    sidePanelContainer.addContainer(
        newGameContainer, 
        Constants.BUTTON_OFFSET * 2 + buttonWidth, 
        Constants.BOARD_SIZE - Constants.RESIGN_CONTAINER_HEIGHT - Constants.BUTTON_OFFSET
    )

    outerLoggingContainer, innerLogginContainer = getLoggingContainers(game)

    sidePanelContainer.addContainer(
        outerLoggingContainer, 
        Constants.LOGGING_CONTAINER_BUFFER, 
        Constants.TURN_CONTAINER_HEIGHT + Constants.UNDO_CONTAINER_HEIGHT + 2 * Constants.BUTTON_OFFSET
    )

    outerLoggingContainer.addContainer(
        innerLogginContainer,
        Constants.LOGGING_CONTAINER_BUFFER,
        Constants.LOGGING_CONTAINER_BUFFER
    )

    return sidePanelContainer
