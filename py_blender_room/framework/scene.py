import abc
from typing import List

from py_blender_room.framework.object import Object


class Scene:

    def __init__(self):
        self.objects: List[Object] = []
        self._build()

    @abc.abstractmethod
    def _build(self):
        pass
