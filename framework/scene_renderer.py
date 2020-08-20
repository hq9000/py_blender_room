from framework.entity import Entity
from framework.object import Object
from framework.object_renderer import ObjectRenderer
from framework.scene import Scene


class SceneRenderer:

    def render(self, scene: Scene, object_renderer: ObjectRenderer):
        for obj in scene.objects:
            object_renderer.render_object(obj)
