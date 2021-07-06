from src.Constants import Constants
from src.ui.containers.Container import Container

import chess
import pygame

def getBeginNewGameContainer(game) -> Container:
    boxXPosition = (Constants.BOARD_SIZE - Constants.NEW_GAME_SELECTION_CONTAINER_WIDTH) // 2
    boxYPosition = (Constants.BOARD_SIZE - Constants.NEW_GAME_SELECTION_CONTAINER_HEIGHT) // 2
    newGameContainer = Container(
        Constants.NEW_GAME_SELECTION_CONTAINER_WIDTH, 
        Constants.NEW_GAME_SELECTION_CONTAINER_HEIGHT, 
        boxXPosition, 
        boxYPosition, 
        Constants.NEW_GAME_SELECTION_CONTAINER_COLOR
    )

    textFont = pygame.font.SysFont("Arial", Constants.NEW_GAME_SELECTION_BUTTON_TEXT_SIZE)
    buttonXPosition = (Constants.NEW_GAME_SELECTION_CONTAINER_WIDTH - Constants.NEW_GAME_SELECTION_BUTTON_WIDTH) // 2
    buttonYOffset = (Constants.NEW_GAME_SELECTION_CONTAINER_HEIGHT - 5 * Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT) // 6
    
    twoPlayerButton = Container(Constants.NEW_GAME_SELECTION_BUTTON_WIDTH, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT)
    twoPlayerButton.setFillColor(Constants.NEW_GAME_SELECTION_BUTTON_COLOR)
    twoPlayerButton.setText(["Two-Player"], textFont, Constants.WHITE, (0, 0), centered = True)
    def twoPlayerFunction(game):
        game.newGame(2)
    twoPlayerButton.setOnClickFunction(twoPlayerFunction)
    newGameContainer.addContainer(twoPlayerButton, buttonXPosition, buttonYOffset)

    onePlayerWhiteButton = Container(Constants.NEW_GAME_SELECTION_BUTTON_WIDTH, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT)
    onePlayerWhiteButton.setFillColor(Constants.NEW_GAME_SELECTION_BUTTON_COLOR)
    onePlayerWhiteButton.setText(["One-Player (White)"], textFont, Constants.WHITE, (0, 0), centered = True)
    def onePlayerWhiteFunction(game):
        game.newGame(1, chess.WHITE)
    onePlayerWhiteButton.setOnClickFunction(onePlayerWhiteFunction)
    newGameContainer.addContainer(onePlayerWhiteButton, buttonXPosition, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT + 2 * buttonYOffset)

    onePlayerBlackButton = Container(Constants.NEW_GAME_SELECTION_BUTTON_WIDTH, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT)
    onePlayerBlackButton.setFillColor(Constants.NEW_GAME_SELECTION_BUTTON_COLOR)
    onePlayerBlackButton.setText(["One-Player (Black)"], textFont, Constants.WHITE, (0, 0), centered = True)
    def onePlayerBlackFunction(game):
        game.newGame(1, chess.BLACK)
    onePlayerBlackButton.setOnClickFunction(onePlayerBlackFunction)
    newGameContainer.addContainer(onePlayerBlackButton, buttonXPosition, 2 * Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT + 3 * buttonYOffset)

    onePlayerRandomButton = Container(Constants.NEW_GAME_SELECTION_BUTTON_WIDTH, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT)
    onePlayerRandomButton.setFillColor(Constants.NEW_GAME_SELECTION_BUTTON_COLOR)
    onePlayerRandomButton.setText(["One-Player (Random)"], textFont, Constants.WHITE, (0, 0), centered = True)
    def onePlayerRandomFunction(game):
        game.newGame(1)
    onePlayerRandomButton.setOnClickFunction(onePlayerRandomFunction)
    newGameContainer.addContainer(onePlayerRandomButton, buttonXPosition, 3 * Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT + 4 * buttonYOffset)

    zeroPlayerRandomButton = Container(Constants.NEW_GAME_SELECTION_BUTTON_WIDTH, Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT)
    zeroPlayerRandomButton.setFillColor(Constants.NEW_GAME_SELECTION_BUTTON_COLOR)
    zeroPlayerRandomButton.setText(["Compete AIs"], textFont, Constants.WHITE, (0, 0), centered = True)
    def zeroPlayerRandomFunction(game):
        game.newGame(0)
    zeroPlayerRandomButton.setOnClickFunction(zeroPlayerRandomFunction)
    newGameContainer.addContainer(zeroPlayerRandomButton, buttonXPosition, 4 * Constants.NEW_GAME_SELECTION_BUTTON_HEIGHT + 5 * buttonYOffset)

    return newGameContainer