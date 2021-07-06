from time import time

import chess

class Timer:

    def __init__(self, startingTime : float, incrementTime : float) -> None:
        self.timeWhite = startingTime * 60
        self.timeBlack = startingTime * 60
        self.startingTime = startingTime
        self.incrementTime = incrementTime
        self.startTime = None

    def updateTime(self, color : chess.Color) -> None:
        duration = time() - self.startTime
        if color:
            self.timeWhite += self.incrementTime - duration
        else:
            self.timeBlack += self.incrementTime - duration
        self.startTime = time()

    def isOutOfTime(self) -> bool:
        if self.timeWhite < 0:
            return True
        elif self.timeBlack < 0:
            return False
        return None

    def toString(self, color : chess.Color) -> str:
        time = self.timeWhite if color else self.timeBlack
        if time < 0:
            return "0:00"
        minutes = str(int(time / 60))
        seconds = int(time % 60)
        return minutes + ":" + "{:02d}".format(seconds)

    def getTimeRemaining(self, color : chess.Color) -> float:
        if color:
            return self.timeWhite
        return self.timeBlack

    def restart(self) -> None:
        self.timeWhite = self.startingTime * 60
        self.timeBlack = self.startingTime * 60
        self.startTime = time()