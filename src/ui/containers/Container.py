from collections.abc import Callable
from pygame.font import Font
from src.Constants import Constants

import pygame

class Container:

    def __init__(self, width : int, height : int, x : int = 0, y : int = 0, color : tuple[int, int, int] = None) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.containers = []
        self.onClickFunction = None
        self.textList = []
        self.textFont = None
        self.textColor = Constants.BLACK
        self.textOffset = (0, 0)
        self.textCentered = False

    def setFillColor(self, color : tuple[int, int, int]) -> None:
        self.color = color

    def setText(self, textList : list[str], font : Font, color : tuple[int, int, int], offset : tuple[int, int], centered : bool = False) -> None:
        self.textList = textList
        self.textFont = font
        self.textColor = color
        self.textOffset = offset
        self.textCentered = centered

    def __renderText(self, screen : pygame.Surface) -> None:
        initialOffset = 0
        offsetX = self.textOffset[0]
        offsetY = self.textOffset[1]
        for textString in self.textList:
            text = self.textFont.render(textString, True, self.textColor)
            rect = text.get_rect()
            if self.textCentered:
                screen.blit(text, (self.x + (self.width - rect.width) // 2, self.y + (self.height - rect.height) // 2))
            else:
                screen.blit(text, (self.x + offsetX, self.y + initialOffset + offsetY))
            initialOffset += offsetY + rect.height

    def __setXPosition(self, x : int) -> None:
        self.x = x

    def __setYPosition(self, y : int) -> None:
        self.y = y

    def addContainer(self, container, x : int, y : int) -> None:
        container.__setXPosition(x + self.x)
        container.__setYPosition(y + self.y)
        self.containers.append(container)

    def __isWithinContainer(self, x : int, y : int) -> bool:
        withinXRange = x < self.x + self.width and x >= self.x
        withinYRange = y < self.y + self.height and y >= self.y
        return withinXRange and withinYRange

    def setOnClickFunction(self, fn : Callable[..., None]) -> None:
        self.onClickFunction = fn

    def __click(self, game) -> bool:
        if self.onClickFunction != None:
            self.onClickFunction(game)
            return True
        return False

    def tryClick(self, game, x : int, y : int) -> bool:
        for subContainer in self.containers:
            if subContainer.__isWithinContainer(x, y):
                return subContainer.tryClick(game, x, y)
        if self.__isWithinContainer(x, y):
            return self.__click(game)
        return False

    def draw(self, screen : pygame.Surface) -> None:
        if self.color != None:
            rectangle = [self.x, self.y, self.width, self.height]
            pygame.draw.rect(screen, self.color, rectangle)
            self.__renderText(screen)

        for subContainer in self.containers:
            subContainer.draw(screen)
