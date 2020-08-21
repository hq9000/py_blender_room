from py_blender_room.framework.object_renderer import ObjectRenderer
from py_blender_room.framework.scene import Scene


class SceneRenderer:

    def render(self, scene: Scene, object_renderer: ObjectRenderer):
        for obj in scene.objects:
            object_renderer.render_object(obj)
