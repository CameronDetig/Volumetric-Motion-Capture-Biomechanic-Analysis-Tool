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
import time
import numpy as np
from numpy.ma.core import fmod

# Blender imports
import bpy
from bpy.types import Operator
from mathutils import Matrix
from mathutils.bvhtree import BVHTree

# Addon imports
from ..functions import *

class OBJECT_OT_icp_align_track(Operator):
    """Uses ICP alignment to iteratively align two objects over a sequence of frames."""
    bl_idname = "object.align_icp_track"
    bl_label = "Track Individual"
    bl_options = {'REGISTER', 'UNDO'}

    ################################################
    # Blender Operator methods

    @classmethod
    def poll(cls, context):
        """Used to determine whether to show the button as active or inactive."""
        condition_1 = False
        condition_2 = False

        if (bpy.context.scene.baseObj != ""):
            condition_1 = True
        if (bpy.context.scene.alignObj != ""):
            condition_2 = True

        return condition_1 and condition_2

    def execute(self, context):

        #Play the animation
        #bpy.ops.screen.animation_play()

        #currentFrame = bpy.data.scenes['Scene'].frame_current

        positions = []

        # Use the object name from the text input to get the object
        base_obj = bpy.context.scene.objects.get(bpy.context.scene.baseObj)
        align_obj = bpy.context.scene.objects.get(bpy.context.scene.alignObj)
        print (align_obj)
        print (base_obj)

        # To store the mesh sequence cache modifier on the base object
        # seqCacheModifier = None
        # isAlembic = False
        # cacheFile = None
        # for m in base_obj.modifiers:
        #     print(m)
        #     if (m.type == "MESH_SEQUENCE_CACHE"):
        #         isAlembic = True
        #         print ("Is Alembic")
        #         seqCacheModifier = m
        #         print (seqCacheModifier)
        #         cacheFile = bpy.data.cache_files["sport_coach_man_-_warmup_60_00fps_FILTERED_2880.abc"]
        #         cacheFile.override_frame = True


        curScene = bpy.context.scene
        print (curScene)

        curLayer = bpy.context.view_layer
        print (curLayer)

        settings = get_addon_preferences()
        start = time.time()
        base_bvh = BVHTree.FromObject(base_obj, context.evaluated_depsgraph_get())
        align_obj.rotation_mode = 'QUATERNION'
        align_meth = settings.align_meth
        thresh = settings.min_start
        sample = settings.sample_fraction
        iters = settings.icp_iterations
        target_d = settings.target_d
        use_target = settings.use_target
        factor = round(1 / sample)


        vlist = []
        #figure out if we need to do any inclusion/exclusion
        group_lookup = {g.name: g.index for g in align_obj.vertex_groups}
        if 'icp_include' in align_obj.vertex_groups:
            group = group_lookup['icp_include']

            for v in align_obj.data.vertices:
                for g in v.groups:
                    if g.group == group and g.weight > 0.9:
                        vlist.append(v.index)

        elif 'icp_exclude' in align_obj.vertex_groups:
            group = group_lookup['icp_exclude']
            for v in align_obj.data.vertices:
                v_groups = [g.group for g in v.groups]
                if group not in v_groups:
                    vlist.append(v.index)
                else:
                    for g in v.groups:
                        if g.group == group and g.weight < 0.1:
                            vlist.append(v.index)

        #unfortunate way to do this..
        else:
            vlist = [v.index for v in align_obj.data.vertices]


        # We only have to do this once:
        #dg = bpy.context.evaluated_depsgraph_get()  # getting the dependency graph

        # # Advance through the specified frames
        # for curFrame in range(settings.start_frame, settings.end_frame + 1):
        #
        #     #bpy.data.scenes[curScene].frame_set(curFrame)
        #     #curScene.frame_set(curFrame)
        #     curScene.frame_current = curFrame
        #     #bpy.ops.anim.change_frame(frame=curFrame)
        #
        #     f = curScene.frame_current
        #     print (f)
        #
        #     #Update the view so the base object is in the correct position
        #     #curLayer.update()
        #     bpy.context.view_layer.update()
        #
        #     #f = curScene.frame_get()
        #     #print(f)
        #
        #     # every time the object updates:
        #     #base_obj_modified = base_obj.evaluated_get(dg)  # this gives us the evaluated version of the object. Aka with all modifiers and deformations applied.
        #
        #     # if (isAlembic):
        #     #     cacheFile.frame = curFrame
        #
        #     n = 0
        #     converged = False
        #     conv_t_list = [target_d * 2] * 5  # store last 5 translations
        #     conv_r_list = [None] * 5
        #
        #     #Main ICP Program Loop
        #     while n < iters  and not converged:
        #         iter_start = time.time()
        #
        #         (A, B, d_stats) = make_pairs(align_obj, base_obj, base_bvh, vlist, thresh, factor, calc_stats = use_target)
        #
        #         pair_time = time.time()
        #         #print('Made pairs in %f seconds' % (iter_start - pair_time))
        #
        #         if align_meth == '0': #rigid transform
        #             M = affine_matrix_from_points(A, B, shear=False, scale=False, usesvd=True)
        #         elif align_meth == '1': # rot, loc, scale
        #             M = affine_matrix_from_points(A, B, shear=False, scale=True, usesvd=True)
        #
        #         affine_time = time.time()
        #         #print('Affine matrix tooth %f seconds' % (affine_time - pair_time))
        #
        #
        #         #TODO inefficient way to transpose a matrix?
        #         new_mat = Matrix.Identity(4)
        #         for y in range(0,4):
        #             for z in range(0,4):
        #                 new_mat[y][z] = M[y][z]
        #
        #         align_obj.matrix_world = align_obj.matrix_world @ new_mat
        #         trans = new_mat.to_translation()
        #         quat = new_mat.to_quaternion()
        #
        #         align_obj.update_tag()
        #         curLayer.update()
        #         #context.view_layer.update()
        #         #curScene.update()
        #
        #         if d_stats:
        #             i = int(fmod(n,5))
        #             conv_t_list[i] = trans.length
        #             conv_r_list[i] = abs(quat.angle)
        #
        #             #If the objects are converged
        #             if all(d < target_d for d in conv_t_list):
        #                 converged = True
        #                 print('Converged in %s iterations' % str(n+1))
        #                 #Record and keyframe the position of the aligned object on every frame
        #                 positions.append(align_obj.location)
        #                 align_obj.keyframe_insert(data_path="location", frame=curFrame)
        #                 align_obj.keyframe_insert(data_path="rotation_quaternion", frame=curFrame)
        #
        #         n += 1
        #
        #     time_taken = time.time() - start
        #     #If the objects did not converge over the specified number of iterations
        #     if use_target and not converged:
        #         print('Maxed out iterations')
        #
        #     print('Final Translation: %f ' % conv_t_list[i])
        #     print('Final Avg Dist: %f' % d_stats[0])
        #     print('Final St Dev %f' % d_stats[1])
        #     print('Avg last 5 rotation angle: %f' % np.mean(conv_r_list))
        #
        #     #print('Aligned obj in %f sec' % time_taken)
        #
        # #for pos in positions:
        # #    print(pos)
        # #cacheFile.override_frame = False
        # print()
        # return {'FINISHED'}

        n = 0
        converged = False
        conv_t_list = [target_d * 2] * 5  # store last 5 translations
        conv_r_list = [None] * 5

        # Main ICP Program Loop
        while n < iters and not converged:
            iter_start = time.time()

            (A, B, d_stats) = make_pairs(align_obj, base_obj, base_bvh, vlist, thresh, factor,
                                         calc_stats=use_target)

            pair_time = time.time()
            # print('Made pairs in %f seconds' % (iter_start - pair_time))

            if align_meth == '0':  # rigid transform
                M = affine_matrix_from_points(A, B, shear=False, scale=False, usesvd=True)
            elif align_meth == '1':  # rot, loc, scale
                M = affine_matrix_from_points(A, B, shear=False, scale=True, usesvd=True)

            affine_time = time.time()
            # print('Affine matrix tooth %f seconds' % (affine_time - pair_time))

            # TODO inefficient way to transpose a matrix?
            new_mat = Matrix.Identity(4)
            for y in range(0, 4):
                for z in range(0, 4):
                    new_mat[y][z] = M[y][z]

            align_obj.matrix_world = align_obj.matrix_world @ new_mat
            trans = new_mat.to_translation()
            quat = new_mat.to_quaternion()

            align_obj.update_tag()
            curLayer.update()
            # context.view_layer.update()
            # curScene.update()

            if d_stats:
                i = int(fmod(n, 5))
                conv_t_list[i] = trans.length
                conv_r_list[i] = abs(quat.angle)

                # If the objects are converged
                if all(d < target_d for d in conv_t_list):
                    converged = True
                    print('Converged in %s iterations' % str(n + 1))
                    # Record and keyframe the position of the aligned object on every frame
                    positions.append(align_obj.location)
                    align_obj.keyframe_insert(data_path="location", frame=curScene.frame_current)
                    align_obj.keyframe_insert(data_path="rotation_quaternion", frame=curScene.frame_current)

            n+=1
        time_taken = time.time() - start
        # If the objects did not converge over the specified number of iterations
        if use_target and not converged:
            print('Maxed out iterations')

        print('Final Translation: %f ' % conv_t_list[i])
        print('Final Avg Dist: %f' % d_stats[0])
        print('Final St Dev %f' % d_stats[1])
        print('Avg last 5 rotation angle: %f' % np.mean(conv_r_list))

        # print('Aligned obj in %f sec' % time_taken)

        # for pos in positions:
        #    print(pos)
        # cacheFile.override_frame = False
        curScene.frame_current = curScene.frame_current + 1
        print()
        return {'FINISHED'}

    ################################################
