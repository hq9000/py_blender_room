import abc

from framework.object import Object
from framework.object_renderer import ObjectRenderer
from projects.room1.room1_scene import Wall

import bpy


class RenderingStrategy:
    @abc.abstractmethod
    def render(self, obj: Object):
        pass


_id: int = 0


def generate_new_id() -> str:
    global _id
    _id += 1
    return str(_id)


def create_box_mesh(size_x: float, size_y: float, size_z: float):
    """

    http://i.imgur.com/t0VGg09.png

    :param size_x:
    :param size_y:
    :param size_z:
    :return:
    """
    points = [
        [0, 0, 0],
        [size_x, 0, 0],
        [size_x, size_y, 0],
        [0, size_y, 0],

        [0, 0, size_z],
        [size_x, 0, size_z],
        [size_x, size_y, size_z],
        [0, size_y, size_z],
    ]

    faces = [
        [1, 6, 5], [1, 6, 2],
        [4, 6, 7], [7, 4, 3],
        [3, 8, 4], [3, 7, 8],
        [5, 8, 7], [5, 6, 7],
        [1, 5, 8], [8, 1, 4],
        [1, 4, 3], [1, 2, 3],
    ]

    return bpy.data.meshes.new(generate_new_id())


class WallRenderingStrategy(RenderingStrategy):

    def render(self, wall: Wall):
        mesh = create_box_mesh(wall.thickness, wall.width, wall.height)


class Room1ObjectRenderer(ObjectRenderer):
    def render_object(self, obj: Object):
        if isinstance(obj, Wall):
            WallRenderingStrategy().render(obj)
