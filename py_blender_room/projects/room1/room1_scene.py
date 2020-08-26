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
        self.wall_thickness = 0.1
        self.margin_left_of_first_window = 0.3
        self.distance_between_windows = 0.1
        self.window_width: float = 3
        self.window_margin_top: float = 0.3
        self.window_margin_bottom: float = 0.3
        self.num_windows: int = 3
        self.size_x: float = 13
        self.size_y: float = 10
        self.height: float = 3

        super().__init__()

    def _build(self):
        window_material = Material(name=GLASS_MATERIAL_NAME,
                                   texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg')
        wall_material = Material(
            name=WALL_MATERIAL_NAME,
            texture_file_path='/home/sergey/Downloads/damask-seamless-pattern-background_1217-1269.jpg',
            metallic=0.2,
            scale=(7, 7, 3.5),
            displacement=False
        )

        floor_material = Material(name=FLOOR_MATERIAL_NAME,
                                  texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg',
                                  scale=(4, 2, 2))

        ceiling_material = Material(name=CEILING_MATERIAL_NAME,
                                    texture_file_path='/home/sergey/Downloads/seamless-wood-floor-texture-free.jpg',
                                    scale=(4, 2, 2))

        windows: List[Window] = []

        for i in range(0, self.num_windows):
            windows.append(Window(margin_bottom=self.window_margin_bottom, height=self.height - self.window_margin_top - self.window_margin_bottom,
                                  width=self.window_width,
                                  margin_left=self.margin_left_of_first_window + i * (
                                          self.window_width + self.distance_between_windows),
                                  material=window_material),
                           )

        wall_a = Wall(thickness=self.wall_thickness, height=self.height, windows=windows, x0=0, y0=self.size_y,
                      x1=self.size_x, y1=self.size_y)
        wall_a.material = wall_material

        wall_b = Wall(thickness=2, height=2, x0=0, y0=0, x1=2, y1=0, windows=[])
        wall_b.material = wall_material

        floor = Floor(size_x=self.size_x, size_y=self.size_y, material=floor_material)
        ceiling = Ceiling(size_x=self.size_x, size_y=self.size_y, height=self.height, material=ceiling_material)

        self.objects = [
            wall_a,
            floor,
            ceiling,
            Sun(location=(0, 0, 5), rotation=(-1, 0, 0)),
            Camera(location=(self.size_x * 1, self.size_y / 2, 1), rotation=(self.PI / 2, 0, self.PI / 2 - 0.3))
        ]
