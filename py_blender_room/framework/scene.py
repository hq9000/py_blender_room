import abc
from typing import List, Optional

from py_blender_room.framework.object import Object
from py_blender_room.framework.world_texture import WorldTexture


class Scene:

    def __init__(self):
        self.objects: List[Object] = []
        self.world_texture: Optional[WorldTexture] = None
        self._build()

    @abc.abstractmethod
    def _build(self):
        pass
