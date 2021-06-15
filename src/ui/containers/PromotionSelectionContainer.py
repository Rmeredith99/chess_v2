from src.Constants import Constants
from src.ui.containers.Container import Container

import chess
import pygame

def getPromotionSelectionContainer(game) -> Container:
    boxXPosition = (Constants.BOARD_SIZE - Constants.PROMOTION_BOX_WIDTH) // 2
    boxYPosition = (Constants.BOARD_SIZE - Constants.PROMOTION_BOX_HEIGHT) // 2
    promotionContainer = Container(
        Constants.PROMOTION_BOX_WIDTH, 
        Constants.PROMOTION_BOX_HEIGHT, 
        boxXPosition, 
        boxYPosition, 
        Constants.PROMOTION_BOX_COLOR
    )

    textFont = pygame.font.SysFont("Arial", Constants.PROMOTION_TEXT_SIZE)
    buttonXPosition = (Constants.PROMOTION_BOX_WIDTH - Constants.PROMOTION_BUTTON_WIDTH) // 2
    buttonYOffset = (Constants.PROMOTION_BOX_HEIGHT - 4 * Constants.PROMOTION_BUTTON_HEIGHT) // 5
    
    queenButton = Container(Constants.PROMOTION_BUTTON_WIDTH, Constants.PROMOTION_BUTTON_HEIGHT)
    queenButton.setFillColor(Constants.PROMOTION_BUTTON_COLOR)
    queenButton.setText(["Queen"], textFont, Constants.WHITE, (0, 0), centered = True)
    def queenButtonFunction(game):
        game.promotionPiece = chess.QUEEN
    queenButton.setOnClickFunction(queenButtonFunction)
    promotionContainer.addContainer(queenButton, buttonXPosition, buttonYOffset)

    rookButton = Container(Constants.PROMOTION_BUTTON_WIDTH, Constants.PROMOTION_BUTTON_HEIGHT)
    rookButton.setFillColor(Constants.PROMOTION_BUTTON_COLOR)
    rookButton.setText(["Rook"], textFont, Constants.WHITE, (0, 0), centered = True)
    def rookButtonFunction(game):
        game.promotionPiece = chess.ROOK
    rookButton.setOnClickFunction(rookButtonFunction)
    promotionContainer.addContainer(rookButton, buttonXPosition, buttonYOffset * 2 + Constants.PROMOTION_BUTTON_HEIGHT)

    bishopButton = Container(Constants.PROMOTION_BUTTON_WIDTH, Constants.PROMOTION_BUTTON_HEIGHT)
    bishopButton.setFillColor(Constants.PROMOTION_BUTTON_COLOR)
    bishopButton.setText(["Bishop"], textFont, Constants.WHITE, (0, 0), centered = True)
    def bishopButtonFunction(game):
        game.promotionPiece = chess.BISHOP
    bishopButton.setOnClickFunction(bishopButtonFunction)
    promotionContainer.addContainer(bishopButton, buttonXPosition, buttonYOffset * 3 + Constants.PROMOTION_BUTTON_HEIGHT * 2)

    knightButton = Container(Constants.PROMOTION_BUTTON_WIDTH, Constants.PROMOTION_BUTTON_HEIGHT)
    knightButton.setFillColor(Constants.PROMOTION_BUTTON_COLOR)
    knightButton.setText(["Knight"], textFont, Constants.WHITE, (0, 0), centered = True)
    def knightButtonFunction(game):
        game.promotionPiece = chess.KNIGHT
    knightButton.setOnClickFunction(knightButtonFunction)
    promotionContainer.addContainer(knightButton, buttonXPosition, buttonYOffset * 4 + Constants.PROMOTION_BUTTON_HEIGHT * 3)

    return promotionContainer
