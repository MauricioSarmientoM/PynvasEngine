from Scripts.StateManager import StateManager
from Scripts.Essencial import SpriteRenderer, GameObject
from Scripts.Shinobi import Shinobi
from pygame.surface import Surface
from pygame.font import Font
from pygame.sprite import AbstractGroup
from pygame import Vector2, event, mouse, MOUSEBUTTONUP, image, transform
from typing import Union

class Button(GameObject):
    def __init__(self, position : Union[Vector2, list[float], tuple[float, float]], color : tuple[int, int, int] = (255, 255, 255), size : Union[tuple[float, float], list[float], Vector2] = (0, 0), src : str = '', text : str = None, fontColor : tuple[int, int, int] = (0, 0, 0), fontSize : float = 32, onClick = None, onClickProps = None, *groups: AbstractGroup) -> None:
        super().__init__(position)
        if src == '':
            self.sprite = SpriteRenderer(size = size, *groups)
            self.sprite.image = Surface(self.sprite.size)
            self.sprite.image.fill(color)
        else:
            self.sprite = SpriteRenderer(src = src, *groups)
            self.sprite.image = image.load(src)
        self.__text = Font(None, fontSize)
        self.text = text
        self.textColor = fontColor
        self.__onClick = onClick
        self.onClickProps = onClickProps
    @property
    def textPosition(self) -> Vector2:
        pos = self.__text.render(self.text, True, (0, 0, 0), None).get_rect()
        return Vector2(self.transform.position[0] + ((self.sprite.size[0] - pos.width) / 2), self.transform.position[1] + ((self.sprite.size[1] - pos.height) / 2))
    def Render(self, color : Union[tuple[float, float, float], tuple[float, float, float, float], list[float]], bgColor : Union[tuple[float, float, float], tuple[float, float, float, float], list[float]] = None) -> Surface:
        return self.__text.render(self.text, True, color, bgColor)
    def OnClick(self):
        for e in event.get():
            #if mouse.get_pressed()[0]:
            if e.type == MOUSEBUTTONUP:                     #for some reason this sometimes doesn't works
                pos = Vector2(mouse.get_pos())
                if pos.x <= (self.transform.position.x + self.sprite.size.x) and pos.x >= self.transform.position.x and pos.y <= (self.transform.position.y + self.sprite.size.y) and pos.y >= self.transform.position.y:
                    print(str(pos) + str(self.transform.position) + str(self.transform.position + self.sprite.size))
                    self.__onClick(self.onClickProps)
    def Update(self, *props):
        if self.__onClick != None:
            self.OnClick()
        props[0].screen.blit(self.sprite.image, self.transform.position)
        props[0].screen.blit(self.Render(self.textColor), self.textPosition)

class Text(GameObject):
    def __init__(self, color : tuple[int, int, int] = (0, 0, 0), position : Union[Vector2, list[float], tuple[float, float]] = (0, 0), text : str = None, fontSize : int = 32, *groups: AbstractGroup) -> None:
        super().__init__(position)
        self.sprite = SpriteRenderer(*groups)
        self.__text = Font(None, fontSize)
        self.text = text
        self.color = color
        self.sprite.image = self.__text.render(self.text, True, color)
    @property
    def textPosition(self) -> Vector2:
        pos = self.sprite.image.get_rect()
        return Vector2(self.transform.position[0] + ((self.sprite.size[0] - pos.width) / 2), self.transform.position[1] + ((self.sprite.size[1] - pos.height) / 2))
    def Update(self, *props):
        props[0].screen.blit(self.sprite.image, self.transform.position)

class Image(GameObject):
    def __init__(self, src, position: Union[list[float], tuple[float, float], Vector2] = ...) -> None:
        super().__init__(position)
        self.sprite = SpriteRenderer(src = src)
        self.sprite.image = image.load(src)
    def Update(self, *props):
        props[0].screen.blit(self.sprite.image, self.transform.position)

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