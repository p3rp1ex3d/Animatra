# examples/first_animation.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.scene import Scene
from src.core.types import Vector2, Color
from src.shapes.basic import Text
from src.animation.text_animations import TypewriterAnimation, GlitchAnimation, FadeAnimation
from src.export.video_exporter import VideoExporter

def create_first_animation():
    scene = Scene(1920, 1080, fps=30)
    scene.duration = 10.0
    
    text = Text("A Circle's Area", 105)
    text.color = Color(39/255, 126/255, 219/255)
    text.transform.position = Vector2(1920//2, 1080//2)
    scene.add_object(text)
    
    typewriter = FadeAnimation(text, start_time=0.0, stop_time=10.0)
    scene.add_text_animation(typewriter)
  
    return scene

if __name__ == "__main__":  
    scene = create_first_animation()
    exporter = VideoExporter(scene, "my_first_animation.mp4")
    exporter.export(Color(0.9, 0.95, 1.0))