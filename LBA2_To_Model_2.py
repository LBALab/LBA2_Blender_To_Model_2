# +----------------------------------------------------------------------------------------------------------+
# | LBA2 Model Exporter - Blender Python (v2.79)                                                             |
# |    By Quilt from the LBA Discord server.                                                                 |
# |                                                                                                          |
# | Before using this script, please read the following text.                                                |
# | It works as expected, but it can definitely be improved.                                                 |
# | Make sure you edit the path for your liking.                                                             |
# |                                                                                                          |
# | The model must be named, "Mesh".                                                                         |
# | Its location must be at the origin - X, Y, and Z all being zero.                                         |
# | Also, it should be rotated facing the Y-axis.                                                            |
# | Furthermore, it must contain only triangles - no quadrilaterals.                                         |
# | Ensure that it does not exceed 530 triangles.                                                            |
# |                                                                                                          |
# | The armature must be named, "Armature".                                                                  |
# | It must be selected first in pose mode.                                                                  |
# |                                                                                                          |
# | The script should then run as expected.                                                                  |
# |                                                                                                          |
# | Note:                                                                                                    |
# | -----                                                                                                    |
# |    If you want a model that only translates, use one bone at origin.                                     |
# |    If you want a model that translates and rotates, use two bones at origin.                             |
# |    In other words the first bone musn't be weighted to any vertices.                                     |
# |    The same must be the same for the second bone.                                                        |
# |                                                                                                          |
# |    Further explanation for this unfortunately requires an understanding of the LBA2 model format itself. |
# |                                                                                                          |
# | Important Note:                                                                                          |
# | ---------------                                                                                          |
# |    If the armature's weight groups must be edited later on - just reweight the entire model instead.     |
# |    Additionally, delete the armature modifier and re-assign it.                                          |
# |    It's just better if you do. It causes less problems and headaches.                                    |
# |    The only big downside is that the bones must be weighted in the order they were created.              |
# |                                                                                                          |
# |    If you look at the Mesh's block data of an object, make sure the vertex group order starts from 0.    |
# |    For example: Bone, Bone.001, Bone.002... Bone.029.                                                    |
# |    Otherwise, the export process will not work as expected.                                              |
# |                                                                                                          |
# |    This script CAN take many seconds to export the model to the LBA2 format.                             |
# |    If all goes well, there SHOULD be duplicate meshes for each triangle in the model.                    |
# |    These are used to color the model using an operator I wrote to color and save the data to the model.  |
# |                                                                                                          |
# |    All problems with this script should hopefully be resolved in the future.                             |
# |    However, this is still a big improvement in regards to my last exporter.                              |
# +----------------------------------------------------------------------------------------------------------+



# +------------+
# | Libraries. |
# +------------+

import os, bpy, sys, struct
from math import sqrt

# Clear debug messages.
os.system("cls")



# +---------+
# | Macros. |
# +---------+

SCALE           = 100
HEADER          = 0x60
BONES           = 0x20
BONES_OFFSET    = 0x24
VERTICES        = 0x28
VERTICES_OFFSET = 0x2C
NORMALS         = 0x30
NORMALS_OFFSET  = 0x34
UNKNOWNS        = 0x38
UNKNOWNS_OFFSET = 0x3C
POLYGONS        = 0x40
POLYGONS_OFFSET = 0x44
LINES           = 0x48
LINES_OFFSET    = 0x4C
SPHERES         = 0x50
SPHERES_OFFSET  = 0x54
TEXTURES        = 0x58
TEXTURES_OFFSET = 0x5C



# +-----------------------+
# | Variables And Arrays. |
# +-----------------------+

# Path.
model_path = "C:\\Users\\SomePerson\\custom_model.lm2"

# Bone indices.
bones = []
bones_parents = []
bones_parents_indices = []

bone_0_parents_checked = False
bone_1_parents_checked = False
bone_2_parents_checked = False
bone_3_parents_checked = False
bone_4_parents_checked = False
bone_5_parents_checked = False
bone_6_parents_checked = False
bone_7_parents_checked = False
bone_8_parents_checked = False
bone_9_parents_checked = False
bone_10_parents_checked = False
bone_11_parents_checked = False
bone_12_parents_checked = False
bone_13_parents_checked = False
bone_14_parents_checked = False
bone_15_parents_checked = False
bone_16_parents_checked = False
bone_17_parents_checked = False
bone_18_parents_checked = False
bone_19_parents_checked = False
bone_20_parents_checked = False
bone_21_parents_checked = False
bone_22_parents_checked = False
bone_23_parents_checked = False
bone_24_parents_checked = False
bone_25_parents_checked = False
bone_26_parents_checked = False
bone_27_parents_checked = False
bone_28_parents_checked = False
bone_29_parents_checked = False

# Bone vertices.
bone_0_verts = []
bone_1_verts = []
bone_2_verts = []
bone_3_verts = []
bone_4_verts = []
bone_5_verts = []
bone_6_verts = []
bone_7_verts = []
bone_8_verts = []
bone_9_verts = []
bone_10_verts = []
bone_11_verts = []
bone_12_verts = []
bone_13_verts = []
bone_14_verts = []
bone_15_verts = []
bone_16_verts = []
bone_17_verts = []
bone_18_verts = []
bone_19_verts = []
bone_20_verts = []
bone_21_verts = []
bone_22_verts = []
bone_23_verts = []
bone_24_verts = []
bone_25_verts = []
bone_26_verts = []
bone_27_verts = []
bone_28_verts = []
bone_29_verts = []

bone_all_verts = []

# Bone vertex indices.
bones_vertices = []
bones_root_indices = []
bones_root_vertices = []

# Bone vertex positions.
bones_vertices_x = []
bones_vertices_y = []
bones_vertices_z = []

