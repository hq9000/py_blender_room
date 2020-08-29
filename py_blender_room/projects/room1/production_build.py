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

    scene.path_to_sky_texture = '/home/sergey/Downloads/autumn_park_4k.hdr'
    scene.path_to_floor_texture = '/home/sergey/Downloads/parquet.jpg'
    scene.path_to_wall_texture = '/home/sergey/Downloads/damask-seamless-pattern-background_1217-1269.jpg'
    scene.path_to_ceiling_texture = '/home/sergey/Downloads/ceiling_texture.jpg'
    scene.needs_sun = False

    scene.build()
    modeler = Blender()
    scene_renderer = Room1SceneRenderer()
    scene_renderer.modeler = modeler
    scene_renderer.render(scene)


# this script is supposed to be run with modellers, e.g.:
# ~/dist/modellers-2.83.4-linux64/modellers --python ~/room/py_blender_room/projects/room1/build.py -b
if __name__ == '__main__':
    run()
