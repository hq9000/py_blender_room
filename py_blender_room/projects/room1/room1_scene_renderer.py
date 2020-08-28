from math import asin
from typing import Dict

from py_blender_room.framework.scene_renderer import SceneRenderer
from py_blender_room.framework.material import Material
from py_blender_room.framework.object import Object
from py_blender_room.projects.room1.room1_scene import Wall, Window, Floor, \
    Sun, Camera, Ceiling, Table


class Room1SceneRenderer(SceneRenderer):
    _id_cursor: int = 0

    def _render_object(self, obj: Object):
        if isinstance(obj, Wall):
            self._render_wall(obj)
        elif isinstance(obj, Floor):
            self._render_floor(obj)
        elif isinstance(obj, Ceiling):
            self._render_ceiling(obj)
        elif isinstance(obj, Sun):
            self._render_sun(obj)
        elif isinstance(obj, Camera):
            self._render_camera(obj)
        elif isinstance(obj, Table):
            self._render_table(obj)
        else:
            raise Exception(f"don't know how to deal with objects of this class: {type(obj)}")

    def __init__(self):
        self._material_registry: Dict = {}

    @classmethod
    def _generate_new_id(cls, prefix: str) -> str:
        cls._id_cursor += 1
        return prefix + '_' + str(cls._id_cursor)

    def _cut_out_hole_for_window(self, wall: Wall, wall_object, window: Window):
        window_cutter_object = self.modeler.create_box(wall.thickness * 3, window.width, window.height,
                                                       self._generate_new_id('window_cutter'))
        self.modeler.move_object(window_cutter_object, -wall.thickness, window.margin_left, window.margin_bottom)
        self.modeler.cut_a_from_b(window_cutter_object, wall_object)

    def _create_glass_for_window(self, window: Window):
        glass_object = self.modeler.create_box(window.thickness, window.width, window.height,
                                               self._generate_new_id('window_glass'))
        self.modeler.move_object(glass_object, 0, window.margin_left, window.margin_bottom)
        material = self._get_modeler_material(window.material)
        self.modeler.assign_material_to_object(material, glass_object)

        return glass_object

    def _get_modeler_material(self, material: Material):

        if material not in self._material_registry:
            self._material_registry[material] = self.modeler.create_material(material)

        return self._material_registry[material]

    def _render_wall(self, wall: Wall):

        self._log('creating mesh for wall of width ' + str(wall.width))

        wall_object = self.modeler.create_box(wall.thickness, wall.width, wall.height, self._generate_new_id('wall'))

        # creating holes in the wall
        window_glass_objects = []
        for window in wall.windows:
            self._cut_out_hole_for_window(wall, wall_object, window)
            window_glass_objects.append(self._create_glass_for_window(window))

        all_objects = [wall_object, *window_glass_objects]

        material = self._get_modeler_material(wall.material)
        self.modeler.assign_material_to_object(material, wall_object)

        angle = -asin((wall.x1 - wall.x0) / wall.width)
        self.modeler.rotate_many_objects(all_objects, angle, 'Z', (0, 0, 0))
        self.modeler.move_many_objects(all_objects, wall.x0, wall.y0, 0)

    def _log(self, message: str):
        print(message)

    def _render_floor(self, floor: Floor):
        box = self.modeler.create_box(floor.size_x, floor.size_y, 0.02, self._generate_new_id('floor'))
        material = self._get_modeler_material(floor.material)
        self.modeler.assign_material_to_object(material, box)

    def _render_ceiling(self, ceiling: Ceiling):
        box = self.modeler.create_box(ceiling.size_x, ceiling.size_y, 0.02, self._generate_new_id('ceiling'))
        self.modeler.move_object(box, 0, 0, ceiling.height)
        material = self._get_modeler_material(ceiling.material)
        self.modeler.assign_material_to_object(material, box)

    def _render_sun(self, obj: Sun):
        self.modeler.add_sun(obj.location, obj.rotation)

    def _render_camera(self, obj: Camera):
        self.modeler.add_camera(obj)

    def _render_table(self, obj: Table):

        margin: float = 0.05
        spacer_height = 0.4
        top = self.modeler.create_box(obj.depth, obj.width, obj.thickness, self._generate_new_id('table_top'))
        self.modeler.move_object(top, 0, 0, obj.height)

        right_stand = self.modeler.create_box(obj.depth * (1 - 2 * margin), obj.thickness, obj.height,
                                              self._generate_new_id('table_right_stand'))
        left_stand = self.modeler.create_box(obj.depth * (1 - 2 * margin), obj.thickness, obj.height,
                                             self._generate_new_id('table_right_stand'))

        spacer = self.modeler.create_box(obj.thickness, obj.width * (1 - 2 * margin) - obj.thickness,
                                         obj.height * spacer_height, self._generate_new_id('table_spacer'))

        self.modeler.move_object(spacer, obj.depth * (1 - margin), obj.width * margin + obj.thickness,
                                 obj.height * (1 - spacer_height))

        self.modeler.move_object(right_stand, obj.depth * margin, obj.width * margin, 0)
        self.modeler.move_object(left_stand, obj.depth * margin, obj.width * (1 - margin), 0)

        all_parts = [
            top, left_stand, right_stand, spacer
        ]

        material = self._get_modeler_material(obj.material)

        for part in all_parts:
            self.modeler.assign_material_to_object(material, part)

        self.modeler.move_many_objects(all_parts, obj.location[0], obj.location[1], obj.location[2])
