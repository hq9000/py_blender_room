from dataclasses import dataclass
from math import sqrt
from typing import List

from framework.entity import Entity
from framework.point import Point
from framework.scene import Scene


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

        wall_a = Wall(thickness=0.2, height=5, windows=[window], x0=0, y0=0, x1=10, y1=10)
        self.objects.append(wall_a)
