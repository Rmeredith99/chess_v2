from src.Constants import Constants
from src.ui.containers.Container import Container

import pygame

def getLoggingContainers(game) -> Container:
    currentlyUsedHeight = Constants.TURN_CONTAINER_HEIGHT + Constants.UNDO_CONTAINER_HEIGHT + Constants.RESIGN_CONTAINER_HEIGHT + 4 * Constants.BUTTON_OFFSET
    xPosition = Constants.LOGGING_CONTAINER_BUFFER
    yPosition = Constants.TURN_CONTAINER_HEIGHT + Constants.UNDO_CONTAINER_HEIGHT + 2 * Constants.BUTTON_OFFSET

    loggingContainer = Container(
        Constants.SIDE_PANEL_WIDTH - 2 * Constants.LOGGING_CONTAINER_BUFFER,
        Constants.BOARD_SIZE - currentlyUsedHeight,
        xPosition,
        yPosition
    )
    loggingContainer.setFillColor(Constants.LOGGING_CONTAINER_OUTER_COLOR)

    innerContainer = Container(
        Constants.SIDE_PANEL_WIDTH - 4 * Constants.LOGGING_CONTAINER_BUFFER,
        Constants.BOARD_SIZE - currentlyUsedHeight - 2 * Constants.LOGGING_CONTAINER_BUFFER
    )
    innerContainer.setFillColor(Constants.LOGGING_CONTAINER_INNER_COLOR)
    textFont = pygame.font.SysFont("Arial", Constants.LOGGING_CONTAINER_TEXT_SIZE)
    innerContainer.setText(game.getCurrentLog(), textFont, Constants.BLACK, (Constants.LOGGING_CONTAINER_TEXT_OFFSET, Constants.LOGGING_CONTAINER_TEXT_OFFSET))

    return loggingContainer, innerContainer