bones_vertices_x_root = []
bones_vertices_y_root = []
bones_vertices_z_root = []

# Bone normal positions.
bones_normals_x = []
bones_normals_y = []
bones_normals_z = []

# Vertex indices.
vertices = []

# Normal indices.
normals = []

# Triangle vertex indices.
triangles = []
triangles_1 = []
triangles_2 = []
triangles_3 = []

# Triangle vertex positions.
triangles_x = []
triangles_y = []
triangles_z = []

triangles_colors = []

# Other variables.
global_scale = 100
normal_scale = 150

extra_verts = 0
bones_num = [0]
triangle_index = 0
triangle_index_1 = 0



# +------------+
# | Functions. |
# +------------+

def set_bone_data(bone):
    bones_num[0] += 1
    bones.append(bone)
    bones_parents.append(bone.parent)

def distance(first, second):
    x = second[0] - first[0]
    y = second[1] - first[1]
    z = second[2] - first[2]
    
    distance = sqrt((x)**2 + (y)**2 + (z)**2)
    return distance

# Anyway to get this working would most likely decrease redundancy, increase readability, and increase speed.
# Part of the reason this code is so bulky as is is because I cannot get this part to work properly.
'''def check_bone_data(bones_checked, bone_index, bone_verts):
    # Get children bone's vertices.
    if (bones_checked == False):
        # Check if this bone has children.
        if (len(bones[bone_index].children) >= 1):
            # Check for 30 possible child bones.
            for q in range(0, 30):
                # Check if this child is a part of this bone.
                if (len(bones[bone_index].children) == q):
                    # Loop through each child in this bone.
                    for w in range(0, len(bones[bone_index].children)):
                        bone_verts.append(0)
                        bones_vertices.append(bone_index)
                                        
                        bpy.ops.mesh.primitive_cube_add()
                        bpy.context.scene.objects.active.location = (bones[bone_index].children[w].head[0], \
                                                                     bones[bone_index].children[w].head[1], \
                                                                     bones[bone_index].children[w].head[2])
                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                        bpy.context.scene.objects.active.name = ("branch  " + str(bone_index) + ":" + str(w))
                                        
                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                        bones_vertices_x_root.append(bones[bone_index].head[0])
                        bones_vertices_y_root.append(bones[bone_index].head[1])
                        bones_vertices_z_root.append(bones[bone_index].head[2])
                                        
                        bones_normals_x.append(0)
                        bones_normals_y.append(0)
                        bones_normals_z.append(0)
        else:
            bones_checked = True
        bones_checked = True
                    
    # Get all other vertices in this vertex group.
    bone_verts.append(0)
    bones_vertices.append(bone_index)
    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                    
    bones_vertices_x_root.append(bones[bone_index].head[0])
    bones_vertices_y_root.append(bones[bone_index].head[1])
    bones_vertices_z_root.append(bones[bone_index].head[2])
                    
    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])'''



# +-----------------+
# | Get Bone Datas. |
# +-----------------+

# Check to make sure bones in armature exist.
bone_0  = bpy.data.objects["Armature"].pose.bones.get("Bone")
bone_1  = bpy.data.objects["Armature"].pose.bones.get("Bone.001")
bone_2  = bpy.data.objects["Armature"].pose.bones.get("Bone.002")
bone_3  = bpy.data.objects["Armature"].pose.bones.get("Bone.003")
bone_4  = bpy.data.objects["Armature"].pose.bones.get("Bone.004")
bone_5  = bpy.data.objects["Armature"].pose.bones.get("Bone.005")
bone_6  = bpy.data.objects["Armature"].pose.bones.get("Bone.006")
bone_7  = bpy.data.objects["Armature"].pose.bones.get("Bone.007")
bone_8  = bpy.data.objects["Armature"].pose.bones.get("Bone.008")
bone_9  = bpy.data.objects["Armature"].pose.bones.get("Bone.009")
bone_10 = bpy.data.objects["Armature"].pose.bones.get("Bone.010")
bone_11 = bpy.data.objects["Armature"].pose.bones.get("Bone.011")
bone_12 = bpy.data.objects["Armature"].pose.bones.get("Bone.012")
bone_13 = bpy.data.objects["Armature"].pose.bones.get("Bone.013")
bone_14 = bpy.data.objects["Armature"].pose.bones.get("Bone.014")
bone_15 = bpy.data.objects["Armature"].pose.bones.get("Bone.015")
bone_16 = bpy.data.objects["Armature"].pose.bones.get("Bone.016")
bone_17 = bpy.data.objects["Armature"].pose.bones.get("Bone.017")
bone_18 = bpy.data.objects["Armature"].pose.bones.get("Bone.018")
bone_19 = bpy.data.objects["Armature"].pose.bones.get("Bone.019")
bone_20 = bpy.data.objects["Armature"].pose.bones.get("Bone.020")
bone_21 = bpy.data.objects["Armature"].pose.bones.get("Bone.021")
bone_22 = bpy.data.objects["Armature"].pose.bones.get("Bone.022")
bone_23 = bpy.data.objects["Armature"].pose.bones.get("Bone.023")
bone_24 = bpy.data.objects["Armature"].pose.bones.get("Bone.024")
bone_25 = bpy.data.objects["Armature"].pose.bones.get("Bone.025")
bone_26 = bpy.data.objects["Armature"].pose.bones.get("Bone.026")
bone_27 = bpy.data.objects["Armature"].pose.bones.get("Bone.027")
bone_28 = bpy.data.objects["Armature"].pose.bones.get("Bone.028")
bone_29 = bpy.data.objects["Armature"].pose.bones.get("Bone.029")

