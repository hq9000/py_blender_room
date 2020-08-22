import abc

from py_blender_room.framework.object import Object


class ObjectRenderer:
    @abc.abstractmethod
    def render_object(self, obj: Object):
        pass

    @abc.abstractmethod
    def remove_default_objects(self):
        pass