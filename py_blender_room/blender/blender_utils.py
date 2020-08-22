import bpy


def remove_default_objects():
    # noinspection PyTypeChecker
    # bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)
    pass


def add_object_to_default_collection(obj):
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)


def select_one_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]


def move_object(obj, x: float, y: float, z: float):
    select_one_object(obj)
    bpy.ops.transform.translate(value=[x, y, z])


def rotate_object_over_z(obj, angle: float):
    select_one_object(obj)
    bpy.ops.transform.rotate(value=angle, orient_axis='Z')


def hide_object(obj):
    obj.hide_set(True)