# Set to edit mode.
bpy.ops.object.mode_set(mode='EDIT')

# Edit bones must always be edited in edit mode.
# These get all bones, whether they have disconnected roots or not.
if (bone_0 is not None):
    bone_0_edit = bpy.context.object.data.edit_bones["Bone"]
if (bone_1 is not None):
    bone_1_edit = bpy.context.object.data.edit_bones["Bone.001"]
if (bone_2 is not None):
    bone_2_edit = bpy.context.object.data.edit_bones["Bone.002"]
if (bone_3 is not None):
    bone_3_edit = bpy.context.object.data.edit_bones["Bone.003"]
if (bone_4 is not None):
    bone_4_edit = bpy.context.object.data.edit_bones["Bone.004"]
if (bone_5 is not None):
    bone_5_edit = bpy.context.object.data.edit_bones["Bone.005"]
if (bone_6 is not None):
    bone_6_edit = bpy.context.object.data.edit_bones["Bone.006"]
if (bone_7 is not None):
    bone_7_edit = bpy.context.object.data.edit_bones["Bone.007"]
if (bone_8 is not None):
    bone_8_edit = bpy.context.object.data.edit_bones["Bone.008"]
if (bone_9 is not None):
    bone_9_edit = bpy.context.object.data.edit_bones["Bone.009"]
if (bone_10 is not None):
    bone_10_edit = bpy.context.object.data.edit_bones["Bone.010"]
if (bone_11 is not None):
    bone_11_edit = bpy.context.object.data.edit_bones["Bone.011"]
if (bone_12 is not None):
    bone_12_edit = bpy.context.object.data.edit_bones["Bone.012"]
if (bone_13 is not None):
    bone_13_edit = bpy.context.object.data.edit_bones["Bone.013"]
if (bone_14 is not None):
    bone_14_edit = bpy.context.object.data.edit_bones["Bone.014"]
if (bone_15 is not None):
    bone_15_edit = bpy.context.object.data.edit_bones["Bone.015"]
if (bone_16 is not None):
    bone_16_edit = bpy.context.object.data.edit_bones["Bone.016"]
if (bone_17 is not None):
    bone_17_edit = bpy.context.object.data.edit_bones["Bone.017"]
if (bone_18 is not None):
    bone_18_edit = bpy.context.object.data.edit_bones["Bone.018"]
if (bone_19 is not None):
    bone_19_edit = bpy.context.object.data.edit_bones["Bone.019"]
if (bone_20 is not None):
    bone_20_edit = bpy.context.object.data.edit_bones["Bone.020"]
if (bone_21 is not None):
    bone_21_edit = bpy.context.object.data.edit_bones["Bone.021"]
if (bone_22 is not None):
    bone_22_edit = bpy.context.object.data.edit_bones["Bone.022"]
if (bone_23 is not None):
    bone_23_edit = bpy.context.object.data.edit_bones["Bone.023"]
if (bone_24 is not None):
    bone_24_edit = bpy.context.object.data.edit_bones["Bone.024"]
if (bone_25 is not None):
    bone_25_edit = bpy.context.object.data.edit_bones["Bone.025"]
if (bone_26 is not None):
    bone_26_edit = bpy.context.object.data.edit_bones["Bone.026"]
if (bone_27 is not None):
    bone_27_edit = bpy.context.object.data.edit_bones["Bone.027"]
if (bone_28 is not None):
    bone_28_edit = bpy.context.object.data.edit_bones["Bone.028"]
if (bone_29 is not None):
    bone_29_edit = bpy.context.object.data.edit_bones["Bone.029"]

if (bone_0  is not None):
    set_bone_data(bone_0)
if (bone_1  is not None):
    set_bone_data(bone_1)
if (bone_2  is not None):
    set_bone_data(bone_2)
if (bone_3  is not None):
    set_bone_data(bone_3)
if (bone_4  is not None):
    set_bone_data(bone_4)
if (bone_5  is not None):
    set_bone_data(bone_5)
if (bone_6  is not None):
    set_bone_data(bone_6)
if (bone_7  is not None):
    set_bone_data(bone_7)
if (bone_8  is not None):
    set_bone_data(bone_8)
if (bone_9  is not None):
    set_bone_data(bone_9)
if (bone_10 is not None):
    set_bone_data(bone_10)
if (bone_11 is not None):
    set_bone_data(bone_11)
if (bone_12 is not None):
    set_bone_data(bone_12)
if (bone_13 is not None):
    set_bone_data(bone_13)
if (bone_14 is not None):
    set_bone_data(bone_14)
if (bone_15 is not None):
    set_bone_data(bone_15)
if (bone_16 is not None):
    set_bone_data(bone_16)
if (bone_17 is not None):
    set_bone_data(bone_17)
if (bone_18 is not None):
    set_bone_data(bone_18)
if (bone_19 is not None):
    set_bone_data(bone_19)
if (bone_20 is not None):
    set_bone_data(bone_20)
if (bone_21 is not None):
    set_bone_data(bone_21)
if (bone_22 is not None):
    set_bone_data(bone_22)
if (bone_23 is not None):
    set_bone_data(bone_23)
if (bone_24 is not None):
    set_bone_data(bone_24)
if (bone_25 is not None):
    set_bone_data(bone_25)
if (bone_26 is not None):
    set_bone_data(bone_26)
if (bone_27 is not None):
    set_bone_data(bone_27)
if (bone_28 is not None):
    set_bone_data(bone_28)
if (bone_29 is not None):
    set_bone_data(bone_29)

# Append the head of the first bone's position.
bone_0_verts.append(0)
bones_vertices.append(0)
bones_vertices_x.append(bones[0].head[0])
bones_vertices_y.append(bones[0].head[1])
bones_vertices_z.append(bones[0].head[2])

