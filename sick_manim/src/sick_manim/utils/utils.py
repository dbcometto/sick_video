from manim import *
from typing import Optional

def render_scene(scene: Scene, config: Optional[tempconfig] = None):
    """Render a scene"""
    if config:
        with config:
            scene().render()
    else:
        scene().render()