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
# NONE!

# Blender imports
import bpy
from bpy.types import Panel

# Addon imports
from .functions import *

### Sets up the side menu UI ###

class VIEW3D_PT_UI_MENU(Panel):
    """UI for Motion Capture Addon"""
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI" if b280() else "TOOLS"
    bl_label       = "Motion Capture"
    bl_context     = "objectmode"
    bl_category    = "Motion Capture"

    def draw(self, context):
        preferences = get_addon_preferences()
        layout = self.layout

        # if bpy.data.texts.find("Object Alignment log") >= 0:
        #     split = layout.split(align=True, percentage=0.9)
        #     col = split.column(align=True)
        #     row = col.row(align=True)
        #     row.operator("scene.report_error", text="Report Error", icon="URL")
        #     col = split.column(align=True)
        #     row = col.row(align=True)
        #     row.operator("scene.close_report_error", text="", icon="PANEL_CLOSE")

        # align_obj = context.object
        # row = layout.row()
        # if align_obj:
        #     row.label(text="Align Object: " + align_obj.name)
        # else:
        #     row.label(text="Align Object: Empty")
        #
        # if len(context.selected_objects) == 2:
        #     base_obj = [obj for obj in context.selected_objects if obj != align_obj][0]
        #     row = layout.row()
        #     row.label(text="Base Object: " + base_obj.name)
        # else:
        #     row = layout.row()
        #     row.label(text="Base Object: Empty")
        #
        # row = layout.row()
        # row.label(text="Pre Processing:")
        # row = layout.row()
        # row.operator("object.align_include")
        # row.operator("object.align_include_clear", icon="X", text="")
        #
        # row = layout.row()
        # row.operator("object.align_exclude")
        # row.operator("object.align_exclude_clear", icon="X", text="")

        # row = layout.row()
        # row.label(text="Initial Alignment:")
        # row = layout.row()
        # row.operator("object.align_picked_points")
        # row.operator("screen.area_dupli", icon="FULLSCREEN_ENTER", text="")

        row = layout.row()
        row.prop(preferences, "align_meth")

        #row = layout.row()
        #row.prop(preferences, "redraw_frequency")

        row = layout.row()
        row.prop(preferences, "icp_iterations")

        row = layout.row()
        row.prop(preferences, "use_sample")
        row.prop(preferences, "sample_fraction")

        row = layout.row()
        row.prop(preferences, "min_start")

        row = layout.row()
        row.prop(preferences, "use_target")
        row.prop(preferences, "target_d")

        layout.separator()
        row = layout.row()
        row.label(text="Alignment Track")

        row = layout.row(align=True)
        row.operator("object.add_track_objects", text="Add Track Objects")
        row.operator("object.enable_booleans", text="View Selections")
        row = layout.row(align=True)
        row.operator("object.apply_booleans")

        # Code modified from the blender timeline panel for the sequence control buttons
        if not context.screen.is_animation_playing:
            # If not playing, show the play-reversed button
            row.operator("object.align_icp_track_all_reverse", text="", icon='PLAY_REVERSE')
            row.operator("object.align_icp_track_all_forward", text="", icon='PLAY')
        else:
            # If playing, show the pause button
            row.scale_x = 2
            row.operator("object.align_icp_track_all_pause", text="", icon='PAUSE')
            row.scale_x = 1


        layout.separator()
        row = layout.row(align=True)
        row.operator("object.align_icp", text="Individual Align")
        #row.operator("object.align_icp_redraw")

        row.operator("object.align_icp_track", text="Individual Track")

        # Code modified from the blender timeline panel for the sequence control buttons
        if not context.screen.is_animation_playing:
            # If not playing, show the play-reversed button
            row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.alignObj
            row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.alignObj
        else:
            # If playing, show the pause button
            row.scale_x = 2
            row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
            row.scale_x = 1

        #row = layout.row()
        #row.prop(preferences, "start_frame")
        #row.prop(preferences, "end_frame")

        row = layout.row()
        row.prop(context.scene, "baseObj", text="base object")
        base_obj = bpy.context.scene.objects.get(bpy.context.scene.baseObj)
        row = layout.row()
        row.prop(context.scene, "alignObj", text="align object")
        #layout.separator()

        row = layout.row(align=True)
        row.operator("export_test.some_data")


        # Old vertex paint system
        # ##### Head Track Properties --------------------------------------------------------------------------------
        # row = layout.row(align=True)
        # row.label(text="Head")
        # bodyPart = "head"
        # row.operator("object.paint_region", text="paint").regionName = bodyPart
        # if bodyPart in base_obj.vertex_groups:
        #     row.operator("object.duplicate_region", text="generate").regionName = bodyPart
        #
        # row = layout.row(align=True)
        # row.prop(context.scene, "headObjText", text="")
        # # Display track forward and backwards buttons
        # if not context.screen.is_animation_playing: # If not playing, show the play-reversed button
        #     row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.headObjText
        #     row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.headObjText
        # else:  # If playing, show the pause button
        #     row.scale_x = 2
        #     row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
        #     row.scale_x = 1
        #
        #
        # ##### Right Hand Track Properties ----------------------------------------------------------------------------
        # row = layout.row(align=True)
        # row.label(text="Right Hand")
        # bodyPart = "right hand"
        # row.operator("object.paint_region", text="paint").regionName = bodyPart
        # if bodyPart in base_obj.vertex_groups:
        #     row.operator("object.duplicate_region", text="generate").regionName = bodyPart
        #
        # row = layout.row(align=True)
        # row.prop(context.scene, "rightHandObjText", text="")
        # # Display track forward and backwards buttons
        # if not context.screen.is_animation_playing:  # If not playing, show the play-reversed button
        #     row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.rightHandObjText
        #     row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.rightHandObjText
        # else:  # If playing, show the pause button
        #     row.scale_x = 2
        #     row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
        #     row.scale_x = 1
        #
        #
        # ##### Left Hand Track Properties ----------------------------------------------------------------------------
        # row = layout.row(align=True)
        # row.label(text="Left Hand")
        # bodyPart = "left hand"
        # row.operator("object.paint_region", text="paint").regionName = bodyPart
        # if bodyPart in base_obj.vertex_groups:
        #     row.operator("object.duplicate_region", text="generate").regionName = bodyPart
        #
        # row = layout.row(align=True)
        # row.prop(context.scene, "leftHandObjText", text="")
        # # Display track forward and backwards buttons
        # if not context.screen.is_animation_playing:  # If not playing, show the play-reversed button
        #     row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.leftHandObjText
        #     row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.leftHandObjText
        # else:  # If playing, show the pause button
        #     row.scale_x = 2
        #     row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
        #     row.scale_x = 1
        #
        #
        # ##### Right Foot Track Properties ----------------------------------------------------------------------------
        # row = layout.row(align=True)
        # row.label(text="Right Foot")
        # bodyPart = "right foot"
        # row.operator("object.paint_region", text="paint").regionName = bodyPart
        # if bodyPart in base_obj.vertex_groups:
        #     row.operator("object.duplicate_region", text="generate").regionName = bodyPart
        #
        # row = layout.row(align=True)
        # row.prop(context.scene, "rightFootObjText", text="")
        # # Display track forward and backwards buttons
        # if not context.screen.is_animation_playing:  # If not playing, show the play-reversed button
        #     row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.rightFootObjText
        #     row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.rightFootObjText
        # else:  # If playing, show the pause button
        #     row.scale_x = 2
        #     row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
        #     row.scale_x = 1
        #
        #
        # ##### Left Foot Track Properties ----------------------------------------------------------------------------
        # row = layout.row(align=True)
        # row.label(text="Left Foot")
        # bodyPart = "left foot"
        # row.operator("object.paint_region", text="paint").regionName = bodyPart
        # if bodyPart in base_obj.vertex_groups:
        #     row.operator("object.duplicate_region", text="generate").regionName = bodyPart
        #
        # row = layout.row(align=True)
        # row.prop(context.scene, "leftFootObjText", text="")
        # # Display track forward and backwards buttons
        # if not context.screen.is_animation_playing:  # If not playing, show the play-reversed button
        #     row.operator("object.align_icp_track_reverse", text="", icon='PLAY_REVERSE').alignObj = bpy.context.scene.leftFootObjText
        #     row.operator("object.align_icp_track_forward", text="", icon='PLAY').alignObj = bpy.context.scene.leftFootObjText
        # else:  # If playing, show the pause button
        #     row.scale_x = 2
        #     row.operator("object.align_icp_track_pause", text="", icon='PAUSE')
        #     row.scale_x = 1