bones_vertices_x_root.append(bones[0].head[0])
bones_vertices_y_root.append(bones[0].head[1])
bones_vertices_z_root.append(bones[0].head[2])

bones_normals_x.append(0)
bones_normals_y.append(0)
bones_normals_z.append(0)

# Append the tail of the first bone's position.
bone_0_verts.append(0)
bones_vertices.append(0)
bones_vertices_x.append(bones[0].tail[0])
bones_vertices_y.append(bones[0].tail[1])
bones_vertices_z.append(bones[0].tail[2])

bones_vertices_x_root.append(bones[0].tail[0])
bones_vertices_y_root.append(bones[0].tail[1])
bones_vertices_z_root.append(bones[0].tail[2])

bones_normals_x.append(0)
bones_normals_y.append(0)
bones_normals_z.append(0)

# Append the tail of the second bone's position.
bone_1_verts.append(0)
bones_vertices.append(1)
bones_vertices_x.append(bones[1].tail[0])
bones_vertices_y.append(bones[1].tail[1])
bones_vertices_z.append(bones[1].tail[2])

bones_vertices_x_root.append(bones[1].tail[0])
bones_vertices_y_root.append(bones[1].tail[1])
bones_vertices_z_root.append(bones[1].tail[2])

bones_normals_x.append(0)
bones_normals_y.append(0)
bones_normals_z.append(0)

