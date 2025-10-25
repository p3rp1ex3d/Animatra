# src/rendering/cairo_renderer.py
import cairo
import numpy as np
from ..core.types import Vector2, Color

class CairoRenderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context(self.surface)
        
        self.ctx.translate(0, height)
        self.ctx.scale(1, -1)
        
        self.background = Color(0, 0, 0)
    
    def clear(self, color: Color = None):
        """Clear the canvas with background color"""
        color = color or self.background
        self.ctx.set_source_rgba(color.r, color.g, color.b, color.a)
        self.ctx.paint()
    
    def draw_circle(self, center: Vector2, radius: float, color: Color):
        """Draw a circle"""
        self.ctx.arc(center.x, center.y, radius, 0, 2 * np.pi)
        self.ctx.set_source_rgba(color.r, color.g, color.b, color.a)
        self.ctx.fill()
    
    def draw_rectangle(self, center: Vector2, width: float, height: float, color: Color):
        """Draw a rectangle centered at position"""
        x = center.x - width / 2
        y = center.y - height / 2
        self.ctx.rectangle(x, y, width, height)
        self.ctx.set_source_rgba(color.r, color.g, color.b, color.a)
        self.ctx.fill()
    
    def draw_text(self, position: Vector2, text: str, font_size: int, color: Color):
        """Draw text centered at the given position"""
        self.ctx.save()
        self.ctx.identity_matrix()
        
        self.ctx.set_font_size(font_size)
        self.ctx.set_source_rgba(color.r, color.g, color.b, color.a)
        
        extents = self.ctx.text_extents(text)
        text_width = extents[2]  
        text_height = extents[3] 
        
        text_x = position.x - text_width / 2
        text_y = self.height - position.y + text_height / 2  
        
        self.ctx.move_to(text_x, text_y)
        self.ctx.show_text(text)
        self.ctx.restore()
    
    def get_numpy_frame(self) -> np.ndarray:
        """Get current frame as numpy array for video export"""
        buf = self.surface.get_data()
        return np.ndarray(
            shape=(self.height, self.width, 4),
            dtype=np.uint8,
            buffer=buf
        )