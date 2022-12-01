from Scripts.StateManager import StateManager
from Core.Essencial import SpriteRenderer, GameObject
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