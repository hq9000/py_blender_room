from py_blender_room.blender import blender_utils
from py_blender_room.framework.object_renderer import ObjectRenderer
from py_blender_room.framework.scene import Scene


class SceneRenderer:

    def render(self, scene: Scene, object_renderer: ObjectRenderer):

        if scene.world_texture is not None:
            blender_utils.set_world_texture(scene.world_texture)

        for obj in scene.objects:
            object_renderer.render_object(obj)

        object_renderer.remove_default_objects()
