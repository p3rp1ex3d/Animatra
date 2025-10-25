# src/animation/text_animations.py
from typing import List, Optional
import random
import time
from ..core.types import Vector2, Color
from ..shapes.basic import Text
from .animator import Animation, Keyframe


class TextAnimation:
    """Base class for all text animations with start/stop timing"""
    def __init__(self, text_obj: Text, start_time: float = 0.0, stop_time: float = 2.0):
        self.text_obj = text_obj
        self.start_time = start_time
        self.stop_time = stop_time
        self.duration = stop_time - start_time
        self.current_time = 0.0
        self.finished = False
        self.scene = None  
        
        self.original_text = text_obj.content
        self.original_position = Vector2(text_obj.transform.position.x, text_obj.transform.position.y)
        self.original_color = Color(text_obj.color.r, text_obj.color.g, text_obj.color.b, text_obj.color.a)
    
    def update(self, scene_current_time: float):
        """Update animation based on scene time"""
        self.scene_current_time = scene_current_time
        
        if scene_current_time < self.start_time:
            self.on_before_start()
        elif scene_current_time > self.stop_time:
            if not self.finished:
                self.on_finish()
                self.finished = True
        else:
            local_time = scene_current_time - self.start_time
            progress = min(local_time / self.duration, 1.0)
            self.on_animate(progress)
    
    def on_before_start(self):
        """Override to set initial state before animation starts"""
        pass
    
    def on_animate(self, progress: float):
        """Override to define animation behavior (0.0 to 1.0)"""
        pass
    
    def on_finish(self):
        """Override to clean up after animation finishes"""
        pass

    def reset(self):
        """Reset text to original state"""
        self.text_obj.content = self.original_text
        self.text_obj.transform.position = self.original_position
        self.text_obj.color = self.original_color
        self.current_time = 0.0
        self.finished = False

class TypewriterAnimation(TextAnimation):
    def __init__(self, text_obj: Text, start_time: float = 0.0, stop_time: float = 2.0, cursor: str = "|"):
        super().__init__(text_obj, start_time, stop_time)
        self.cursor = cursor
        self.displayed_text = ""
        self.full_text = text_obj.content 
    
    def on_before_start(self):
        """Before animation starts - show empty text"""
        self.text_obj.content = ""
    
    def on_animate(self, progress: float):
        """During animation - show text gradually"""
        chars_to_show = int(len(self.full_text) * progress)
        self.displayed_text = self.full_text[:chars_to_show]
        
        cursor_visible = int(self.scene_current_time * 5) % 2 == 0
        display_content = self.displayed_text + (self.cursor if cursor_visible else "")
        
        self.text_obj.content = display_content
    
    def on_finish(self):
        """After animation - show full text without cursor"""
        self.text_obj.content = self.full_text
        
class GlitchAnimation(TextAnimation):
    def __init__(self, text_obj: Text, start_time: float = 0.0, stop_time: float = 1.5, intensity: float = 0.3):
        super().__init__(text_obj, start_time, stop_time)
        self.intensity = intensity
        self.glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        self.original_content = text_obj.content
    
    def on_before_start(self):
        """Before animation starts - ensure original state"""
        self.text_obj.content = self.original_content
        self.text_obj.transform.position = self.original_position
        self.text_obj.color = self.original_color
    
    def on_animate(self, progress: float):
        """During animation - apply glitch effects"""
        if progress < 0.8:
            if random.random() < self.intensity:
                glitched = list(self.original_content)
                for i in range(len(glitched)):
                    if random.random() < 0.2:
                        glitched[i] = random.choice(self.glitch_chars)

                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-3, 3)
                self.text_obj.transform.position = Vector2(
                    self.original_position.x + offset_x,
                    self.original_position.y + offset_y
                )

                self.text_obj.color = Color(
                    random.random(),
                    random.random(), 
                    random.random(),
                    1.0
                )
                
                self.text_obj.content = "".join(glitched)
            else:
                self.text_obj.content = self.original_content
                self.text_obj.transform.position = self.original_position
                self.text_obj.color = self.original_color
        else:
            self.text_obj.content = self.original_content
            self.text_obj.transform.position = self.original_position
            self.text_obj.color = self.original_color
    
    def on_finish(self):
        """After animation - ensure clean final state"""
        self.text_obj.content = self.original_content
        self.text_obj.transform.position = self.original_position
        self.text_obj.color = self.original_color

class FadeAnimation(TextAnimation):
    def __init__(self, text_obj: Text, start_time: float = 0.0, stop_time: float = 1.0, fade_in: bool = True):
        super().__init__(text_obj, start_time, stop_time)
        self.fade_in = fade_in
    
    def on_before_start(self):
        """Set initial alpha based on fade direction"""
        if self.fade_in:
            self.text_obj.color = Color(
                self.original_color.r,
                self.original_color.g,
                self.original_color.b,
                0.0  
            )
    
    def on_animate(self, progress: float):
        """Animate alpha value"""
        if self.fade_in:
            alpha = progress
        else: 
            alpha = 1 - progress
        
        self.text_obj.color = Color(
            self.original_color.r,
            self.original_color.g, 
            self.original_color.b,
            alpha
        )
