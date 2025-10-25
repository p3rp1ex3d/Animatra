# src/animation/animator.py
from typing import Any, List
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.types import Vector2, Color

class AnimationSystem:
    """Manages and updates all animations with proper timing"""
    def __init__(self):
        self.animations = []
        self.text_animations = [] 
        self.last_time = None
    
    def add_animation(self, animation):
        """Add any type of animation to the system"""
        if hasattr(animation, 'update') and hasattr(animation, 'finished'):
            if hasattr(animation, 'text_obj'):  
                self.text_animations.append(animation)
            else:  
                self.animations.append(animation)
    
    def remove_animation(self, animation):
        """Remove an animation from the system"""
        if animation in self.text_animations:
            self.text_animations.remove(animation)
        if animation in self.animations:
            self.animations.remove(animation)
    
    def update(self, current_time=None):
        """Update all animations with proper timing"""
        if current_time is None:
            current_time = time.time()
        
        if self.last_time is None:
            self.last_time = current_time
            return
        
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        for anim in self.text_animations[:]:
            anim.update(delta_time)
            if anim.finished:
                self.text_animations.remove(anim)
        
        for anim in self.animations[:]:
            anim.update(current_time)
            if anim.finished:
                self.animations.remove(anim)
    
    def clear(self):
        """Clear all animations"""
        self.animations.clear()
        self.text_animations.clear()
        self.last_time = None

class Keyframe:
    def __init__(self, time: float, value: Any, easing: str = "linear"):
        self.time = time
        self.value = value
        self.easing = easing

class Animation:
    def __init__(self, target: Any, property_path: str, keyframes: List[Keyframe]):
        self.target = target
        self.property_path = property_path
        self.keyframes = sorted(keyframes, key=lambda k: k.time)
        self.duration = keyframes[-1].time if keyframes else 0
        self.finished = False
    
    def update(self, current_time: float):
        if not self.keyframes or current_time > self.duration:
            self.finished = True
            return
        
        for i in range(len(self.keyframes) - 1):
            kf_current = self.keyframes[i]
            kf_next = self.keyframes[i + 1]
            
            if kf_current.time <= current_time <= kf_next.time:
                t = (current_time - kf_current.time) / (kf_next.time - kf_current.time)
                t = self.apply_easing(t, kf_current.easing)
                
                current_value = self.interpolate(kf_current.value, kf_next.value, t)
                
                self.set_property(self.target, self.property_path, current_value)
                break
    
    def interpolate(self, a, b, t):
        """Interpolate between two values"""
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a + (b - a) * t
        elif isinstance(a, Vector2) and isinstance(b, Vector2):
            return Vector2(
                a.x + (b.x - a.x) * t,
                a.y + (b.y - a.y) * t
            )
        elif isinstance(a, Color) and isinstance(b, Color):
            return Color(
                a.r + (b.r - a.r) * t,
                a.g + (b.g - a.g) * t,
                a.b + (b.b - a.b) * t,
                a.a + (b.a - a.a) * t
            )
        return b 
    
    def apply_easing(self, t, easing):
        """Apply easing function"""
        if easing == "linear":
            return t
        elif easing == "ease_in":
            return t * t
        elif easing == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif easing == "ease_in_out":
            return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
        return t
    
    def set_property(self, obj, path, value):
        """Set property on object using dot notation path"""
        parts = path.split('.')
        current = obj
        for part in parts[:-1]:
            current = getattr(current, part)
        setattr(current, parts[-1], value)