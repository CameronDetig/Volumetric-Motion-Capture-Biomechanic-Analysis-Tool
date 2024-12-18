# Script by Cameron Detig 07/2021

# System imports
import random

# Blender imports
import bpy
from bpy.types import Operator

# Addon imports
from ..functions import *


class OBJECT_OT_add_track_objects(Operator):
    """Adds track objects for all the necessary body regions."""
    bl_idname = "object.add_track_objects"
    bl_label = "Add track objects"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        condition = context.mode in {'OBJECT'}
        return condition


    def setupBoundaryObject(self, regionName, bevelAmount):
        ''' Sets up boundary objects. Rename, clears scale, moves collection. Returns the object. '''
        bpy.context.active_object.name = regionName + "_Boundary"
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].width = bevelAmount
        bpy.ops.object.modifier_apply(modifier="Bevel")
        bpy.context.object.color = (random.random(), random.random(), random.random(), 1) # Give it a random color
        bpy.context.object.display_type = 'WIRE'
        # Add to the body regions collection. Remove it from the default collection.
        bpy.data.collections.get("Body Regions").objects.link(bpy.context.object)
        bpy.context.collection.objects.unlink(bpy.context.object)
        return bpy.context.active_object


    def setupTrackObject(self, regionName, pos, rot, childObj):
        ''' Sets up the track object. duplicates boundary object, renames, adds boolean modifier. '''
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = regionName
        bpy.context.object.show_name = True
        bpy.context.active_object.location = pos
        bpy.context.object.rotation_euler = rot
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].object = bpy.context.scene.objects.get(bpy.context.scene.baseObj)
        bpy.context.object.modifiers["Boolean"].show_viewport = False
        bpy.context.object.display_type = 'TEXTURED'
        bpy.context.object.color = childObj.color # Give it the same color as the boundary object.
        childObj.parent = bpy.context.active_object
        childObj.hide_select = True
        return bpy.context.active_object


    def createMarker(self, pos, markerName, parentObj):
        '''Create an empty and place it with the mesh'''
        bpy.ops.object.empty_add(type='SPHERE', radius=0.025, align='WORLD', location=pos, scale=(1, 1, 1))
        bpy.context.object.name = markerName
        bpy.context.object.show_in_front = True

        # Add the empty to the markers collection. Remove it from the default collection.
        bpy.data.collections.get("Markers").objects.link(bpy.context.object)
        if (bpy.context.collection != bpy.data.collections.get("Markers")): # If it is not already in the collection
            bpy.context.collection.objects.unlink(bpy.context.object)
        bpy.context.active_object.parent = parentObj
        return bpy.context.active_object



    # def createBone(self, boneName, curMarker):
    #     '''Add a new bone to the armature'''
    #     bpy.ops.object.hide_view_clear()
    #     bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("Marker Armature")
    #     arm = bpy.context.active_object
    #     bpy.ops.object.mode_set(mode="EDIT")
    #
    #     if (arm.data.bones[0].name == "defaultBone"):
    #         curBone = arm.data.bones[0]
    #     else:
    #         bpy.ops.armature.duplicate()
    #         curBone = arm.data.bones[-1]
    #
    #     curBone.select = True
    #     curBone.name = boneName
    #     bpy.ops.object.mode_set(mode="POSE")
    #     bpy.context.object.pose.bones[boneName].constraints[0].target = curMarker
    #     bpy.ops.object.mode_set(mode="OBJECT")
    #     #bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("Marker Armature")


    def execute(self, context):
        print ("Add track objects")

        # Check if the body regions collection already exists
        if not bpy.data.collections.get("Body Regions"):
            mCol = bpy.data.collections.new("Body Regions")  # Create a new one if not found
            bpy.context.scene.collection.children.link(mCol)  # Add it to the Scene

        # Check if the markers collection already exists
        if not bpy.data.collections.get("Markers"):
            mCol = bpy.data.collections.new("Markers")  # Create a new one if not found
            bpy.context.scene.collection.children.link(mCol)  # Add it to the Scene

        # Check if the armature object already exists
        # armatureExists = False
        # for o in bpy.context.scene.objects:
        #     if o.name == "Marker Armature":
        #         armatureExists = True
        #
        # if armatureExists == False:  # If it does not exist, add one.
        #     bpy.ops.object.armature_add(radius=0.15, enter_editmode=False, align='WORLD', location=(0, 0, 0),
        #                                 rotation=(1.5708, 0, 0), scale=(1, 1, 1))
        #     arm = bpy.context.active_object
        #     arm.name = "Marker Armature"
        #
        #     bpy.ops.object.mode_set(mode="POSE")
        #     curBone = arm.data.bones[0]
        #     curBone.name = "defaultBone"
        #     curBone.select = True
        #     bpy.ops.pose.constraint_add(type='COPY_LOCATION')



        regionName = "Left_Foot" #-------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.175, 0.36, 0.12))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.02)
        parentObj = self.setupTrackObject(regionName, (0.2, -0.08, 0.04), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0,-0.13,0), "L.Toe.Tip", parentObj)
        #self.createBone("L.Toe.Tip",curMarker)
        curMarker = self.createMarker((0, 0.16, 0), "L.Heel", parentObj)
        #self.createBone("L.Heel", curMarker)
        curMarker = self.createMarker((0, 0.1, 0.05), "L.Ankle.Center", parentObj)
        #self.createBone("L.Ankle.Center", curMarker)


        regionName = "Right_Foot" #------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(0.175, 0.36, 0.12))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.02)
        parentObj = self.setupTrackObject(regionName, (-0.2, -0.08, 0.04), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, -0.13, 0), "R.Toe.Tip", parentObj)
        #self.createBone("R.Toe.Tip", curMarker)
        curMarker = self.createMarker((0, 0.16, 0), "R.Heel", parentObj)
        #self.createBone("R.Heel", curMarker)
        curMarker = self.createMarker((0, 0.1, 0.05), "R.Ankle.Center", parentObj)
        #self.createBone("R.Ankle.Center", curMarker)


        regionName = "Left_Calf" #-------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.2, .2, .3))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0.2, 0, 0.3), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "L.Calf.Top", parentObj)
        #self.createBone("L.Calf.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.1), "L.Calf.Bottom", parentObj)
        #self.createBone("L.Calf.Bottom", curMarker)


        regionName = "Right_Calf" #------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.2, .2, .3))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (-0.2, 0, 0.3), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "R.Calf.Top", parentObj)
        #self.createBone("R.Calf.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.1), "R.Calf.Bottom", parentObj)
        #self.createBone("R.Calf.Bottom", curMarker)


        regionName = "Left_Thigh" #------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.22, .22, .3))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0.2, 0, 0.62), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "L.Thigh.Top", parentObj)
        #self.createBone("L.Thigh.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "L.Thigh.Bottom", parentObj)
        #self.createBone("L.Thigh.Bottom", curMarker)


        regionName = "Right_Thigh" #-----------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.22, .22, .3))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (-0.2, 0, 0.62), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "R.Thigh.Top", parentObj)
        #self.createBone("R.Thigh.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "R.Thigh.Bottom", parentObj)
        #self.createBone("R.Thigh.Bottom", curMarker)


        regionName = "Pelvis"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.3, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.9, .65, 1))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0, 0, 0.89), (0,0,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, -0.045, 0.017), "Pelvis.Center", parentObj)
        #self.createBone("Pelvis", curMarker)
        curMarker = self.createMarker((0.12, 0, -0.05), "L.Hip.Center", parentObj)
        #self.createBone("L.Hip.Center", curMarker)
        curMarker = self.createMarker((-0.12, 0, -0.05), "R.Hip.Center", parentObj)
        #self.createBone("R.Hip.Center", curMarker)


        regionName = "Collar"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.8, .6, 1))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0, 0, 1.5), (0,0,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0.1, 0, 0), "L.Collar", parentObj)
        #self.createBone("L.Collar", curMarker)
        curMarker = self.createMarker((-0.1, 0, 0), "R.Collar", parentObj)
        #self.createBone("R.Collar", curMarker)



        regionName = "Head"  # ----------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                              scale=(.13, .17, .17))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=0.01)
        parentObj = self.setupTrackObject(regionName, (0, 0, 1.7), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "Head.Top", parentObj)
        #self.createBone("Head.Top", curMarker)
        curMarker = self.createMarker((0, 0.1, -0.08), "Head.Bottom", parentObj)
        #self.createBone("Kneck", curMarker)


        regionName = "Left_Shoulder"  # -------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                              scale=(.09, .09, .09))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=0.01)
        parentObj = self.setupTrackObject(regionName, (0.2, 0, 1.45), (0,0,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0), "L.Shoulder.Center", parentObj)
        #self.createBone("L.Shoulder.Center", curMarker)


        regionName = "Right_Shoulder"  # -------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                              scale=(.09, .09, .09))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=0.01)
        parentObj = self.setupTrackObject(regionName, (-0.2, 0, 1.45), (0,0,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0), "R.Shoulder.Center", parentObj)
        #self.createBone("R.Shoulder.Center", curMarker)


        regionName = "Left_Bicep"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.13, .13, .26))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0.36, 0, 1.3), (0,-45,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.08), "L.Bicep.Top", parentObj)
        #self.createBone("L.Bicep.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "L.Bicep.Bottom", parentObj)
        #self.createBone("L.Bicep.Bottom", curMarker)


        regionName = "Right_Bicep"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.13, .13, .26))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (-0.36, 0, 1.3), (0,45,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.08), "R.Bicep.Top", parentObj)
        #self.createBone("R.Bicep.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "R.Bicep.Bottom", parentObj)
        #self.createBone("R.Bicep.Bottom", curMarker)


        regionName = "Left_Forearm"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.12, .12, .26))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (0.6, 0, 1.14), (0,-45,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.08), "L.Forearm.Top", parentObj)
        #self.createBone("L.Forearm.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "L.Forearm.Bottom", parentObj)
        #self.createBone("L.Forearm.Bottom", curMarker)


        regionName = "Right_Forearm"  # ------------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, enter_editmode=False,
                                            align='WORLD', location=(0, 0, 0), scale=(.12, .12, .26))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.015)
        parentObj = self.setupTrackObject(regionName, (-0.6, 0, 1.14), (0,45,0), childObj)  # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.08), "R.Forearm.Top", parentObj)
        #self.createBone("R.Forearm.Top", curMarker)
        curMarker = self.createMarker((0, 0, -0.08), "R.Forearm.Bottom", parentObj)
        #self.createBone("R.Forearm.Bottom", curMarker)


        regionName = "Left_Hand"  # -----------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                        scale=(0.1, 0.12, 0.18))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.01)
        parentObj = self.setupTrackObject(regionName, (0.8, 0, 1), (0,-45,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "L.Wrist.Center", parentObj)
        #self.createBone("L.Wrist.Center", curMarker)
        curMarker = self.createMarker((0, 0, 0), "L.Knuckle", parentObj)
        #self.createBone("L.Knuckle", curMarker)


        regionName = "Right_Hand"  # ----------------------------------------------------------------------------------
        # Create Boundary Object (Child)
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                        scale=(0.1, 0.12, 0.18))
        childObj = self.setupBoundaryObject(regionName, bevelAmount=.01)
        parentObj = self.setupTrackObject(regionName, (-0.8, 0, 1), (0,45,0), childObj) # Create Track Object (Parent)

        curMarker = self.createMarker((0, 0, 0.1), "R.Wrist.Center", parentObj)
        #self.createBone("R.Wrist.Center", curMarker)
        curMarker = self.createMarker((0, 0, 0), "R.Knuckle", parentObj)
        #self.createBone("R.Knuckle", curMarker)


        # # Hide the armature object to make the viewport simpler.
        # bpy.ops.object.select_all(action='DESELECT')
        # obj = bpy.context.scene.objects.get("Marker Armature")
        # bpy.context.view_layer.objects.active = obj
        # obj.select_set(state=True)
        # bpy.ops.object.hide_view_set(unselected=False)

        return {'FINISHED'}
