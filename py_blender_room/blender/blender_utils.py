import os
from typing import List, Tuple

import bpy
from py_blender_room.framework.material import Material
from py_blender_room.framework.world_texture import WorldTexture


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


def scale_object(obj, scale: Tuple[float, float, float]):
    select_one_object(obj)
    # bpy.ops.transform.resize(list(scale))


def get_object_by_name(name: str):
    return bpy.data.objects[name]


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


# noinspection PyTypeChecker
def create_material(material: Material):
    blender_material = bpy.data.materials.new(name=material.name)
    blender_material.use_nodes = True

    nodes = blender_material.node_tree.nodes
    links = blender_material.node_tree.links

    bsdf_node = nodes["Principled BSDF"]
    texture_coordinate_node = nodes.new("ShaderNodeTexCoord")
    texture_node = nodes.new(type="ShaderNodeTexImage")
    texture_node.projection = 'BOX'

    mapping_node = nodes.new(type="ShaderNodeMapping")
    material_output_node = nodes["Material Output"]

    if material.texture_file_path is not None:

        filename = os.path.basename(material.texture_file_path)

        bpy.ops.image.open(filepath=material.texture_file_path,
                           files=[
                               {
                                   "name": filename
                               }
                           ],
                           relative_path=True, show_multiview=False)

        image = bpy.data.images[filename]

        texture_node.image = image
        links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])

        if material.use_texture_for_displacement is True:
            links.new(texture_node.outputs['Color'], material_output_node.inputs['Displacement'])

        links.new(texture_coordinate_node.outputs['Generated'], mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])

        mapping_node.inputs['Scale'].default_value = list(material.scale)
        mapping_node.inputs['Rotation'].default_value = list(material.rotation)

    bsdf_node.inputs['Metallic'].default_value = material.metallic
    bsdf_node.inputs['Roughness'].default_value = material.roughness
    bsdf_node.inputs['Alpha'].default_value = material.alpha
    return blender_material

    # bpy.context.space_data.context = 'MATERIAL'
    # bpy.ops.node.add_node(type="ShaderNodeTexCoord", use_transform=True)


def set_world_texture(self, texture: WorldTexture):
    node_tree = bpy.data.worlds['World'].node_tree

    nodes = node_tree.nodes
    links = node_tree.links

    nodes.remove(nodes['Background'])  # removing the default node
