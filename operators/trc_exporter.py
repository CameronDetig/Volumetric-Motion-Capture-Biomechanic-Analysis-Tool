# Script by: Cameron Detig 07/2021
# Some code from Jonathan Merritt

import bpy
import csv
# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

# class TRCData:
#     markers = {}         # map of marker names to sequence of mathutils.Vector
#     data_rate = bpy.context.scene.render.fps      # data rate (Hz)
#     camera_rate = bpy.context.scene.render.fps    # camera rate (Hz)
#     num_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start   # number of frames
#     num_markers = len(bpy.data.collections.get("Markers").objects)      # number of markers
#     units = "mm"         # measurement units
#     orig_data_rate = bpy.context.scene.render.fps  # original data rate (Hz)
#     orig_data_start = bpy.context.scene.frame_start  # original data start frame
#     orig_num_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start  # original number of frames

def write_some_data(context, filepath, yUp):
    print("Exporting TRC File")
    file = open(filepath, 'w', encoding='utf-8', newline='')
    writer = csv.writer(file, 'excel-tab')


    data_rate = bpy.context.scene.render.fps  # data rate (Hz)
    camera_rate = bpy.context.scene.render.fps  # camera rate (Hz)
    num_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start  # number of frames
    num_markers = len(bpy.data.collections.get("Markers").objects)  # number of markers
    units = "mm"  # measurement units
    orig_data_rate = bpy.context.scene.render.fps  # original data rate (Hz)
    orig_data_start = bpy.context.scene.frame_start  # original data start frame
    orig_num_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start  # original number of frames

    markers = []  # map of marker objects
    markerNames = []
    for m in bpy.data.collections.get("Markers").objects:
        markers.append(m)

    for m in markers:
        markerNames.append(m.name)


    writer.writerow(['PathFileType', '4', '(X,Y,Z)', "MoCap Data"])
    writer.writerow(['DataRate', 'CameraRate', 'NumFrames', 'NumMarkers', 'Units', 'OrigDataRate', 'OrigDataStartFrame', 'OrigNumFrames'])
    writer.writerow([data_rate, camera_rate, num_frames, num_markers, units, orig_data_rate, orig_data_start, orig_num_frames])

    row4 = ["Frame#", "Time"]
    for i in range(1, (len(markerNames) * 3) + 2):  # XYZ for each marker + "Frame#" and "Time"
        print(i % 3)
        if (i % 3 == 0):  # If is a third column, add marker name
            if (i//3 == 0):
                row4.append(markerNames[0])
            else:
                row4.append(markerNames[(i // 3) - 1])
        else:
            if (i > 2): #If past the "Frame#" and "Time" cells
                row4.append('')
    writer.writerow(row4)


    row5 = ["", ""]
    for i in range(0, len(markerNames)):
        row5.append("X" + str(i+1))
        row5.append("Y" + str(i+1))
        row5.append("Z" + str(i+1))
    writer.writerow(row5)

    writer.writerow("")

    data = []
    curTime = 0
    frameTime = 1 / data_rate
    for i in range(orig_data_start, orig_num_frames+1):
        curRow = [i, round(curTime, 3)]
        bpy.context.scene.frame_set(i)
        for m in markers:
            if yUp == True:
                curRow.append(round(m.matrix_world.translation[1] * -1000,5)) # * 1000 to convert m to mm
                curRow.append(round(m.matrix_world.translation[2] * 1000,5))
                curRow.append(round(m.matrix_world.translation[0] * -1000,5)) # Swaps the axis around
            else:
                curRow.append(round(m.matrix_world.translation[0] * 1000, 5))  # * 1000 to convert m to mm
                curRow.append(round(m.matrix_world.translation[1] * 1000, 5))
                curRow.append(round(m.matrix_world.translation[2] * 1000, 5))  # Keep Y and Z the same

        data.append(curRow)
        curTime += frameTime

    writer.writerows(data)

    file.close()

    return {'FINISHED'}





class ExportTRC(Operator, ExportHelper):
    """Exports the empties from the markers collection to the .trc file format for use in OpenSim."""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export to .trc"

    # ExportHelper mixin class uses this
    filename_ext = ".trc"

    filter_glob: StringProperty(
        default="*.trc",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    yUp: BoolProperty(
        name="Make Y the Up Axis",
        description="Swap the Z axis with the Y axis for use in other programs where Y being up is the standard.",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.yUp)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportTRC.bl_idname, text="TRC Export Operator")


# def register():
#     bpy.utils.register_class(ExportTRC)
#     bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
#
#
# def unregister():
#     bpy.utils.unregister_class(ExportTRC)
#     bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
#
#
# if __name__ == "__main__":
#     register()
#
#     # test call
#     bpy.ops.export_test.some_data('INVOKE_DEFAULT')