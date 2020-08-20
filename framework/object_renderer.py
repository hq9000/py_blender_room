import abc

from framework.object import Object


class ObjectRenderer:
    @abc.abstractmethod
    def render_object(self, obj: Object):
        pass
