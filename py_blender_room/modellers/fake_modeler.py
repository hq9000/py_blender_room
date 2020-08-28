from typing import Tuple, List

from py_blender_room.framework.camera import Camera
from py_blender_room.framework.material import Material
from py_blender_room.framework.modeler_interface import ModelerInterface
from py_blender_room.framework.world_texture import WorldTexture


class FakeModeler(ModelerInterface):
    def initialize(self):
        pass

    def remove_default_objects(self):
        pass

    def add_object_to_default_collection(self, obj):
        pass

    def select_one_object(self, obj):
        pass

    def select_many_objects(self, objects: List):
        pass

    def move_object(self, obj, x: float, y: float, z: float):
        pass

    def scale_object(self, obj, scale: Tuple[float, float, float]):
        pass

    def get_object_by_name(self, name: str):
        pass

    def move_many_objects(self, objects: List, x: float, y: float, z: float):
        pass

    def rotate_object_over_z(self, obj, angle: float):
        pass

    def rotate_many_objects(self, objects: List, angle: float, axis: str, center: Tuple[float, float, float]):
        pass

    def hide_object(self, obj):
        pass

    def add_sun(self, source_point: Tuple[float, float, float], rotation: Tuple[float, float, float]):
        pass

    def create_material(self, material: Material):
        pass

    def set_world_texture(self, texture: WorldTexture):
        pass

    def add_camera(self, camera: Camera):
        pass

    def create_box(self, size_x: float, size_y: float, size_z: float, name: str):
        pass

    def cut_a_from_b(self, x, y):
        pass

    def assign_material_to_object(self, material, obj):
        pass

