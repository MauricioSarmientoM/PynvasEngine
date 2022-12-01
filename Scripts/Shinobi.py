from random import randint
from Core.Essencial import SpriteRenderer, GameObject
from Core.Mathf import Clamp
from math import ceil
from typing import Union
from pygame import image, Vector2
from pygame.sprite import AbstractGroup

class Shinobi(GameObject):
    def __init__(self, name : str = '', description : str = '', src : str = '', chakra : int = 10, shield : int = 5, clan : str = '', distance : int = 10, position : Union[Vector2, list[float], tuple[float, float]] = (0, 0), specialTech : list = [], *groups: AbstractGroup) -> None:
        super().__init__(position)
        self.sprite = SpriteRenderer(src = src)
        self.sprite.image = image.load(src)
        self.name = name
        self.description = description
        self.chakra = chakra
        self.chakraFlow = chakra                                            #Mechanic to use techniques
        self.shield = shield
        self.activeShield = 10
        self.clan = clan
        self.distance = distance
        self.specialTech = specialTech
    def Attack(self, other):
        damage : int = Clamp(0, 1000, randint(0, self.chakra) - other.activeShield)
        other.chakra -= damage
        return self
    def Defense(self):
        if self.distance >= 10:
            self.activeShield = ceil((randint(0, self.shield)) * 1.9)
        elif self.distance <= 9:
            self.activeShield = ceil((randint(0, self.shield)) * (1 + (self.distance - 2) * 0.1))
        return self
    def Move(self, move : int = 1, left : bool = True):
        if left:                                    #if placed to the left
            if move > 0:                            #and moves to the right
                if self.distance > 0:               #if is not side to side with enemy
                    self.distance += move
                else:
                    pass                            #do something to alert the error
            else:
                if self.distance < 20:               #if is not too far away
                    self.distance += move
                else:
                    pass                            #do something to alert the error
        else:
            if move > 0:
                if self.distance < 20:
                    self.distance += move
                else:
                    pass
            else:
                if self.distance > 0:
                    self.distance += move
                else:
                    pass
        return self
    def Recover(self):
        self.chakraFlow += ceil(self.chakra * 0.25)
        if self.chakraFlow > self.chakra: self.chakraFlow = self.chakra     #In this way, the maximum amount of flow a character can have is equals to the chakra
        return self
    def Heal(self):
        self.chakraFlow += ceil(self.chakra * 0.25)
        if self.chakraFlow > self.chakra: self.chakraFlow = self.chakra     #In this way, the maximum amount of flow a character can have is equals to the chakra
        return self
    def NextRound(self, round : int): ...
    def Update(self, *props):
        props[0].screen.blit(self.sprite.image, self.transform.position)

class Uchiha(Shinobi):
    def __init__(self, name : str = '', description : str = '', src : str = '', chakra : int = 10, shield : int = 5, agility : int = 5, clan : str = 'Uchiha', distance : int = 0, position : Union[Vector2, list[float], tuple[float, float]] = (0, 0), specialTech : list = [], *groups: AbstractGroup) -> None:
        self.agility = agility
        def Special(self):
            self.agility += 10
        specialTech.append(Technique(name = 'Sharingan', description = ['Increases your Agility by 10', 'The agility reduced by 2 every', 'turn to a minimum of 1.'], cost = 8, tech = Special))
        super().__init__(chakra = chakra, clan = clan, description = description, distance = distance, name = name, shield = shield, src = src, position = position, specialTech = specialTech, *groups)
    def NextRound(self, round : int):
        if round >= 1:
            self.agility = ceil(Clamp(1, 1000, self.agility - 2))
        return self
    def Attack(self, other):
        damage : int = Clamp(0, 1000, randint(0, self.chakra) + self.agility - other.shield)
        other.chakra -= damage
        return self

class Uzumaki(Shinobi):
    def __init__(self, name : str = '', description : str = '', src : str = '', chakra : int = 10, shield : int = 5, speed : int = 5, clan : str = 'Uzumaki', distance : int = 0, position : Union[Vector2, list[float], tuple[float, float]] = (0, 0), specialTech : list = [], *groups: AbstractGroup) -> None:
        self.speed = Clamp(0, shield, speed)
        self.shieldBonus = 1
        def Special(self):
            self.shieldBonus += .4
        specialTech.append(Technique(name = 'Fuinjutsu', description = ['Increases your Defense by 40%.', 'This buff decreases by 5% per', 'round to a minimum of 0%.'], cost = 10, tech = Special))
        super().__init__(chakra = chakra, clan = clan, description = description, distance = distance, name = name, shield = shield, src = src, position = position, *groups)
    def NextRound(self, round : int):
        if round >= 1:
            self.shieldBonus = Clamp(1, 10, self.shieldBonus - .05)
        return self
    def Defense(self):
        if self.distance >= 10:
            self.activeShield = ceil((randint(self.speed, self.shield)) * 1.9 * self.shieldBonus)
        elif self.distance <= 9:
            self.activeShield = ceil((randint(self.speed, self.shield)) * (1 + (self.distance - 2) * 0.1))
        return self

class Otsutsuki(Shinobi):
    def __init__(self, name : str = '', description : str = '', src : str = '', chakra : int = 10, shield : int = 5, strength : int = 5, clan : str = 'Otsutsuki', distance : int = 0, position : Union[Vector2, list[float], tuple[float, float]] = (0, 0), specialTech : list = [], *groups: AbstractGroup) -> None:
        self.strength = strength
        self.dmgBonus = 1
        def Special(self):
            self.dmgBonus += .25
        specialTech.append(Technique(name = 'Byakugan', description = ['Your strikes deals 25% more Damage.', 'This extra damage gets reduced by 4%', 'per round to a minimum of 0%.'], cost = 10, tech = Special))
        super().__init__(chakra = chakra, clan = clan, description = description, distance = distance, name = name, shield = shield, src = src, position = position, *groups)
    def NextRound(self, round : int):
        if round >= 1:
            self.dmgBonus = Clamp(1, 10, self.dmgBonus - .04)
        return self
    def Attack(self, other):
        damage : int = ceil((Clamp(0, 1000, randint(0, self.chakra) - other.activeShield) + self.strength) * self.dmgBonus)
        other.chakra -= damage
        other.shield = 0
        return self

class Technique:
    def __init__(self, name = '', description : list[str] = [], cost = 0, score = 0, tech = None, techProps = None) -> None:
        self.name = name
        self.description = description
        self.cost = cost
        self.score = score
        self.tech = tech
        self.techProps = techProps
    def Execute(self, char : Shinobi, *props):
        if char.chakraFlow >= self.cost:
            char.chakraFlow -= self.cost
            if self.techProps != None:
                self.tech(self.techProps)