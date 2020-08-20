from dataclasses import dataclass

from framework.entity import Entity
from framework.scene import Scene


@dataclass
class Wall(Entity):
    thickness: float
    height: float
    width: float


class Room1Scene(Scene):
    def _build(self):
        self.objects.append(Wall(thickness=0.2, height=5, width=10))