# Loop through existing vertex groups.
for i in range(0, bones_num[0]):
    
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.scene.objects.active.location = (bones[i].head[0], bones[i].head[1], bones[i].head[2])
    
    bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
    bones_root_vertices.append(bpy.context.scene.objects.active)
    if (i < 10):
        bpy.context.scene.objects.active.name = ("b00" + str(i))
    if (i >= 10 and i < 100):
        bpy.context.scene.objects.active.name = ("b0" + str(i))
    
    # Set to object mode.
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Loop through existing vertices.
    for j in (bpy.data.objects["Mesh"].data.vertices):
        # Loop through existing vertex indices in vertex groups.
        for k in (j.groups):
            vg = bpy.data.objects["Mesh"].vertex_groups[i].index
            
            # Check if the vertex is in this bone.
            if (k.group == vg):
                
                #if (vg != 0):
                #    print("none")
                #if (vg != 1):
                #    print("none")
                
                if (vg == 2):
                    # Get children bone's vertices.
                    if (bone_2_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[2].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[2].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[2].children)):
                                        bone_2_verts.append(0)
                                        bones_vertices.append(2)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[2].children[w].head[0], \
                                                                                     bones[2].children[w].head[1], \
                                                                                     bones[2].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 2: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[2].head[0])
                                        bones_vertices_y_root.append(bones[2].head[1])
                                        bones_vertices_z_root.append(bones[2].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                                
                        bone_2_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_2_verts.append(0)
                    bones_vertices.append(2)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                    
                    bones_vertices_x_root.append(bones[2].head[0])
                    bones_vertices_y_root.append(bones[2].head[1])
                    bones_vertices_z_root.append(bones[2].head[2])
                    
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 3):
                    # Get children bone's vertices.
                    if (bone_3_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[3].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[3].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[3].children)):
                                        bone_3_verts.append(0)
                                        bones_vertices.append(3)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[3].children[w].head[0], \
                                                                                     bones[3].children[w].head[1], \
                                                                                     bones[3].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 3: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[3].head[0])
                                        bones_vertices_y_root.append(bones[3].head[1])
                                        bones_vertices_z_root.append(bones[3].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_3_parents_checked = True
                        bone_3_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_3_verts.append(0)
                    bones_vertices.append(3)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                    
                    bones_vertices_x_root.append(bones[3].head[0])
                    bones_vertices_y_root.append(bones[3].head[1])
                    bones_vertices_z_root.append(bones[3].head[2])
                    
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                
                if (vg == 4):
                    # Get children bone's vertices.
                    if (bone_4_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[4].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[4].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[4].children)):
                                        bone_4_verts.append(0)
                                        bones_vertices.append(4)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[4].children[w].head[0], \
                                                                                     bones[4].children[w].head[1], \
                                                                                     bones[4].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 4: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[4].head[0])
                                        bones_vertices_y_root.append(bones[4].head[1])
                                        bones_vertices_z_root.append(bones[4].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_4_parents_checked = True
                        bone_4_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_4_verts.append(0)
                    bones_vertices.append(4)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[4].head[0])
                    bones_vertices_y_root.append(bones[4].head[1])
                    bones_vertices_z_root.append(bones[4].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 5):
                    #check_bone_data(bone_5_parents_checked, 5, bone_5_verts)
                    # Get children bone's vertices.
                    if (bone_5_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[5].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[5].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[5].children)):
                                        bone_5_verts.append(0)
                                        bones_vertices.append(5)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[5].children[w].head[0], \
                                                                                     bones[5].children[w].head[1], \
                                                                                     bones[5].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 5: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[5].head[0])
                                        bones_vertices_y_root.append(bones[5].head[1])
                                        bones_vertices_z_root.append(bones[5].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_5_parents_checked = True
                        bone_5_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_5_verts.append(0)
                    bones_vertices.append(5)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[5].head[0])
                    bones_vertices_y_root.append(bones[5].head[1])
                    bones_vertices_z_root.append(bones[5].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                
                if (vg == 6):
                    # Get children bone's vertices.
                    if (bone_6_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[6].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[6].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[6].children)):
                                        bone_6_verts.append(0)
                                        bones_vertices.append(6)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[6].children[w].head[0], \
                                                                                     bones[6].children[w].head[1], \
                                                                                     bones[6].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 6: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[6].head[0])
                                        bones_vertices_y_root.append(bones[6].head[1])
                                        bones_vertices_z_root.append(bones[6].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_6_parents_checked = True
                        bone_6_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_6_verts.append(0)
                    bones_vertices.append(6)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[6].head[0])
                    bones_vertices_y_root.append(bones[6].head[1])
                    bones_vertices_z_root.append(bones[6].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 7):
                    # Get children bone's vertices.
                    if (bone_7_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[7].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[7].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[7].children)):
                                        bone_7_verts.append(0)
                                        bones_vertices.append(7)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[7].children[w].head[0], \
                                                                                     bones[7].children[w].head[1], \
                                                                                     bones[7].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 7: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[7].head[0])
                                        bones_vertices_y_root.append(bones[7].head[1])
                                        bones_vertices_z_root.append(bones[7].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_7_parents_checked = True
                        bone_7_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_7_verts.append(0)
                    bones_vertices.append(7)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[7].head[0])
                    bones_vertices_y_root.append(bones[7].head[1])
                    bones_vertices_z_root.append(bones[7].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 8):
                    # Get children bone's vertices.
                    if (bone_8_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[8].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[8].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[8].children)):
                                        bone_8_verts.append(0)
                                        bones_vertices.append(8)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[8].children[w].head[0], \
                                                                                     bones[8].children[w].head[1], \
                                                                                     bones[8].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 8: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[8].head[0])
                                        bones_vertices_y_root.append(bones[8].head[1])
                                        bones_vertices_z_root.append(bones[8].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_8_parents_checked = True
                        bone_8_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_8_verts.append(0)
                    bones_vertices.append(8)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[8].head[0])
                    bones_vertices_y_root.append(bones[8].head[1])
                    bones_vertices_z_root.append(bones[8].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 9):
                    # Get children bone's vertices.
                    if (bone_9_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[9].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[9].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[9].children)):
                                        bone_9_verts.append(0)
                                        bones_vertices.append(9)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[9].children[w].head[0], \
                                                                                     bones[9].children[w].head[1], \
                                                                                     bones[9].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 9: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[9].head[0])
                                        bones_vertices_y_root.append(bones[9].head[1])
                                        bones_vertices_z_root.append(bones[9].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_9_parents_checked = True
                        bone_9_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_9_verts.append(0)
                    bones_vertices.append(9)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[9].head[0])
                    bones_vertices_y_root.append(bones[9].head[1])
                    bones_vertices_z_root.append(bones[9].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 10):
                    # Get children bone's vertices.
                    if (bone_10_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[10].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[10].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[10].children)):
                                        bone_10_verts.append(0)
                                        bones_vertices.append(10)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[10].children[w].head[0], \
                                                                                     bones[10].children[w].head[1], \
                                                                                     bones[10].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 10: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[10].head[0])
                                        bones_vertices_y_root.append(bones[10].head[1])
                                        bones_vertices_z_root.append(bones[10].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_10_parents_checked = True
                        bone_10_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_10_verts.append(0)
                    bones_vertices.append(10)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[10].head[0])
                    bones_vertices_y_root.append(bones[10].head[1])
                    bones_vertices_z_root.append(bones[10].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 11):
                    # Get children bone's vertices.
                    if (bone_11_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[11].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[11].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[11].children)):
                                        bone_11_verts.append(0)
                                        bones_vertices.append(11)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[11].children[w].head[0], \
                                                                                     bones[11].children[w].head[1], \
                                                                                     bones[11].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 11: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[11].head[0])
                                        bones_vertices_y_root.append(bones[11].head[1])
                                        bones_vertices_z_root.append(bones[11].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_11_parents_checked = True
                        bone_11_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_11_verts.append(0)
                    bones_vertices.append(11)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[11].head[0])
                    bones_vertices_y_root.append(bones[11].head[1])
                    bones_vertices_z_root.append(bones[11].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 12):
                    # Get children bone's vertices.
                    if (bone_12_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[12].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[12].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[12].children)):
                                        bone_12_verts.append(0)
                                        bones_vertices.append(12)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[12].children[w].head[0], \
                                                                                     bones[12].children[w].head[1], \
                                                                                     bones[12].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 12: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[12].head[0])
                                        bones_vertices_y_root.append(bones[12].head[1])
                                        bones_vertices_z_root.append(bones[12].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_12_parents_checked = True
                        bone_12_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_12_verts.append(0)
                    bones_vertices.append(12)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[12].head[0])
                    bones_vertices_y_root.append(bones[12].head[1])
                    bones_vertices_z_root.append(bones[12].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 13):
                    # Get children bone's vertices.
                    if (bone_13_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[13].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[13].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[13].children)):
                                        bone_13_verts.append(0)
                                        bones_vertices.append(13)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[13].children[w].head[0], \
                                                                                     bones[13].children[w].head[1], \
                                                                                     bones[13].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 13: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[13].head[0])
                                        bones_vertices_y_root.append(bones[13].head[1])
                                        bones_vertices_z_root.append(bones[13].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_13_parents_checked = True
                        bone_13_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_13_verts.append(0)
                    bones_vertices.append(13)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[13].head[0])
                    bones_vertices_y_root.append(bones[13].head[1])
                    bones_vertices_z_root.append(bones[13].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 14):
                    # Get children bone's vertices.
                    if (bone_14_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[14].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[14].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[14].children)):
                                        bone_14_verts.append(0)
                                        bones_vertices.append(14)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[14].children[w].head[0], \
                                                                                     bones[14].children[w].head[1], \
                                                                                     bones[14].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 14: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[14].head[0])
                                        bones_vertices_y_root.append(bones[14].head[1])
                                        bones_vertices_z_root.append(bones[14].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_14_parents_checked = True
                        bone_14_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_14_verts.append(0)
                    bones_vertices.append(14)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[14].head[0])
                    bones_vertices_y_root.append(bones[14].head[1])
                    bones_vertices_z_root.append(bones[14].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 15):
                    # Get children bone's vertices.
                    if (bone_15_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[15].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[15].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[15].children)):
                                        bone_15_verts.append(0)
                                        bones_vertices.append(15)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[15].children[w].head[0], \
                                                                                     bones[15].children[w].head[1], \
                                                                                     bones[15].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 15: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[15].head[0])
                                        bones_vertices_y_root.append(bones[15].head[1])
                                        bones_vertices_z_root.append(bones[15].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_15_parents_checked = True
                        bone_15_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_15_verts.append(0)
                    bones_vertices.append(15)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[15].head[0])
                    bones_vertices_y_root.append(bones[15].head[1])
                    bones_vertices_z_root.append(bones[15].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 16):
                    # Get children bone's vertices.
                    if (bone_16_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[16].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[16].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[16].children)):
                                        bone_16_verts.append(0)
                                        bones_vertices.append(16)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[16].children[w].head[0], \
                                                                                     bones[16].children[w].head[1], \
                                                                                     bones[16].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 16: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[16].head[0])
                                        bones_vertices_y_root.append(bones[16].head[1])
                                        bones_vertices_z_root.append(bones[16].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_16_parents_checked = True
                        bone_16_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_16_verts.append(0)
                    bones_vertices.append(16)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[16].head[0])
                    bones_vertices_y_root.append(bones[16].head[1])
                    bones_vertices_z_root.append(bones[16].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 17):
                    # Get children bone's vertices.
                    if (bone_17_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[17].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[17].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[17].children)):
                                        bone_17_verts.append(0)
                                        bones_vertices.append(17)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[17].children[w].head[0], \
                                                                                     bones[17].children[w].head[1], \
                                                                                     bones[17].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 17: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[17].head[0])
                                        bones_vertices_y_root.append(bones[17].head[1])
                                        bones_vertices_z_root.append(bones[17].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_17_parents_checked = True
                        bone_17_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_17_verts.append(0)
                    bones_vertices.append(17)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[17].head[0])
                    bones_vertices_y_root.append(bones[17].head[1])
                    bones_vertices_z_root.append(bones[17].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 18):
                    # Get children bone's vertices.
                    if (bone_18_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[18].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[18].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[18].children)):
                                        bone_18_verts.append(0)
                                        bones_vertices.append(18)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[18].children[w].head[0], \
                                                                                     bones[18].children[w].head[1], \
                                                                                     bones[18].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 18: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[18].head[0])
                                        bones_vertices_y_root.append(bones[18].head[1])
                                        bones_vertices_z_root.append(bones[18].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_18_parents_checked = True
                        bone_18_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_18_verts.append(0)
                    bones_vertices.append(18)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[18].head[0])
                    bones_vertices_y_root.append(bones[18].head[1])
                    bones_vertices_z_root.append(bones[18].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 19):
                    # Get children bone's vertices.
                    if (bone_19_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[19].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[19].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[19].children)):
                                        bone_19_verts.append(0)
                                        bones_vertices.append(19)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[19].children[w].head[0], \
                                                                                     bones[19].children[w].head[1], \
                                                                                     bones[19].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 19: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[19].head[0])
                                        bones_vertices_y_root.append(bones[19].head[1])
                                        bones_vertices_z_root.append(bones[19].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_19_parents_checked = True
                        bone_19_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_19_verts.append(0)
                    bones_vertices.append(19)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[19].head[0])
                    bones_vertices_y_root.append(bones[19].head[1])
                    bones_vertices_z_root.append(bones[19].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                    
                if (vg == 20):
                    # Get children bone's vertices.
                    if (bone_20_parents_checked == False):
                        # Check if this bone has children.
                        if (len(bones[20].children) >= 1):
                            # Check for 30 possible child bones.
                            for q in range(0, 30):
                                # Check if this child is a part of this bone.
                                if (len(bones[20].children) == q):
                                    # Loop through each child in this bone.
                                    for w in range(0, len(bones[20].children)):
                                        bone_20_verts.append(0)
                                        bones_vertices.append(20)
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[20].children[w].head[0], \
                                                                                     bones[20].children[w].head[1], \
                                                                                     bones[20].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 20: " + str(w))
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[20].head[0])
                                        bones_vertices_y_root.append(bones[20].head[1])
                                        bones_vertices_z_root.append(bones[20].head[2])
                                        
                                        bones_normals_x.append(0)
                                        bones_normals_y.append(0)
                                        bones_normals_z.append(0)
                        else:
                            bone_20_parents_checked = True
                        bone_20_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_20_verts.append(0)
                    bones_vertices.append(20)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[20].head[0])
                    bones_vertices_y_root.append(bones[20].head[1])
                    bones_vertices_z_root.append(bones[20].head[2])
                        
                    bones_normals_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[0])
                    bones_normals_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[1])
                    bones_normals_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].normal[2])
                
                # Decided not to repeat this code for now.
                # This script was mainly used for Twinsen, who uses less bones.
                # So, it just seemed better to leave it as is.
                if (vg == 21):
                    bone_21_verts.append(0)
                if (vg == 22):
                    bone_22_verts.append(0)
                if (vg == 23):
                    bone_23_verts.append(0)
                if (vg == 24):
                    bone_24_verts.append(0)
                if (vg == 25):
                    bone_25_verts.append(0)
                if (vg == 26):
                    bone_26_verts.append(0)
                if (vg == 27):
                    bone_27_verts.append(0)
                if (vg == 28):
                    bone_28_verts.append(0)
                if (vg == 29):
                    bone_29_verts.append(0)

