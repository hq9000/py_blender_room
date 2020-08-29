import abc
from typing import List, Optional

from py_blender_room.framework.sceneobject import SceneObject
from py_blender_room.framework.world_texture import WorldTexture


class Scene:

    def __init__(self):
        self.objects: List[SceneObject] = []
        self.world_texture: Optional[WorldTexture] = None

    @abc.abstractmethod
    def build(self):
        pass
