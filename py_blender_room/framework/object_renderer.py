import abc

from py_blender_room.framework.sceneobject import SceneObject


class ObjectRenderer:
    @abc.abstractmethod
    def render_object(self, obj: SceneObject):
        pass

    @abc.abstractmethod
    def remove_default_objects(self):
        pass