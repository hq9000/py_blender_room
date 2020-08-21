from typing import Optional

from py_blender_room.framework.material import Material
from py_blender_room.framework.object import Object


class Entity(Object):

    def __init__(self):
        self.material: Optional[Material] = None