# Loop through bones.
for i in range(0, len(bones)):
    if (i == 0):
        bones_parents_indices.append(int(-1))
    if (i == 1):
        bones_parents_indices.append(int(0))
    if (i >= 2):
        bonesStr = bones[i].parent.name
        bonesStr = bonesStr.lstrip('Bone.')
        bones_parents_indices.append(int(bonesStr))

for i in range(0, len(bpy.data.objects["Mesh"].data.vertices) + len(bones)):
    # Vertices.
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.scene.objects.active.location = (bones_vertices_x[i], bones_vertices_y[i], bones_vertices_z[i])
    bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
    vertices.append(bpy.context.scene.objects.active)
    bpy.context.scene.objects.active.name = ("v%03d" % i)
    #if (i < 10):
    #    bpy.context.scene.objects.active.name = ("v00" + str(i))
    #if (i >= 10 and i < 100):
    #    bpy.context.scene.objects.active.name = ("v0" + str(i))
    #if (i >= 100):
    #    bpy.context.scene.objects.active.name = ("v" + str(i))

for i in range(0, len(bpy.data.objects["Mesh"].data.vertices) + len(bones)):
    # Normals.
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.scene.objects.active.location = (bones_normals_x[i], \
                                                 bones_normals_y[i], \
                                                 bones_normals_z[i])
    bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
    bpy.context.scene.objects.active.parent = vertices[i]
    normals.append(bpy.context.scene.objects.active)
    bpy.context.scene.objects.active.name = ("n%03d" % i)
    #if (i < 10):
    #    bpy.context.scene.objects.active.name = ("n00" + str(i))
    #if (i >= 10 and i < 100):
    #    bpy.context.scene.objects.active.name = ("n0" + str(i))
    #if (i >= 100):
    #    bpy.context.scene.objects.active.name = ("n" + str(i))

