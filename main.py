from sys import exit
from Scripts.StateManager import StateManager
from Core.SceneManager import SceneManager
from Scripts.Scenes import MainMenu, CharacterSelection, BattleField, HiScores
from pygame import init as StartGame, display, event, QUIT
from pygame.font import init as StartFont

StartGame()
StartFont()

size = width, height = 640, 480             #Setting the size of the window
screen = display.set_mode(size)             #Setting the main window as a Surface
data = StateManager(screen = screen)        #Creating the StateManager to keep some global info
game = SceneManager()                       #This is the scene manager that keeps all the objects
game.children['state'] = data
game.SetScene([MainMenu, CharacterSelection, BattleField, HiScores]).ChangeScene()
while True:                                 #Literally, Gaem Loop
    for e in event.get():                   #Without this, the game doesn't close xd
        if e.type == QUIT: exit()
    screen.fill(data.bg)                    #Recoloring the bg allows the antialias works like a charm
    game.Update(data, game)                       #Updating every GameObject that gets instanciated in scene
    display.update()