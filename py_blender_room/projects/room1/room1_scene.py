from dataclasses import dataclass
from math import sqrt
from typing import List

from py_blender_room.framework.entity import Entity
from py_blender_room.framework.material import Material
from py_blender_room.framework.scene import Scene

WALL_MATERIAL_NAME: str = 'wall'


@dataclass
class Window:
    width: float
    height: float
    margin_bottom: float
    margin_left: float


@dataclass
class Wall(Entity):
    thickness: float
    height: float
    x0: float
    y0: float
    x1: float
    y1: float
    windows: List[Window]

    @property
    def width(self) -> float:
        delta_x = self.x1 - self.x0
        delta_y = self.y1 - self.y0
        return sqrt(pow(delta_x, 2) + pow(delta_y, 2))


class Room1Scene(Scene):
    def _build(self):
        window = Window(margin_bottom=1, height=2, width=1.5, margin_left=1)

        wall_material = Material(name=WALL_MATERIAL_NAME)


        wall_a = Wall(thickness=0.2, height=2, windows=[window], x0=2, y0=3, x1=5, y1=3)
        wall_a.material = wall_material

        wall_b = Wall(thickness=0.2, height=2, windows=[window], x0=5, y0=3, x1=1, y1=10)
        wall_b.material = wall_material

        self.objects.append(wall_a)
        self.objects.append(wall_b)
