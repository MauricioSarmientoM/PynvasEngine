from Scripts.Essencial import GameObject
from Scripts.Shinobi import Shinobi, Uchiha, Uzumaki, Otsutsuki
from Scripts.UI import Text, Button, Image, CharacterData, BattleUI
from Scripts.StateManager import StateManager
from typing import Union
from pygame import Vector2
from sys import exit

class SceneManager(GameObject):
    def __init__(self, state : StateManager, position: Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        super().__init__(position)
        self.scenesList = []
        self.scene = []
        self.state = state
    def Update(self, *props):
        for obj in self.scene:
            obj.Update(self.state, self, *props)
    def ChangeScene(self, index : int = 0):
        self.scene = self.scenesList[index](self)
        return self
    def SetScene(self, scenes : list = []):
        self.scenesList = scenes
        return self
    def AppendScene(self, scene):
        self.scenesList.append(scene)
        return self
def MainMenu(scene : SceneManager) -> list[GameObject]:
    titlePos = Vector2(243, 250)
    scene.state.SetDefault()
    return [
        Image(src = './Sprites/Logo.png', position = (10, 0)),
        Text(color = (255, 255, 255), position = titlePos, text = 'Ultimate Ninja'),
        Text(color = (255, 255, 255), position = titlePos + Vector2(20, 32), text = 'Storm OOP'),
        Button(size = (140, 40), color = (255, 255, 255), position = (260, 320), text = 'PLAY', onClick = scene.ChangeScene, onClickProps = 1),
        Button(size = (140, 40), color = (255, 127, 127), fontColor = (255, 255, 255), position = (260, 370), text = 'HI-SCORES', onClick = scene.ChangeScene, onClickProps = 3),
        Button(size = (140, 40), color = (255, 0, 0), fontColor = (255, 255, 255), position = (260, 420), text = 'EXIT', onClick = exit)
    ]
def CharacterSelection(scene : SceneManager) -> list[GameObject]:
    mugshots = Vector2(100, 50)
    showoffPos = Vector2(20, 300)
    def CharacterShowOff(character : Shinobi):
        scene.scene.pop(len(scene.scene) - 1)
        scene.scene.append(CharacterData(character = character, state = scene.state))
    return [
        Text(color = (255, 255, 0), position = (210, 20), text = 'Choose Your Fighter'),
        Button(position = (0, 0), size = (80, 40), text = 'Back', onClick = scene.ChangeScene, onClickProps = 0),
        Button(position = mugshots, src = './Sprites/MugshotNaruto.png', onClick = CharacterShowOff, onClickProps = Uzumaki(name = 'Naruto Uzumaki', description = 'Fast fighter full of techs and trickery.', src = './Sprites/NarutoStand00.png', position = showoffPos, shield = 10)),
        Button(position = mugshots + Vector2(140, 0), src = './Sprites/MugshotSasuke.png', onClick = CharacterShowOff, onClickProps = Uchiha(name = 'Sasuke Uchiha', description = 'Agile fighter able to foresee enemy attacks.', src = './Sprites/SasukeStand00.png', position = showoffPos, chakra = 8, shield = 8)),
        Button(position = mugshots + Vector2(280, 0), src = './Sprites/MugshotNeji.png', onClick = CharacterShowOff, onClickProps = Otsutsuki(name = 'Neji Hyuga', description = 'Strong fighter with ever growing might.', src = './Sprites/NejiStand00.png', position = showoffPos, chakra = 14)),
        GameObject()
    ]
def BattleField(scene : SceneManager) -> list[GameObject]:
    scene.state.bg = 30, 120, 10
    scene.state.player1.transform.left, scene.state.player1.transform.top = 122, 100
    scene.state.player2.transform.left, scene.state.player2.transform.top = 440, 100
    return [
        Button(position = (0, 0), size = (80, 40), text = 'Back', onClick = scene.ChangeScene, onClickProps = 0),
        BattleUI(state = scene.state)
    ]
def HiScores(scene : SceneManager) -> list[GameObject]:
    return [
        Text(color = (255, 255, 0), position = (250, 20), text = 'HiScore!'),
        Button(position = (0, 0), size = (80, 40), text = 'Back', onClick = scene.ChangeScene, onClickProps = 0)
        #HiScore Not implemented yet
    ]