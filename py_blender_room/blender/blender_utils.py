from typing import List, Tuple

import bpy


def remove_default_objects():
    # noinspection PyTypeChecker
    bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)
    # noinspection PyTypeChecker
    bpy.data.objects.remove(bpy.data.objects['Camera'], do_unlink=True)
    # noinspection PyTypeChecker
    bpy.data.objects.remove(bpy.data.objects['Light'], do_unlink=True)


def add_object_to_default_collection(obj):
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)


def select_one_object(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]


def select_many_objects(objects: List):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)


def move_object(obj, x: float, y: float, z: float):
    select_one_object(obj)
    bpy.ops.transform.translate(value=[x, y, z])


def move_many_objects(objects: List, x: float, y: float, z: float):
    select_many_objects(objects)
    bpy.ops.transform.translate(value=[x, y, z])


def rotate_object_over_z(obj, angle: float):
    select_one_object(obj)
    bpy.ops.transform.rotate(value=angle, orient_axis='Z')


def rotate_many_objects(objects: List, angle: float, axis: str, center: Tuple[float, float, float]):
    select_many_objects(objects)
    bpy.ops.transform.rotate(value=angle, orient_axis=axis, orient_type='GLOBAL', center_override=list(center))


def hide_object(obj):
    obj.hide_set(True)


def add_sun(source_point: Tuple[float, float, float], target_point: Tuple[float, float, float]):
    bpy.ops.object.light_add(type="SUN", location=list(source_point))
