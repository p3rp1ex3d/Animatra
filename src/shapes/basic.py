# src/shapes/basic.py
from ..core.scene import SceneObject
from ..core.types import Vector2, Color

class Circle(SceneObject):
    def __init__(self, radius: float = 50.0):
        super().__init__()
        self.radius = radius
    
    def draw(self, renderer):
        renderer.draw_circle(self.transform.position, self.radius, self.color)

class Rectangle(SceneObject):
    def __init__(self, width: float = 100.0, height: float = 100.0):
        super().__init__()
        self.width = width
        self.height = height
    
    def draw(self, renderer):
        renderer.draw_rectangle(
            self.transform.position, 
            self.width, 
            self.height, 
            self.color
        )

class Text(SceneObject):
    def __init__(self, content: str = "Hello", font_size: int = 36):
        super().__init__()
        self.content = content
        self.font_size = font_size
    
    def draw(self, renderer):
        renderer.draw_text(
            self.transform.position,
            self.content,
            self.font_size,
            self.color
        )