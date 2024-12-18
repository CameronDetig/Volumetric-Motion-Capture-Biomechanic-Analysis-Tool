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

# Blender imports
import bpy
from bpy.types import AddonPreferences
from bpy.props import *


class Preferences(AddonPreferences):
    """Handles the preferences UI that appears in the Addon's page in blender preferences."""
    bl_idname = __package__[:__package__.index(".lib")]


    #Alignment Method drop down
    align_methods = ['RIGID', 'ROT_LOC_SCALE']  # ,'AFFINE']
    align_items = []
    for index, item in enumerate(align_methods):
        align_items.append((str(index), align_methods[index], str(index)))
    align_meth = EnumProperty(items=align_items, name="Alignment Method",
                              description="Changes how picked points registration aligns object", default='0',
                              options={'ANIMATABLE'}, update=None, get=None, set=None)

    redraw_frequency = IntProperty(
        name="Redraw Iterations",
        description="Number of iterations between redraw, bigger = less redraw but faster completion",
        default=10)
    icp_iterations = IntProperty(
            name="ICP Iterations",
            default=50)
    use_sample = BoolProperty(
            name="Use Sample",
            description="Use a sample of vertices to align",
            default=False)
    sample_fraction = FloatProperty(
            name="Sample Fraction",
            description="Only fraction of mesh vertices will be used for alignment. Less accurate, but faster",
            default=0.5,
            min=0,
            max=1)
    min_start = FloatProperty(
            name="Minimum Starting Dist",
            description="Only vertices closer than this distance will be used in each iteration",
            default=0.5,
            min=0,
            max=20)
    target_d = FloatProperty(
            name="Target Translation",
            description="If translation of 3 iterations is less than target, ICP is considered successful",
            default=0.01,
            min=0,
            max=10)
    use_target = BoolProperty(
            name="Use Target Translation",
            description="Calculate alignment stats on every iteration to assess convergence. Slower per step, but may result in less steps",
            default=True)

    # leftHandObjText = StringProperty(
    #     default="",
    #     description="name of left hand object")

    # start_frame = IntProperty(
    #     name="start frame",
    #     default=1)
    #
    # end_frame = IntProperty(
    #     name="end frame",
    #     default=30)



    def draw(self, context):
        layout = self.layout

        # draw addon preferences
        layout.label(text="MoCap Preferences")
        layout.prop(self, "align_meth")
        layout.prop(self, "redraw_frequency")
        layout.prop(self, "icp_iterations")
        layout.prop(self, "use_sample")
        layout.prop(self, "sample_fraction")
        layout.prop(self, "min_start")
        layout.prop(self, "use_target")
        layout.prop(self, "target_d")
        layout.prop(self, "start_frame")
        layout.prop(self, "end_frame")
