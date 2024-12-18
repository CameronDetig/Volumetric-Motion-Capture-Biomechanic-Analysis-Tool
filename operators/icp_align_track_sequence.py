
# System imports
import time
import numpy as np
from numpy.ma.core import fmod

# Blender imports
import bpy
from bpy.types import Operator
from mathutils import Matrix
from mathutils.bvhtree import BVHTree

# Addon imports
from ..functions.icp import runICPAlgrithm
from ..functions import *

def checkObjects():
    """Used to determine whether to show the button as active or inactive."""
    condition_1 = False
    condition_2 = False
    if (bpy.context.scene.baseObj != ""):
        condition_1 = True
    if (bpy.context.scene.alignObj != ""):
        condition_2 = True

    return condition_1 and condition_2

def runICPIndividual(dummy1, dummy2):
    curFrame = bpy.context.scene.frame_current
    if curFrame == bpy.context.scene.frame_start or curFrame == bpy.context.scene.frame_end:
        bpy.app.handlers.frame_change_post.remove(runICPIndividual()) # Stop the ICP Algorithm
        bpy.ops.screen.animation_play()  # Pause the animation

    runICPAlgrithm()



class OBJECT_OT_icp_align_track_forward(Operator):
    """Play animation and run ICP on every frame."""
    bl_idname = "object.align_icp_track_forward"
    bl_label = "ICP Align Track Forward"
    bl_options = {'REGISTER', 'UNDO'}

    alignObj: bpy.props.StringProperty(name='alignObj')

    @classmethod
    def poll(cls, context):
        #return checkObjects()
        return True

    def execute(self, context):
        bpy.context.scene.curAlignObj = self.alignObj
        #bpy.app.handlers.frame_change_post.append(runICPAlgrithm(bpy.context.scene.baseObj, self.alignObj))
        bpy.app.handlers.frame_change_post.append(runICPIndividual)
        #Play the animation
        bpy.ops.screen.animation_play()
        return {'FINISHED'}



class OBJECT_OT_icp_align_track_pause(Operator):
    """Pause the animation and the ICP operations."""
    bl_idname = "object.align_icp_track_pause"
    bl_label = "ICP Align Track Pause"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        #return checkObjects()
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.remove(runICPIndividual)
        #Pause the animation
        bpy.ops.screen.animation_play()
        return {'FINISHED'}



class OBJECT_OT_icp_align_track_reverse(Operator):
    """Reverse the animation and run ICP on every frame."""
    bl_idname = "object.align_icp_track_reverse"
    bl_label = "ICP Align Track Reverse"
    bl_options = {'REGISTER', 'UNDO'}

    alignObj: bpy.props.StringProperty(name='alignObj')

    @classmethod
    def poll(cls, context):
        #return checkObjects()
        return True

    def execute(self, context):
        bpy.context.scene.curAlignObj = self.alignObj
        bpy.app.handlers.frame_change_post.append(runICPIndividual)
        #Reverse the animation
        bpy.ops.screen.animation_play(reverse=True)
        return {'FINISHED'}






def runICPAll(dummy1, dummy2):
    curFrame = bpy.context.scene.frame_current
    if curFrame == bpy.context.scene.frame_start or curFrame == bpy.context.scene.frame_end:
        bpy.app.handlers.frame_change_post.remove(runICPAll) # Stop the ICP Algorithm
        bpy.ops.screen.animation_play()  # Pause the animation

    for obj in bpy.data.collections.get("Body Regions").objects:
        if obj.parent == None:  # If it is a top level object in the collection
            bpy.context.scene.curAlignObj = obj.name  # Used by the ICP script
            runICPAlgrithm()


class OBJECT_OT_icp_align_track_all_forward(Operator):
    """ Play animation and run ICP on every frame. """
    bl_idname = "object.align_icp_track_all_forward"
    bl_label = "ICP Align Track All Forward"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.append(runICPAll)
        bpy.ops.screen.animation_play() #Play the animation
        return {'FINISHED'}


class OBJECT_OT_icp_align_track_all_pause(Operator):
    """ Pause the animation and the ICP operations. """
    bl_idname = "object.align_icp_track_all_pause"
    bl_label = "ICP Align Track All Pause"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.remove(runICPAll)
        bpy.ops.screen.animation_play() #Pause the animation
        return {'FINISHED'}


class OBJECT_OT_icp_align_track_all_reverse(Operator):
    """ Play animation in reverse and run ICP on every frame. """
    bl_idname = "object.align_icp_track_all_reverse"
    bl_label = "ICP Align Track All Reverse"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.append(runICPAll)
        bpy.ops.screen.animation_play(reverse=True) #Play the animation
        return {'FINISHED'}