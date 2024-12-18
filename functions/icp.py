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
#from ..functions import *
from .common import *
from .general import *
from .utilities import *

def runICPAlgrithm(baseObjName = "base", alignObjName = "align"):
    print ("Running ICP")
    # Use the object name from the text input to get the object
    base_obj = bpy.context.scene.objects.get(bpy.context.scene.baseObj)
    #align_obj = bpy.context.scene.objects.get(bpy.context.scene.alignObj)
    align_obj = bpy.context.scene.objects.get(bpy.context.scene.curAlignObj)
    #base_obj = bpy.context.scene.objects.get(baseObjName)
    #align_obj = bpy.context.scene.objects.get(alignObjName)
    print (base_obj)
    print (align_obj)

    curScene = bpy.context.scene
    #print (curScene)

    curLayer = bpy.context.view_layer
    #print (curLayer)

    settings = get_addon_preferences()
    start = time.time()
    base_bvh = BVHTree.FromObject(base_obj, bpy.context.evaluated_depsgraph_get())
    align_obj.rotation_mode = 'QUATERNION'
    align_meth = settings.align_meth
    thresh = settings.min_start
    sample = settings.sample_fraction
    iters = settings.icp_iterations
    target_d = settings.target_d
    use_target = settings.use_target
    factor = round(1 / sample)

    vlist = []
    # figure out if we need to do any inclusion/exclusion
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

    # unfortunate way to do this..
    else:
        vlist = [v.index for v in align_obj.data.vertices]


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
                # Keyframe the position of the aligned object on every frame
                align_obj.keyframe_insert(data_path="location", frame=curScene.frame_current)
                align_obj.keyframe_insert(data_path="rotation_quaternion", frame=curScene.frame_current)

        n += 1
    time_taken = time.time() - start
    # If the objects did not converge over the specified number of iterations
    if use_target and not converged:
        print('Maxed out iterations')

    print('Final Translation: %f ' % conv_t_list[i])
    print('Final Avg Dist: %f' % d_stats[0])
    print('Final St Dev %f' % d_stats[1])
    print('Avg last 5 rotation angle: %f' % np.mean(conv_r_list))

    # print('Aligned obj in %f sec' % time_taken)

    print()