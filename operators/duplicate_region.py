# Script by Cameron Detig 07/2021

# System imports
import random

# Blender imports
import bpy
from bpy.types import Operator

# Addon imports
from ..functions import *

class OBJECT_OT_duplicate_region(Operator):
    """Adds a vertex group and puts in weight paint mode"""
    bl_idname = "object.duplicate_region"
    bl_label = "Paint region of body to be tracked"
    bl_options = {"REGISTER", "UNDO"}

    regionName: bpy.props.StringProperty(
        name='regionName',
        default='group'
    )


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
        print ("duplicate " + self.regionName)

        # Duplicate the object, remove modifier, and go into edit mode
        bpy.ops.object.duplicate()
        newObj = bpy.context.active_object

        n = 0
        for obj in bpy.data.collections["Body Regions"].objects:
            if self.regionName in obj.name:
                n += 1
        newObj.name = self.regionName + "." + str(n+1)

        #newObj.name = self.regionName
        #bpy.ops.object.modifier_remove(modifier="MeshSequenceCache")
        bpy.ops.object.modifier_apply(modifier="MeshSequenceCache")
        bpy.ops.object.mode_set(mode="EDIT")

        # Select the correct vertex group, and delete everything except it
        bpy.ops.object.vertex_group_set_active(group=self.regionName)
        bpy.ops.object.vertex_group_select()
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.delete(type='FACE')

        # Go back to edit mode, center the object's origin, clear rotation, and give it a random color
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.context.object.color = (random.random(), random.random(), random.random(), 1)
        bpy.ops.object.vertex_group_remove(all=True)

        colName = "Body Regions"
        if not bpy.data.collections.get(colName):  # Get collection by name in data, and check if None
            mCol = bpy.data.collections.new(colName)  # Create a new one if not found
            bpy.context.scene.collection.children.link(mCol)  # Add it to your Scene
        else:
            mCol = bpy.data.collections.get(colName)  # If already exists, get the collection

        # Add the object to the body regions collection. Remove it from the default collection.
        mCol.objects.link(bpy.context.object)
        bpy.context.collection.objects.unlink(bpy.context.object)




        # Create an empty and place it with the mesh
        bpy.ops.object.empty_add(type='SPHERE', radius=0.05, align='WORLD', location=(0,0,0), scale=(1, 1, 1))
        bpy.context.object.name = self.regionName + "_marker"
        bpy.context.object.show_in_front = True
        curMarker = bpy.context.active_object

        colName = "Markers"
        if not bpy.data.collections.get(colName):  # Get collection by name in data, and check if None
            mCol = bpy.data.collections.new(colName)  # Create a new one if not found
            bpy.context.scene.collection.children.link(mCol) # Add it to your Scene
        else:
            mCol = bpy.data.collections.get(colName) # If already exists, get the collection

        # Add the empty to the markers collection. Remove it from the default collection.
        mCol.objects.link(bpy.context.object)
        bpy.context.collection.objects.unlink(bpy.context.object)
        bpy.context.active_object.parent = newObj




        # Add a new bone to the armature
        armatureExists = False # Check if the armature object already exists
        for o in bpy.context.scene.objects:
            if o.name == "Marker Armature":
                armatureExists = True
                print(o.name)

        if armatureExists == False:   # If it does not exist, add one.
            print ("Does not exist")
            bpy.ops.object.armature_add(radius=0.15, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                        rotation=(0, 1.5708, 0), scale=(1, 1, 1))
            arm = bpy.context.active_object
            arm.name = "Marker Armature"

            bpy.ops.object.mode_set(mode="POSE")
            curBone = arm.data.bones[0]
            curBone.select = True

            curBone.name = self.regionName + "_bone.1"
            bpy.ops.pose.constraint_add(type='COPY_LOCATION')
            bpy.context.object.pose.bones[self.regionName + "_bone.1"].constraints["Copy Location"].target = curMarker
        else:
            print ("Exists")
            bpy.ops.object.hide_view_clear()
            bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("Marker Armature")
            arm = bpy.context.active_object

            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.armature.duplicate()
            curBone = arm.data.bones[-1]
            curBone.select = True
            #curBone = bpy.ops.armature.duplicate()

            curBone.name = self.regionName + "_bone.1"
            bpy.ops.object.mode_set(mode="POSE")
            bpy.context.object.pose.bones[self.regionName + "_bone.1"].constraints[0].target = curMarker


        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("Marker Armature")
        bpy.ops.object.hide_view_set(unselected=False)


        return {'FINISHED'}
