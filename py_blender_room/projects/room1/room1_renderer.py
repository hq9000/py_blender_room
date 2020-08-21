import abc
from math import atan

from py_blender_room.blender.utils import remove_default_objects
from py_blender_room.framework.material import Material
from py_blender_room.framework.object import Object
from py_blender_room.framework.object_renderer import ObjectRenderer
from py_blender_room.projects.room1.room1_scene import Wall, WALL_MATERIAL_NAME

import bpy


class ObjectRenderingStrategy:
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
        [0, 0, 0],  # 0
        [size_x, 0, 0],  # 1
        [size_x, size_y, 0],  # 2
        [0, size_y, 0],  # 3

        [0, 0, size_z],  # 4
        [size_x, 0, size_z],  # 5
        [size_x, size_y, size_z],  # 6
        [0, size_y, size_z],  # 7
    ]

    faces = [
        [0, 5, 4], [0, 1, 5],  # A
        [1, 2, 6], [1, 6, 5],  # B
        [3, 2, 7], [2, 7, 6],  # C
        [4, 5, 6], [4, 6, 7],  # D
        [0, 7, 4], [0, 3, 7],  # E
        [0, 3, 2], [2, 1, 0],  # F
    ]

    mesh = bpy.data.meshes.new(generate_new_id())
    mesh.from_pydata(points, [], faces)

    return mesh


class MaterialRenderingStrategy:
    def render(self, material: Material):
        mat = bpy.data.materials.new(name=generate_new_id())
        mat.use_nodes = True
        if material.name == WALL_MATERIAL_NAME:
            mat.diffuse_color = (0.8, 0.00652415, 0, 1)

        return mat


class WallRenderingStrategy(ObjectRenderingStrategy):

    def render(self, wall: Wall):
        mesh = create_box_mesh(wall.thickness, wall.width, wall.height)
        obj = bpy.data.objects.new(generate_new_id(), mesh)

        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)

        material = MaterialRenderingStrategy().render(wall.material)
        obj.data.materials.append(material)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.ops.transform.translate(value=[wall.x0, wall.y0, 0])
        angle = atan((wall.y1 - wall.y0) / (wall.x1 - wall.x0))
        bpy.ops.transform.rotate(value=1.0 * angle, orient_axis='Z')


class Room1ObjectRenderer(ObjectRenderer):

    def __init__(self):
        self._initialized: bool = False

    def render_object(self, obj: Object):

        if not self._initialized:
            self._initialize()

        if isinstance(obj, Wall):
            WallRenderingStrategy().render(obj)

    def _initialize(self):
        remove_default_objects()
        pass
