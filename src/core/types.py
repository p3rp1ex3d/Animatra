# src/core/types.py
from dataclasses import dataclass, field
from typing import Any, List, Tuple, Callable
import numpy as np

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

@dataclass
class Color:
    r: float 
    g: float
    b: float
    a: float = 1.0
    
    def to_rgb255(self):
        return (int(self.r * 255), int(self.g * 255), int(self.b * 255))


@dataclass
class Transform:
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    scale: Vector2 = field(default_factory=lambda: Vector2(1, 1))
    rotation: float = 0.0  # radians
