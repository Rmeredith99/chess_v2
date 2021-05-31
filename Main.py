from Gui import Gui
from IconProvider import IconProvider

import chess

class Main:

    def runGame(self) -> None:
        iconProvider = IconProvider()
        gui = Gui(iconProvider)
        board = chess.Board()
        gui.render(board, whiteOrientation = True)

if __name__=="__main__":
    main = Main()
    main.runGame()
    _ = input()