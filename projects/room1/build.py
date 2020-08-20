from framework.scene_renderer import SceneRenderer
from projects.room1.room1_renderer import Room1ObjectRenderer
from projects.room1.room1_scene import Room1Scene

scene = Room1Scene()

object_renderer = Room1ObjectRenderer()
renderer = SceneRenderer()

renderer.render(scene, object_renderer)
