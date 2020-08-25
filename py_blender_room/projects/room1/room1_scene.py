from dataclasses import dataclass
from math import sqrt
from typing import List, Tuple

from py_blender_room.framework.entity import Entity
from py_blender_room.framework.material import Material
from py_blender_room.framework.object import Object
from py_blender_room.framework.scene import Scene

WALL_MATERIAL_NAME: str = 'wall'
GLASS_MATERIAL_NAME: str = 'glass'
FLOOR_MATERIAL_NAME: str = 'floor'
CEILING_MATERIAL_NAME: str = 'ceiling'


@dataclass
class Window:
    width: float
    height: float
    margin_bottom: float
    margin_left: float
    material: Material
    thickness: float = 0.02


@dataclass
class Floor:
    size_x: float
    size_y: float
    material: Material


@dataclass
class Ceiling:
    size_x: float
    size_y: float
    height: float
    material: Material


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


@dataclass
class Sun(Object):
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]


@dataclass
class Camera(Object):
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]


class Room1Scene(Scene):
    PI = 3.14

    def __init__(self):
        self.size_x: float = 13
        self.size_y: float = 10
        self.height: float = 3

        super().__init__()

    def _build(self):
        window_material = Material(name=GLASS_MATERIAL_NAME, texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg')
        wall_material = Material(name=WALL_MATERIAL_NAME, texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg')
        floor_material = Material(name=FLOOR_MATERIAL_NAME, texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg');

        window1 = Window(margin_bottom=1, height=2, width=1.5, margin_left=1.01, material=window_material)
        window2 = Window(margin_bottom=1, height=2, width=1.5, margin_left=3.01, material=window_material)
        window3 = Window(margin_bottom=1, height=2, width=1.5, margin_left=5.01, material=window_material)

        wall_a = Wall(thickness=0.9, height=4, windows=[window1, window2, window3], x0=0, y0=self.size_y,
                      x1=self.size_x, y1=self.size_y)
        wall_a.material = wall_material

        wall_b = Wall(thickness=2, height=2, x0=0, y0=0, x1=2, y1=0, windows=[])
        wall_b.material = wall_material

        floor = Floor(size_x=self.size_x, size_y=self.size_y, material=floor_material)

        self.objects = [
            wall_a,
            floor,
            Sun(location=(0, 0, 5), rotation=(-1, 0, 0)),
            Camera(location=(self.size_x * 1, self.size_y / 2, 1), rotation=(self.PI / 2, 0, self.PI / 2 - 0.3))
        ]


