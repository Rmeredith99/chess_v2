from src.Constants import Constants
from src.ui.containers.Container import Container

import chess
import pygame

def getGameOverContainer(game) -> Container:
    boxXPosition = (Constants.BOARD_SIZE - Constants.GAME_OVER_CONTAINER_WIDTH) // 2
    boxYPosition = (Constants.BOARD_SIZE - Constants.GAME_OVER_CONTAINER_HEIGHT) // 2
    gameOverContainer = Container(
        Constants.GAME_OVER_CONTAINER_WIDTH, 
        Constants.GAME_OVER_CONTAINER_HEIGHT, 
        boxXPosition, 
        boxYPosition, 
        Constants.GAME_OVER_CONTAINER_COLOR
    )

    resultContainer = Container(Constants.GAME_OVER_CONTAINER_WIDTH, Constants.GAME_OVER_CONTAINER_HEIGHT // 3)
    resultContainer.setFillColor(Constants.GAME_OVER_CONTAINER_COLOR)
    if game.gameOverStatus == chess.WHITE:
        resultText = "White Wins"
    elif game.gameOverStatus == chess.BLACK:
        resultText = "Black Wins"
    else:
        resultText = "Draw"
    resultTextFont = pygame.font.SysFont("Arial", Constants.GAME_OVER_CONTAINER_TEXT_SIZE)
    resultTextFont.bold = True
    resultContainer.setText([resultText], resultTextFont, Constants.BLACK, (0, 0), centered = True)
    gameOverContainer.addContainer(resultContainer, 0, 0)

    reasonContainer = Container(Constants.GAME_OVER_CONTAINER_WIDTH, Constants.GAME_OVER_CONTAINER_HEIGHT // 5)
    reasonContainer.setFillColor(Constants.GAME_OVER_CONTAINER_COLOR)
    reasonTextFont = pygame.font.SysFont("Arial", Constants.GAME_OVER_REASON_TEXT_SIZE)
    reasonContainer.setText([game.gameOverReason], reasonTextFont, Constants.BLACK, (0, 0), centered = True)
    gameOverContainer.addContainer(reasonContainer, 0, Constants.GAME_OVER_CONTAINER_HEIGHT // 3)

    closeButton = Container(Constants.GAME_OVER_CLOSE_BUTTON_WIDTH, Constants.GAME_OVER_CLOSE_BUTTON_HEIGHT)
    closeButton.setFillColor(Constants.GAME_OVER_CLOSE_BUTTON_COLOR)
    closeTextFont = pygame.font.SysFont("Arial", Constants.GAME_OVER_CLOSE_TEXT_SIZE)
    closeButton.setText(["Close"], closeTextFont, Constants.WHITE, (0, 0), centered = True)
    def closeButtonFunction(game):
        game.gameOverScreen = False
    closeButton.setOnClickFunction(closeButtonFunction)
    gameOverContainer.addContainer(
        closeButton, 
        Constants.GAME_OVER_CONTAINER_WIDTH - Constants.GAME_OVER_CLOSE_BUTTON_WIDTH - Constants.GAME_OVER_CLOSE_BUTTON_OFFSET, 
        Constants.GAME_OVER_CONTAINER_HEIGHT - Constants.GAME_OVER_CLOSE_BUTTON_HEIGHT - Constants.GAME_OVER_CLOSE_BUTTON_OFFSET)

    return gameOverContainer