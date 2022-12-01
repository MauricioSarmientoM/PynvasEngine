from typing import Union
from pygame import Vector2
from Core.UI import Button, Text
from Core.Essencial import GameObject
from Scripts.StateManager import StateManager
from Scripts.Shinobi import Shinobi

class CharacterData(GameObject):
    def __init__(self, character : Shinobi, state : StateManager, position: Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        super().__init__(position)
        self.player = p1t = state.player1 == None
        if not p1t:
            character.transform.left = 532
            character.sprite.image = character.sprite.flipXImage
        x = 160 if p1t else 20
        self.render = [ character,
                        Button(position = (0, 420) if p1t else (500, 420), size = (140, 60), text = 'GO!', color = (255, 0, 0) if p1t else (0, 0, 255), fontColor = (255, 255, 255), fontSize = 64, onClick = state.SetPlayer1 if p1t else state.SetPlayer2, onClickProps = character),
                        Text(position = (x, 300), text = character.name, color = (255, 255, 255), fontSize = 64),
                        Text(position = (x, 350), text = 'Clan ' + character.clan, color = (255, 255, 255), fontSize = 16),
                        Text(position = (x, 370), text = character.description, color = (255, 255, 255)),
                        Text(position = (x, 400), text = 'Chakra: ' + str(character.chakra), color = (255, 255, 255), fontSize = 16),
                        Text(position = (x, 420), text = 'Shield: ' + str(character.shield), color = (255, 255, 255), fontSize = 16)
        ]
    def Update(self, *props):
        for component in self.render:
            component.Update(*props)
        if self.player and not props[0].player1 == None:
            props[1].scene.pop(len(props[1].scene) - 1)
            props[1].scene.append(Text(position = (20, 250), color = (255, 255, 255), text = 'P1 READY'))
            props[1].scene.append(GameObject())
        elif not self.player and not props[0].player2 == None:
            props[1].scene.pop(len(props[1].scene) - 1)
            props[1].scene.append(Text(position = (500, 250), color = (255, 255, 255), text = 'P2 READY'))
            props[1].scene.append(Button(position = (250, 400), color = (255, 255, 0), fontColor = (0, 0, 0), size = (140, 60), text = 'GO!', fontSize = 64, onClick = props[1].ChangeScene, onClickProps = 2))
    
class BattleUI(GameObject):
    def __init__(self, state : StateManager, position: Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        super().__init__(position)
        battleUIPos = Vector2(400, 360)
        self.buttons = [
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos, text = 'Attack'),
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos + Vector2(120, 0), text = 'Defense'),
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos + Vector2(0, 40), text = 'Techniques'),
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos + Vector2(120, 40), text = 'Recover'),
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos + Vector2(0, 80), text = 'Move Left'),
            Button(color = (255, 255, 255), size = (120, 40), position = battleUIPos + Vector2(120, 80), text = 'Move Right')
        ]
        self.render = [
            state.player1,
            state.player2,
            Button(position = (170, 300), color = (255, 255, 0), fontColor = (0, 0, 0), size = (360, 60), text = 'Player 1 Turn!', fontSize = 64, onClick = self.render.append, onClickProps = self.buttons)
        ]
    def Update(self, *props):
        for component in self.render:
            component.Update(*props)