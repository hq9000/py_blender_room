from typing import Optional

from py_blender_room.framework.material import Material
from py_blender_room.framework.sceneobject import SceneObject


class Entity(SceneObject):

    def __init__(self):
        self.material: Optional[Material] = None
