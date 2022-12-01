from typing import Union
from pygame import Vector2

def Lerp(start : float, end : float, interpolation : float):        #Linear interpolation
    interpolation = Clamp(0, 1, interpolation)
    if interpolation == 0:
        return start
    if interpolation == 1:
        return end
    else:
        return (start + end) * interpolation
def Vector2Lerp(start : Union[tuple[float, float], list[float], Vector2], end : Union[tuple[float, float], list[float], Vector2], interpolation : float) -> Vector2:
    interpolation = Clamp(0, 1, interpolation)
    if interpolation == 0:
        return start
    if interpolation == 1:
        return end
    else:
        return Vector2((start[0] + end[0]) * interpolation, (start[1] + end[1]) * interpolation)
def Clamp(min : float, max : float, value : float) -> float:
    if value >= max: return max
    elif value <= min: return min
    else: return value