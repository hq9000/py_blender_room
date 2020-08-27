from abc import ABC, abstractmethod
from dataclasses import dataclass

from py_blender_room.framework.modeler_interface import ModelerInterface
from py_blender_room.modellers import blender
from py_blender_room.framework.object_renderer import ObjectRenderer
from py_blender_room.framework.scene import Scene


@dataclass
class SceneRenderer(ABC):
    modeler: ModelerInterface

    @abstractmethod
    def _render_object(self, obj):
        pass

    def render(self, scene: Scene):

        if scene.world_texture is not None:
            self.modeler.set_world_texture(scene.world_texture)

        for obj in scene.objects:
            self.render_object(obj)

        self.modeler.remove_default_objects()
