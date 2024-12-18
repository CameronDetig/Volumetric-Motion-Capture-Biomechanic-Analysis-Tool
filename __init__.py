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

bl_info = {
    "name": "Motion Capture",
    "author": "Cameron Detig - expanded upon work from Patrick Moore & Christopher Gearhart",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Motion Capture",
    "description": "Used to locate and track joint movements in volumetric motion capture data",
    "warning": "",
    "wiki_url": "",
    "category": "Transform Mesh"
}

# System imports
# NONE!

# Blender imports
import bpy
from bpy.types import Scene, Object

# Addon imports
from .operators import *
from .ui import *
from .lib.preferences import *  #to be able to register the preferences
from .functions.common import *

classes = [
    Preferences,
    VIEW3D_PT_UI_MENU,
    OBJECT_OT_align_include_add,
    OBJECT_OT_align_include_clear,
    OBJECT_OT_align_exclude_add,
    OBJECT_OT_align_exclude_clear,
    OBJECT_OT_align_pick_points,
    OBJECT_OT_icp_align,
    OBJECT_OT_icp_align_feedback,
    OBJECT_OT_icp_align_track,
    OBJECT_OT_icp_align_track_forward,
    OBJECT_OT_icp_align_track_pause,
    OBJECT_OT_icp_align_track_reverse,
    OBJECT_OT_icp_align_track_all_forward,
    OBJECT_OT_icp_align_track_all_pause,
    OBJECT_OT_icp_align_track_all_reverse,
    OBJECT_OT_paint_region,
    OBJECT_OT_duplicate_region,
    OBJECT_OT_enable_booleans,
    OBJECT_OT_apply_booleans,
    OBJECT_OT_add_track_objects,
    ExportTRC
]

def register():
    # register classes
    for cls in classes:
        make_annotations(cls)
        bpy.utils.register_class(cls)

    bpy.types.Scene.baseObj = bpy.props.StringProperty(
        default="",
        description="name of base object")
    bpy.types.Scene.alignObj = bpy.props.StringProperty(
        default="",
        description="name of align object")

    bpy.types.Scene.headObjText = bpy.props.StringProperty(
        default="head",
        description="name of head object")

    bpy.types.Scene.rightHandObjText = bpy.props.StringProperty(
        default="right hand",
        description="name of right hand object")
    bpy.types.Scene.leftHandObjText = bpy.props.StringProperty(
        default="left hand",
        description="name of left hand object")

    bpy.types.Scene.rightFootObjText = bpy.props.StringProperty(
        default="right foot",
        description="name of right foot object")
    bpy.types.Scene.leftFootObjText = bpy.props.StringProperty(
        default="left foot",
        description="name of left foot object")


    bpy.types.Scene.curAlignObj = bpy.props.StringProperty(
        description="scene level variable to hold the current alignment object"
    )

    #bpy.types.Scene.string_property = bpy.props.PointerProperty(
    #    description="object for selection")
    #bpy.types.Scene.prop = bpy.props.PointerProperty(type=bpy.types.Object)
    #string_property = PointerProperty(type=bpy.types.Object)


def unregister():
    # unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
