from dataclasses import dataclass
from typing import Tuple

from py_blender_room.framework.object import Object


@dataclass
class Camera(Object):
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]