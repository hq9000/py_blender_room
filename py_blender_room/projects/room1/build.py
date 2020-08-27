import os
import sys

sys.path.append(
    os.path.dirname(os.path.realpath(__file__)) + '/../../../'
)



from py_blender_room.modellers.blender import Blender
from py_blender_room.modellers.fake_modeler import FakeModeler
from py_blender_room.projects.room1.room1_scene_renderer import Room1SceneRenderer
from py_blender_room.projects.room1.room1_scene import Room1Scene


def run():
    scene = Room1Scene()
    scene.build()
    modeler = Blender()
    scene_renderer = Room1SceneRenderer()
    scene_renderer.modeler = modeler
    scene_renderer.render(scene)


# this script is supposed to be run with modellers, e.g.:
# ~/dist/modellers-2.83.4-linux64/modellers --python ~/room/py_blender_room/projects/room1/build.py -b
if __name__ == '__main__':
    run()
