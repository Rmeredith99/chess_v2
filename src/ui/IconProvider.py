from chess import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
from src.Constants import Constants

import pygame

class IconProvider:

    def __init__(self) -> None:
        self.__loadIcons()
        self.__scaleIcons()

        self.pieceIconMap : "dict[tuple[bool, int], pygame.Surface]" = {
            (WHITE, PAWN): self.WHITE_PAWN_ICON,
            (WHITE, KNIGHT): self.WHITE_KNIGHT_ICON,
            (WHITE, BISHOP): self.WHITE_BISHOP_ICON,
            (WHITE, ROOK): self.WHITE_ROOK_ICON,
            (WHITE, QUEEN): self.WHITE_QUEEN_ICON,
            (WHITE, KING): self.WHITE_KING_ICON,
            (BLACK, PAWN): self.BLACK_PAWN_ICON,
            (BLACK, KNIGHT): self.BLACK_KNIGHT_ICON,
            (BLACK, BISHOP): self.BLACK_BISHOP_ICON,
            (BLACK, ROOK): self.BLACK_ROOK_ICON,
            (BLACK, QUEEN): self.BLACK_QUEEN_ICON,
            (BLACK, KING): self.BLACK_KING_ICON,
        }

    def getIcon(self, pieceType : int, color : bool) -> pygame.Surface:
        return self.pieceIconMap[(color, pieceType)]

    def __loadIcons(self) -> None:
        self.WHITE_PAWN_ICON = pygame.image.load("icons/white_pawn.png")
        self.WHITE_KNIGHT_ICON = pygame.image.load("icons/white_knight.png")
        self.WHITE_BISHOP_ICON = pygame.image.load("icons/white_bishop.png")
        self.WHITE_ROOK_ICON = pygame.image.load("icons/white_rook.png")
        self.WHITE_QUEEN_ICON = pygame.image.load("icons/white_queen.png")
        self.WHITE_KING_ICON = pygame.image.load("icons/white_king.png")

        self.BLACK_PAWN_ICON = pygame.image.load("icons/black_pawn.png")
        self.BLACK_KNIGHT_ICON = pygame.image.load("icons/black_knight.png")
        self.BLACK_BISHOP_ICON = pygame.image.load("icons/black_bishop.png")
        self.BLACK_ROOK_ICON = pygame.image.load("icons/black_rook.png")
        self.BLACK_QUEEN_ICON = pygame.image.load("icons/black_queen.png")
        self.BLACK_KING_ICON = pygame.image.load("icons/black_king.png")

    def __scaleIcons(self) -> None:
        iconSize = int(Constants.BOARD_SIZE / Constants.NUM_TILES * Constants.ICON_RATIO)

        self.WHITE_PAWN_ICON = pygame.transform.smoothscale(self.WHITE_PAWN_ICON, (iconSize, iconSize))
        self.WHITE_KNIGHT_ICON = pygame.transform.smoothscale(self.WHITE_KNIGHT_ICON, (iconSize, iconSize))
        self.WHITE_BISHOP_ICON = pygame.transform.smoothscale(self.WHITE_BISHOP_ICON, (iconSize, iconSize))
        self.WHITE_ROOK_ICON = pygame.transform.smoothscale(self.WHITE_ROOK_ICON, (iconSize, iconSize))
        self.WHITE_QUEEN_ICON = pygame.transform.smoothscale(self.WHITE_QUEEN_ICON, (iconSize, iconSize))
        self.WHITE_KING_ICON = pygame.transform.smoothscale(self.WHITE_KING_ICON, (iconSize, iconSize))

        self.BLACK_PAWN_ICON = pygame.transform.smoothscale(self.BLACK_PAWN_ICON, (iconSize, iconSize))
        self.BLACK_KNIGHT_ICON = pygame.transform.smoothscale(self.BLACK_KNIGHT_ICON, (iconSize, iconSize))
        self.BLACK_BISHOP_ICON = pygame.transform.smoothscale(self.BLACK_BISHOP_ICON, (iconSize, iconSize))
        self.BLACK_ROOK_ICON = pygame.transform.smoothscale(self.BLACK_ROOK_ICON, (iconSize, iconSize))
        self.BLACK_QUEEN_ICON = pygame.transform.smoothscale(self.BLACK_QUEEN_ICON, (iconSize, iconSize))
        self.BLACK_KING_ICON = pygame.transform.smoothscale(self.BLACK_KING_ICON, (iconSize, iconSize))
        