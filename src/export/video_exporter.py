# src/export/video_exporter.py
import cv2
import numpy as np
from typing import Optional
from ..core.scene import Scene
from ..rendering.cairo_renderer import CairoRenderer

class VideoExporter:
    def __init__(self, scene: Scene, output_path: str = "output.mp4"):
        self.scene = scene
        self.output_path = output_path
        self.renderer = CairoRenderer(scene.width, scene.height)
        
    def export(self, background_color: Optional = None):
        """Export the entire animation as video"""
        if background_color is None:
            from ..core.types import Color
            background_color = Color(1, 1, 1)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            self.output_path,
            fourcc,
            self.scene.fps,
            (self.scene.width, self.scene.height)
        )
        
        total_frames = int(self.scene.duration * self.scene.fps)
        frame_duration = 1.0 / self.scene.fps
        
        self.scene.reset()
        
        for frame_num in range(total_frames):
            self.scene.update(frame_duration)
            
            self.renderer.clear(background_color)
            self.scene.render(self.renderer)
            
            frame_rgba = self.renderer.get_numpy_frame()
            frame_bgr = cv2.cvtColor(frame_rgba, cv2.COLOR_RGBA2BGR)
            
            video_writer.write(frame_bgr)
            
        
        video_writer.release()