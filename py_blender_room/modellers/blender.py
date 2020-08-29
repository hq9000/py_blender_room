import os
from typing import List, Tuple

import bpy
from py_blender_room.framework.camera import Camera
from py_blender_room.framework.material import Material
from py_blender_room.framework.modeler_interface import ModelerInterface
from py_blender_room.framework.world_texture import WorldTexture


# noinspection PyTypeChecker
class Blender(ModelerInterface):

    def initialize(self):
        scene = bpy.data.scenes['Scene']
        scene.render.engine = 'CYCLES'
        scene.view_settings.look = 'High Contrast'

    def remove_default_objects(self):
        # noinspection PyTypeChecker
        bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)
        # noinspection PyTypeChecker
        bpy.data.objects.remove(bpy.data.objects['Camera'], do_unlink=True)
        # noinspection PyTypeChecker
        bpy.data.objects.remove(bpy.data.objects['Light'], do_unlink=True)

    def add_object_to_default_collection(self, obj):
        col = bpy.data.collections.get("Collection")
        col.objects.link(obj)

    def select_one_object(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]

    def select_many_objects(self, objects: List):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)

    def move_object(self, obj, x: float, y: float, z: float):
        self.select_one_object(obj)
        bpy.ops.transform.translate(value=[x, y, z])

    def scale_object(self, obj, scale: Tuple[float, float, float]):
        self.select_one_object(obj)
        # bpy.ops.transform.resize(list(scale))

    def get_object_by_name(self, name: str):
        return bpy.data.objects[name]

    def move_many_objects(self, objects: List, x: float, y: float, z: float):
        self.select_many_objects(objects)
        bpy.ops.transform.translate(value=[x, y, z])

    def rotate_object_over_z(self, obj, angle: float):
        self.select_one_object(obj)
        bpy.ops.transform.rotate(value=angle, orient_axis='Z')

    def rotate_many_objects(self, objects: List, angle: float, axis: str, center: Tuple[float, float, float]):
        self.select_many_objects(objects)
        bpy.ops.transform.rotate(value=angle, orient_axis=axis, orient_type='GLOBAL', center_override=list(center))

    def hide_object(self, obj):
        obj.hide_set(True)

    def add_sun(self, source_point: Tuple[float, float, float], rotation: Tuple[float, float, float]):
        bpy.ops.object.light_add(type="SUN", location=list(source_point), rotation=list(rotation))

    # noinspection PyTypeChecker
    def create_material(self, material: Material):
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

            image = self._open_image(material.texture_file_path)

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
        nodes.remove(nodes['Background'])  # removing the default node

        links = node_tree.links
        environment_texture_node = nodes.new(type="ShaderNodeTexEnvironment")
        mapping_node = nodes.new(type="ShaderNodeMapping")

        mapping_node.inputs['Rotation'].default_value = list(texture.rotation)
        mapping_node.inputs['Scale'].default_value = list(texture.scale)
        mapping_node.inputs['Location'].default_value = list(texture.location)

        texture_coordinate_node = nodes.new("ShaderNodeTexCoord")

        image = self._open_image(texture.path_to_texture_file)
        environment_texture_node.image = image

        links.new(environment_texture_node.outputs['Color'], nodes['World Output'].inputs['Surface'])
        links.new(texture_coordinate_node.outputs['Generated'], mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], environment_texture_node.inputs['Vector'])

    def add_camera(self, camera: Camera):
        bpy.ops.object.camera_add(location=list(camera.location), rotation=list(camera.rotation))

    def create_box(self, size_x: float, size_y: float, size_z: float, name: str):
        self._log('creating box named ' + name)
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=[0.5, 0.5, 0.5])
        bpy.ops.transform.resize(value=list((size_x, size_y, size_z)), center_override=[0, 0, 0], orient_type='GLOBAL')
        obj = bpy.context.selected_objects[0]
        obj.name = name
        return obj

    def cut_a_from_b(self, x, y):
        modifier_name = "cut_x_from_y"
        modifier = y.modifiers.new(type="BOOLEAN", name=modifier_name)
        modifier.object = x
        modifier.operation = 'DIFFERENCE'

        bpy.context.view_layer.objects.active = bpy.data.objects[y.name]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)
        bpy.data.objects.remove(x, do_unlink=True)

    def assign_material_to_object(self, material, obj):
        obj.data.materials.append(material)

    def _log(self, message: str):
        print(message)

    def _open_image(self, image_file_path) -> object:
        filename = os.path.basename(image_file_path)

        bpy.ops.image.open(filepath=image_file_path,
                           files=[
                               {
                                   "name": filename
                               }
                           ],
                           relative_path=True, show_multiview=False)

        return bpy.data.images[filename]
