from Core.Essencial import GameObject
from Scripts.StateManager import StateManager
from typing import Union
from pygame import Vector2

class SceneManager(GameObject):
    def __init__(self, position: Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        super().__init__(position = position)
        self.scenesList = []
        self.scene = []
    def Update(self, *props):
        if self.scene:
            for obj in self.scene:
                obj.Update(*props)
    def ChangeScene(self, index : int = 0):
        self.scene = self.scenesList[index](self)
        return self
    def SetScene(self, scenes : list = []):
        self.scenesList = scenes
        return self
    def AppendScene(self, scene):
        self.scenesList.append(scene)
        return self