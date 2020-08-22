import abc
from math import atan, asin
from pprint import pprint

import py_blender_room.blender.blender_utils
from py_blender_room.blender import blender_utils
from py_blender_room.framework.material import Material
from py_blender_room.framework.object import Object
from py_blender_room.framework.object_renderer import ObjectRenderer
from py_blender_room.projects.room1.room1_scene import Wall, WALL_MATERIAL_NAME, Window, GLASS_MATERIAL_NAME

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
        if material.name == GLASS_MATERIAL_NAME:
            mat.diffuse_color = (0.0, 0.00652415, 0.8, 0.1)
        return mat


class WallRenderingStrategy(ObjectRenderingStrategy):

    def render(self, wall: Wall):
        print('creating mesh for wall of width ' + str(wall.width))

        mesh = create_box_mesh(wall.thickness, wall.width, wall.height)
        wall_object = bpy.data.objects.new(generate_new_id(), mesh)

        blender_utils.add_object_to_default_collection(wall_object)

        # creating holes in the wall
        window_objects = []
        for window in wall.windows:
            self._cut_out_hole_for_window(wall, wall_object, window)
            window_objects.append(self._create_glass_for_window(wall, window))

        all_objects = [wall_object, *window_objects]

        material = MaterialRenderingStrategy().render(wall.material)
        wall_object.data.materials.append(material)

        blender_utils.move_many_objects(all_objects, wall.x0, wall.y0, 0)
        angle = -asin((wall.x1 - wall.x0) / wall.width)

        blender_utils.rotate_many_objects(all_objects, angle, 'Z')

    def _cut_out_hole_for_window(self, wall: Wall, wall_object, window: Window):
        mesh = create_box_mesh(wall.thickness * 3, window.width, window.height)
        window_object_id = "window_cutter_" + generate_new_id()
        window_cutter_object = bpy.data.objects.new(window_object_id, mesh)
        blender_utils.add_object_to_default_collection(window_cutter_object)
        # blender_utils.select_one_object(wall_object)
        modifier_name = "cut out window " + window_object_id
        modifier = wall_object.modifiers.new(type="BOOLEAN", name=modifier_name)
        modifier.object = window_cutter_object
        modifier.operation = 'DIFFERENCE'
        blender_utils.move_object(window_cutter_object, -wall.thickness, window.margin_left, window.margin_bottom)

        bpy.context.view_layer.objects.active = bpy.data.objects[wall_object.name]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
        bpy.data.objects.remove(window_cutter_object, do_unlink=True)

    def _create_glass_for_window(self, wall: Wall, window: Window):
        mesh = create_box_mesh(window.thickness, window.width, window.height)
        glass_object_id = "window_glass_" + generate_new_id()
        glass_object = bpy.data.objects.new(glass_object_id, mesh)
        blender_utils.add_object_to_default_collection(glass_object)

        blender_utils.move_object(glass_object, 0, window.margin_left, window.margin_bottom)

        material = MaterialRenderingStrategy().render(window.material)
        glass_object.data.materials.append(material)

        return glass_object


class Room1ObjectRenderer(ObjectRenderer):

    def __init__(self):
        self._initialized: bool = False

    def render_object(self, obj: Object):

        if not self._initialized:
            self._initialize()

        if isinstance(obj, Wall):
            WallRenderingStrategy().render(obj)

    def _initialize(self):
        blender_utils.remove_default_objects()
        pass
