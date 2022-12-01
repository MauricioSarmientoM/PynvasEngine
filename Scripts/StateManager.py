from Scripts.Essencial import GameObject
from random import randint
from pygame import Surface

class StateManager(GameObject):
    def __init__(self, screen = None) -> None:
        self.player1 : GameObject = None
        self.player2 : GameObject = None
        self.bg : tuple[int, int, int] = 10, 10, 10
        self.screen : Surface = screen
        self.turn = randint(0, 1)
        self.round = 0
    def SetPlayer1(self, player1 : GameObject):
        self.player1 = player1
        return self
    def SetPlayer2(self, player2 : GameObject):
        self.player2 = player2
        return self
    def SetDefault(self):
        self.player1 = None
        self.player2 = None
        self.turn = randint(0, 1)
        self.bg = 10, 10, 10
        self.round = 0