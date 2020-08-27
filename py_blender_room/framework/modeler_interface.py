from abc import ABC, abstractmethod
from typing import List, Tuple

from py_blender_room.framework.camera import Camera
from py_blender_room.framework.material import Material
from py_blender_room.framework.world_texture import WorldTexture


class ModelerInterface(ABC):

    @abstractmethod
    def remove_default_objects(self):
        pass

    @abstractmethod
    def add_object_to_default_collection(self, obj):
        pass

    @abstractmethod
    def select_one_object(self, obj):
        pass

    @abstractmethod
    def select_many_objects(self, objects: List):
        pass

    @abstractmethod
    def move_object(self, obj, x: float, y: float, z: float):
        pass

    @abstractmethod
    def scale_object(self, obj, scale: Tuple[float, float, float]):
        pass

    @abstractmethod
    def get_object_by_name(self, name: str):
        pass

    @abstractmethod
    def move_many_objects(self, objects: List, x: float, y: float, z: float):
        pass

    @abstractmethod
    def rotate_object_over_z(self, obj, angle: float):
        pass

    @abstractmethod
    def rotate_many_objects(self, objects: List, angle: float, axis: str, center: Tuple[float, float, float]):
        pass

    @abstractmethod
    def hide_object(self, obj):
        pass

    @abstractmethod
    def add_sun(self, source_point: Tuple[float, float, float], rotation: Tuple[float, float, float]):
        pass

    # noinspection PyTypeChecker
    @abstractmethod
    def create_material(self, material: Material):
        pass

    @abstractmethod
    def set_world_texture(self, texture: WorldTexture):
        pass

    @abstractmethod
    def add_camera(self, camera: Camera):
        pass

    @abstractmethod
    def create_box(self, size_x: float, size_y: float, size_z: float, name: str):
        pass

    @abstractmethod
    def cut_a_from_b(self, x, y):
        pass

    @abstractmethod
    def assign_material_to_object(self, material, obj):
        pass

    @abstractmethod
    def initialize(self):
        pass
