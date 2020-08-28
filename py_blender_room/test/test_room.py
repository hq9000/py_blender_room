import unittest

from py_blender_room.modellers.fake_modeler import FakeModeler
from py_blender_room.projects.room1.room1_scene import Room1Scene
from py_blender_room.projects.room1.room1_scene_renderer import Room1SceneRenderer


class TestWithFakeModeller(unittest.TestCase):
    def test_room1_fake_modeller(self):
        scene = Room1Scene()
        scene.build()
        modeler = FakeModeler()
        scene_renderer = Room1SceneRenderer()
        scene_renderer.modeler = modeler
        scene_renderer.render(scene)


if __name__ == '__main__':
    unittest.main()
