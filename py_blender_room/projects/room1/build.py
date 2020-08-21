import os
import sys

sys.path.append(
    os.path.dirname(os.path.realpath(__file__)) + '/../../../'
)

from py_blender_room.framework.scene_renderer import SceneRenderer
from py_blender_room.projects.room1.room1_renderer import Room1ObjectRenderer
from py_blender_room.projects.room1.room1_scene import Room1Scene


def run():
    scene = Room1Scene()
    object_renderer = Room1ObjectRenderer()
    renderer = SceneRenderer()
    renderer.render(scene, object_renderer)


# this script is supposed to be run with blender, e.g.:
# ~/dist/blender-2.83.4-linux64/blender --python ~/room/py_blender_room/projects/room1/build.py -b
if __name__ == '__main__':
    run()
