from framework.object import Object
from framework.object_renderer import ObjectRenderer


class Room1ObjectRenderer(ObjectRenderer):
    def render_object(self, obj: Object):
        print('preved ' + str(type(obj)))
