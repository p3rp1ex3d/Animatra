# src/core/scene.py
from typing import List, Optional
from .types import Vector2, Color, Transform

class Scene:
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.text_animations = []
        self.objects = []
        self.animations = []
        self.current_time = 0.0
        self.duration = 10.0  
        self.last_update_time = None  
        
    def add_object(self, obj: 'SceneObject'):
        """Add an object to the scene"""
        obj.scene = self
        self.objects.append(obj)
        return obj
    
    def add_text_animation(self, text_animation):
        self.text_animations.append(text_animation)
    
    def add_animation(self, animation: 'Animation'):
        """Add animation to the scene"""
        self.animations.append(animation)
    
    def update(self, delta_time: float = None):
        """Update scene state"""
        import time 
        if delta_time is None:
            current_time = time.time()
            if self.last_update_time is None:
                self.last_update_time = current_time
                delta_time = 0.0
            else:
                delta_time = current_time - self.last_update_time
                self.last_update_time = current_time
        
        self.current_time += delta_time
        for text_anim in self.text_animations[:]:
            text_anim.update(self.current_time)
            if text_anim.finished:
                self.text_animations.remove(text_anim)
                
       
        for animation in self.animations[:]: 
            animation.update(self.current_time)  
            if animation.finished:
                self.animations.remove(animation)

        for obj in self.objects:
            obj.update(delta_time)
    
    def render(self, renderer: 'Renderer'):
        """Render all objects in scene"""
        for obj in self.objects:
            if obj.visible:
                obj.draw(renderer)

    def reset(self):
        """Reset scene to initial state"""
        self.current_time = 0.0
        self.last_update_time = None
        
        # Reset text animations
        for text_anim in self.text_animations:
            if hasattr(text_anim, 'reset'):
                text_anim.reset()
            elif hasattr(text_anim, 'finished'):
                text_anim.finished = False
                text_anim.current_time = 0.0
        
        # Reset keyframe animations  
        for animation in self.animations:
            if hasattr(animation, 'finished'):
                animation.finished = False
        
        # Reset objects
        for obj in self.objects:
            if hasattr(obj, 'reset'):
                obj.reset()

class SceneObject:
    def __init__(self):
        self.transform = Transform()  
        self.color = Color(1, 1, 1) 
        self.visible = True
        self.scene: Optional[Scene] = None
    
    def update(self, delta_time: float):
        """Override this for custom object behavior"""
        pass
    
    def draw(self, renderer: 'Renderer'):
        """Override this for custom drawing"""
        pass