# Loop through bones.
for i in range(0, len(bones)):
    # Loop through vertices.
    for j in range(0, len(vertices)):
        if (distance(bones_root_vertices[i].location, vertices[j].location) <= 0.01):
            
            # Append vertex roots.
            verticesStr = vertices[j].name
            verticesStr = verticesStr.lstrip('v')
            bones_root_indices.append(int(verticesStr))

# Get triangles from existing mesh.
for poly in bpy.data.objects["Mesh"].data.polygons:
    
    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
        vert_from_poly = bpy.data.objects["Mesh"].data.loops[loop_index].vertex_index
        
        triangles_x.append(bpy.data.objects["Mesh"].data.vertices[vert_from_poly].co[0])
        triangles_y.append(bpy.data.objects["Mesh"].data.vertices[vert_from_poly].co[1])
        triangles_z.append(bpy.data.objects["Mesh"].data.vertices[vert_from_poly].co[2])

# Create new triangles from existing mesh.
for i in range(0, len(bpy.data.objects["Mesh"].data.polygons)):
    vert = [(triangles_x[triangle_index + 0], triangles_y[triangle_index + 0], triangles_z[triangle_index + 0]),
            (triangles_x[triangle_index + 1], triangles_y[triangle_index + 1], triangles_z[triangle_index + 1]),
            (triangles_x[triangle_index + 2], triangles_y[triangle_index + 2], triangles_z[triangle_index + 2])]
    
    triangle_index += 3

    face = [(0, 1, 2)]
    edge = [(0,1), (1,2), (2,0)]

    my_mesh = bpy.data.meshes.new("t")
    
    my_obj = bpy.data.objects.new(("t%03d" % triangle_index_1), my_mesh)
    triangles.append(my_obj)
    #if (triangle_index_1 < 10):
    #    my_obj = bpy.data.objects.new("t00" + str(triangle_index_1), my_mesh)
    #    triangles.append(my_obj)
    #if (triangle_index_1 >= 10 and triangle_index_1 < 100):
    #    my_obj = bpy.data.objects.new("t0" + str(triangle_index_1), my_mesh)
    #    triangles.append(my_obj)
    #if (triangle_index_1 >= 100):
    #    my_obj = bpy.data.objects.new("t" + str(triangle_index_1), my_mesh)
    #    triangles.append(my_obj)
    
    triangle_index_1 += 1

    my_obj.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(my_obj)

    my_mesh.from_pydata(vert,[],face)
    my_mesh.update(calc_edges=True)

# Loop through new triangles.
for i in range(0, len(triangles)):
    # Loop through new vertices.
    for j in range(0, len(vertices)):
        
        # Compare the distances.
        if (distance(vertices[j].location, triangles[i].data.vertices[0].co) <= 0.001):
            triangles_1.append(int(j))
            
        if (distance(vertices[j].location, triangles[i].data.vertices[1].co) <= 0.001):
            triangles_2.append(int(j))
            
        if (distance(vertices[j].location, triangles[i].data.vertices[2].co) <= 0.001):
            triangles_3.append(int(j))

# Deselect all objects.
bpy.ops.object.select_all(action='DESELECT')

# Select armature and mesh objects.
bpy.data.objects["Mesh"].select = True
bpy.data.objects["Armature"].select = True

# Move them to the second layer.
bpy.ops.object.move_to_layer(layers=(False, True, False, False, False, \
                                     False, False, False, False, False, \
                                     False, False, False, False, False, \
                                     False, False, False, False, False))

