import os
from dataclasses import dataclass
from math import sqrt
from typing import List, Tuple, Optional

from py_blender_room.framework.camera import Camera
from py_blender_room.framework.entity import Entity
from py_blender_room.framework.material import Material
from py_blender_room.framework.sceneobject import SceneObject
from py_blender_room.framework.scene import Scene
from py_blender_room.framework.world_texture import WorldTexture

WALL_MATERIAL_NAME: str = 'wall'
GLASS_MATERIAL_NAME: str = 'glass'
FLOOR_MATERIAL_NAME: str = 'floor'
TABLE_MATERIAL_NAME: str = 'table'
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
class Table(Entity):
    location: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    thickness: float = 0.1
    width: float = 1
    height: float = 0.5
    depth: float = 0.3


@dataclass
class Sun(SceneObject):
    location: Tuple[float, float, float] = (0, 0, 0)
    rotation: Tuple[float, float, float] = (0, 0, 0)


def degrees_to_radians(degrees: float) -> float:
    return degrees / 180 * 3.14


class Room1Scene(Scene):
    PI = 3.14

    def __init__(self):
        super().__init__()

        resources_dir: str = os.path.dirname(os.path.realpath(__file__)) + '/resources'

        self.wall_thickness = 0.1
        self.margin_left_of_first_window = 0.3
        self.distance_between_windows = 0.3
        self.window_width: float = 3
        self.window_margin_top: float = 0.3
        self.window_margin_bottom: float = 0.3
        self.num_windows: int = 13
        self.size_x: float = 33
        self.size_y: float = 10
        self.height: float = 3
        self.needs_sun: bool = True

        self.path_to_floor_texture = resources_dir + '/parquet_texture.jpg'
        self.path_to_sky_texture = resources_dir + '/sky_texture.jpg'
        self.path_to_ceiling_texture = resources_dir + '/ceiling_texture.jpg'
        self.path_to_wall_texture = resources_dir + '/wallpaper_texture.jpg'

    def build(self):
        self.world_texture: Optional[WorldTexture] = WorldTexture(
            path_to_texture_file=self.path_to_sky_texture,
            rotation=(degrees_to_radians(75), degrees_to_radians(29), degrees_to_radians(-40))
        )

        window_material = Material(name=GLASS_MATERIAL_NAME,
                                   metallic=1.0,
                                   alpha=0.1,
                                   roughness=0.1,
                                   texture_file_path=None)
        wall_material = Material(
            name=WALL_MATERIAL_NAME,
            texture_file_path=self.path_to_wall_texture,
            metallic=0.2,
            scale=(7, 7, 3.5),
            use_texture_for_displacement=False
        )

        table_material = Material(
            name=TABLE_MATERIAL_NAME,
            texture_file_path=self.path_to_wall_texture,
            metallic=0.2,
            scale=(7, 7, 3.5),
            use_texture_for_displacement=False
        )

        table_width = 2.1
        table = Table(thickness=0.03, width=2.1, height=1, depth=1.2,
                      location=(1, self.size_y / 2 - table_width / 2, 0))
        table.material = table_material

        floor_material = Material(name=FLOOR_MATERIAL_NAME,
                                  texture_file_path=self.path_to_floor_texture,
                                  scale=(25, 8, 1))

        ceiling_material = Material(name=CEILING_MATERIAL_NAME,
                                    texture_file_path=self.path_to_ceiling_texture,
                                    metallic=0,
                                    use_texture_for_displacement=True,
                                    scale=(12, 8, 8))

        windows: List[Window] = []

        for i in range(0, self.num_windows):
            windows.append(Window(margin_bottom=self.window_margin_bottom,
                                  height=self.height - self.window_margin_top - self.window_margin_bottom,
                                  width=self.window_width,
                                  margin_left=self.margin_left_of_first_window + i * (
                                          self.window_width + self.distance_between_windows),
                                  material=window_material),
                           )

        wall_right = Wall(thickness=self.wall_thickness, height=self.height, windows=windows, x0=0, y0=self.size_y,
                          x1=self.size_x, y1=self.size_y)
        wall_right.material = wall_material

        wall_front = Wall(thickness=self.wall_thickness, height=self.height, windows=[], x0=0, y0=0,
                          x1=0, y1=self.size_y)
        wall_front.material = wall_material

        wall_left = Wall(thickness=self.wall_thickness, height=self.height, windows=[], x0=0, y0=0,
                         x1=self.size_x, y1=0)
        wall_left.material = wall_material

        wall_back = Wall(thickness=self.wall_thickness, height=self.height, windows=[], x0=self.size_x, y0=0,
                         x1=self.size_x, y1=self.size_y)
        wall_back.material = wall_material

        floor = Floor(size_x=self.size_x, size_y=self.size_y, material=floor_material)
        ceiling = Ceiling(size_x=self.size_x, size_y=self.size_y, height=self.height, material=ceiling_material)

        objects: List[SceneObject] = [
            wall_right, wall_front, wall_left, wall_back,
            floor,
            ceiling,
            Camera(location=(self.size_x * 0.8, self.size_y / 2, 1), rotation=(self.PI / 2, 0, self.PI / 2))
        ]

        if self.needs_sun:
            objects.append(Sun(rotation=(degrees_to_radians(-45), degrees_to_radians(45), 0)))

        self.objects = objects
