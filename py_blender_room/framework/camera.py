from dataclasses import dataclass
from typing import Tuple

from py_blender_room.framework.sceneobject import SceneObject


@dataclass
class Camera(SceneObject):
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]