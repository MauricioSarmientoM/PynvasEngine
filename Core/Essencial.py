from pygame import image, Rect, Vector2, transform, Surface
from pygame.sprite import Sprite, AbstractGroup
from typing import Union

class Component:
    def __init__(self) -> None:
        pass
    def Update(self, *props) -> None: ...

class SpriteRenderer(Component, Sprite):
    def __init__(self, src : Union[str, list[str]] = '', size : Union[list[float], tuple[float, float], Vector2] = (0, 0), *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        if len(src) > 0:
            img = image.load(src)
            self.width, self.height = img.get_rect().width, img.get_rect().height
        else:
            self.width, self.height = size
    @property                                                               #Now 'rect' acts like self.rect instead of self.rect()
    def rect(self) -> Rect:
        return self.image.get_rect()
    @property
    def size(self) -> Vector2:
        return Vector2((self.width, self.height))
    @property
    def flipXImage(self) -> Surface:
        return transform.flip(self.image, True, False)
    @property
    def flipYImage(self) -> Surface:
        return transform.flip(self.image, False, True)
    @property
    def flipXYImage(self) -> Surface:
        return transform.flip(self.image, True, True)

class Transform(Component):
    def __init__(self, position : Union[list[float], tuple[float, float], Vector2] = (0, 0), center : Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        self.left, self.top = position[0], position[1]
        self.xOffset, self.yOffset = center
    @property
    def position(self) -> Vector2:
        return Vector2(self.left, self.top)
    @property
    def center(self) -> Vector2:
        return Vector2(self.xOffset, self.yOffset)
        
class Animator(Component):                     #This is what will be in charge on most details of animation and movement
    def __init__(self) -> None:
        pass

class GameObject:
    def __init__(self, position : Union[list[float], tuple[float, float], Vector2] = (0, 0)) -> None:
        self.components : dict[Component] = { "transform" : Transform(position) }
        self.children : dict = {}
    def Update(self, *props):
        if self.components:
            for comp in self.components:
                comp.Update(*props)
        if self.children:
            for child in self.children:
                child.Update(*props)