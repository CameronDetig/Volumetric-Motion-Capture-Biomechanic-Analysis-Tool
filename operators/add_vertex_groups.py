# Copyright (C) 2019 Christopher Gearhart
# chris@bblanimation.com
# http://bblanimation.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# System imports
import random

# Blender imports
import bpy
from bpy.types import Operator

# Addon imports
from ..functions import *

class OBJECT_OT_add_vertex_groups(Operator):
    """Adds vertex groups to the base object for all the necessary body regions."""
    bl_idname = "object.add_vertex_groups"
    bl_label = "Add Vertex Groups"
    bl_options = {"REGISTER", "UNDO"}

    # regionName: bpy.props.StringProperty(
    #     name='regionName',
    #     default='group'
    # )


    @classmethod
    def poll(cls, context):
        condition1 = context.mode in {'OBJECT', 'PAINT_WEIGHT'}
        condition2 = context.active_object

        if condition1 and condition2:
            condition3 = context.active_object.type == 'MESH'
        else:
            condition3 = False
        return condition1 and condition2 and condition3

    def execute(self, context):
        print ("add vertex groups")


        return {'FINISHED'}