bone_all_verts.append(bone_0_verts)
bone_all_verts.append(bone_1_verts)
bone_all_verts.append(bone_2_verts)
bone_all_verts.append(bone_3_verts)
bone_all_verts.append(bone_4_verts)
bone_all_verts.append(bone_5_verts)
bone_all_verts.append(bone_6_verts)
bone_all_verts.append(bone_7_verts)
bone_all_verts.append(bone_8_verts)
bone_all_verts.append(bone_9_verts)
bone_all_verts.append(bone_10_verts)
bone_all_verts.append(bone_11_verts)
bone_all_verts.append(bone_12_verts)
bone_all_verts.append(bone_13_verts)
bone_all_verts.append(bone_14_verts)
bone_all_verts.append(bone_15_verts)
bone_all_verts.append(bone_16_verts)
bone_all_verts.append(bone_17_verts)
bone_all_verts.append(bone_18_verts)
bone_all_verts.append(bone_19_verts)
bone_all_verts.append(bone_20_verts)
bone_all_verts.append(bone_21_verts)
bone_all_verts.append(bone_22_verts)
bone_all_verts.append(bone_23_verts)
bone_all_verts.append(bone_24_verts)
bone_all_verts.append(bone_25_verts)
bone_all_verts.append(bone_26_verts)
bone_all_verts.append(bone_27_verts)
bone_all_verts.append(bone_28_verts)
bone_all_verts.append(bone_29_verts)

# Lots of debug messages.
#print("bones: " + str(len(bones)))
#print("extra_verts: " + str(extra_verts))
#print("vertices: " + str(vertices))
#print("bones: " + str(bones))
#print("bones parents: " + str(bones_parents))
#print("bones parents indices: " + str(bones_parents_indices))
#print("bones vertices: " + str(bones_vertices))
#print("roots: " + str(bones_root_vertices))
#print("roots indices: " + str(bones_root_indices))
#print("triangles 1: " + str(len(triangles_1)))
#print("triangles 2: " + str(len(triangles_2)))
#print("triangles 3: " + str(len(triangles_3)))
#print("bone vertices 0: " + str(len(bone_0_verts)))
#print("bone vertices 1: " + str(len(bone_1_verts)))
#print("bone vertices 2: " + str(len(bone_2_verts)))
#print("bone vertices 3: " + str(len(bone_3_verts)))

#print(bone_all_verts)

# For now, assign colors.
for i in range(0, len(triangles)):
    triangles_colors.append(0xC0)



# +---------------+
# | Model Export. |
# +---------------+

outfile = open(model_path, 'wb')

for i in range(0, 0x60):
    outfile.write(struct.pack('B', 0x00))

for i in range(0, len(bones)):
    outfile.write(struct.pack('h', bones_parents_indices[i])) # Parent Bone
    outfile.write(struct.pack('h', bones_root_indices[i])) # Parent Vertex
    outfile.write(struct.pack('h', len(bone_all_verts[i]))) # Number Of Vertices
    outfile.write(struct.pack('h', 0x00))

# Vertices.
for i in range(0, len(vertices)):
    
    if (i >= 2):
        outfile.write(struct.pack('h', int((-bones_vertices_x[i] + bones_vertices_x_root[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bones_vertices_z[i] - bones_vertices_z_root[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bones_vertices_y[i] - bones_vertices_y_root[i]) * global_scale)))
    else:
        # Align the model to the ground.
        outfile.write(struct.pack('h', int((-bones_vertices_x[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bones_vertices_z[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bones_vertices_y[i]) * global_scale)))
    
    outfile.write(struct.pack('h', bones_vertices[i]))

# Normals.
for i in range(0, len(normals)):
    outfile.write(struct.pack('h', int(-bones_normals_x[i] * global_scale * normal_scale)))
    outfile.write(struct.pack('h', int( bones_normals_z[i] * global_scale * normal_scale)))
    outfile.write(struct.pack('h', int( bones_normals_y[i] * global_scale * normal_scale)))
    
    outfile.write(struct.pack('h', bones_vertices[i]))

for i in range(0, len(triangles)):
    outfile.write(struct.pack('B', 0x05)) # Material
    outfile.write(struct.pack('B', 0x00)) # Triangle / Quad
    outfile.write(struct.pack('B', 0x01)) # 1 Triangle
    outfile.write(struct.pack('B', 0x00))
    outfile.write(struct.pack('B', 0x14)) # Size In Bytes
    outfile.write(struct.pack('B', 0x00))
    outfile.write(struct.pack('B', 0x00))
    outfile.write(struct.pack('B', 0x00))
    
    outfile.write(struct.pack('h', triangles_1[i])) # Vertex Index 1
    outfile.write(struct.pack('h', triangles_2[i])) # Vertex Index 2
    outfile.write(struct.pack('h', triangles_3[i])) # Vertex Index 3
    outfile.write(struct.pack('h', 0x00))
    outfile.write(struct.pack('B', triangles_colors[i])) # Color
    outfile.write(struct.pack('B', 0x10))
    outfile.write(struct.pack('h', 0x00))

outfile.seek(BONES, 0)
outfile.write(struct.pack('h', len(bones)))

outfile.seek(BONES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER))

outfile.seek(VERTICES, 0)
outfile.write(struct.pack('h', len(vertices)))

outfile.seek(VERTICES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8)))

outfile.seek(NORMALS, 0)
outfile.write(struct.pack('h', len(normals)))

outfile.seek(NORMALS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8)))

outfile.seek(UNKNOWNS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8) + (len(normals) * 8)))

outfile.seek(POLYGONS, 0)
outfile.write(struct.pack('h', len(triangles)))

outfile.seek(POLYGONS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8) + (len(normals) * 8)))

outfile.seek(LINES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8) + (len(normals) * 8) + (len(triangles) * 0x14)))

outfile.seek(SPHERES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8) + (len(normals) * 8) + (len(triangles) * 0x14)))

outfile.seek(TEXTURES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(bones) * 8) + (len(vertices) * 8) + (len(normals) * 8) + (len(triangles) * 0x14)))

outfile.close()