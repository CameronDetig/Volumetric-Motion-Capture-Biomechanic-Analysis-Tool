# Script by Cameron Detig 07/2021

# System imports
import random

# Blender imports
import bpy
from bpy.types import Operator

# Addon imports
from ..functions import *
#import .add_track_objects
from .add_track_objects import *


class OBJECT_OT_enable_booleans(Operator):
    """Enables boolean operators for all the necessary body regions. Lets you see what the selected regions look like."""
    bl_idname = "object.enable_booleans"
    bl_label = "Toggle Booleans"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.mode in 'OBJECT' and len(bpy.data.collections.get("Body Regions").objects) != 0:
            return True
        else:
            return False

    def execute(self, context):
        print ("toggle booleans")
        for obj in bpy.data.collections.get("Body Regions").objects:
            if obj.parent == None: # If it is a top level object in the collection
                print (obj)
                bpy.context.view_layer.objects.active = obj
                if bpy.context.object.modifiers["Boolean"].show_viewport == False:
                    bpy.context.object.modifiers["Boolean"].show_viewport = True
                else:
                    bpy.context.object.modifiers["Boolean"].show_viewport = False

        return {'FINISHED'}



class OBJECT_OT_apply_booleans(Operator):
    """Applies the boolean operators for all the necessary body regions. Needs to be run before tracking the sequence."""
    bl_idname = "object.apply_booleans"
    bl_label = "Apply Booleans"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if context.mode in 'OBJECT' and len(bpy.data.collections.get("Body Regions").objects) != 0:
            return True
        else:
            return False

    def execute(self, context):
        print ("Apply booleans")

        for obj in bpy.data.collections.get("Body Regions").objects:
            if obj.parent == None: # If it is a top level object in the collection
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier="Boolean")

        return {'FINISHED'}



# class OBJECT_OT_toggle_boundaries(Operator):
#     """Adds vertex groups to the base object for all the necessary body regions."""
#     bl_idname = "object.toggle_boundaries"
#     bl_label = "Toggle Boundaries"
#     bl_options = {"REGISTER", "UNDO"}
#
#     @classmethod
#     def poll(cls, context):
#         if context.mode in 'OBJECT' and len(bpy.data.collections.get("Body Regions").objects) != 0:
#             return True
#         else:
#             return False
#
#     def execute(self, context):
#         print ("toggle boundaries")
#         for obj in bpy.data.collections.get("Body Regions").objects:
#             if obj.parent != None and obj.type == "MESH": # If it is not a top level object in the collection.
#                 print (obj)
#                 bpy.context.view_layer.objects.active = obj
#                 obj.select_set(state=True)
#
#                 if obj.hide_viewport == False:
#                     #bpy.ops.object.hide_view_set(unselected=False)
#                     obj.hide_viewport = True
#                     #self.enabled = False
#                 else:
#                     #bpy.ops.object.show_view_set(unselected=False)
#                     obj.hide_viewport = False
#                     #self.enabled = True
#
#         return {'FINISHED'}
