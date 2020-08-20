from typing import Optional

from framework.material import Material
from framework.object import Object


class Entity(Object):

    def __init__(self):
        self.material: Optional[Material] = None
