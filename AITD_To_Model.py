# Python script to export models to Frederick Raynal's "Alone in the Dark (1992)".
# Programmed by Quilt from the LBA Discord server on 10/26/2021.

import os, bpy, struct
from math import sqrt, radians
from mathutils import Vector, Matrix

os.system("cls")



# Functions.
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



#global_scale = 100
global_scale = 300

# Contains Edward's model flag and bounding box data. (This should be used no matter what model.)
edwardCarnbyHeader = [0x03,0x00,0xC9,0xFE,0x37,0x01,0x0F,0xF9,0x00,0x00,0xA8,0xFF,0xDE,0x00,0x0A,0x00]
# Contains Edward's bone index data. This is used to reference the proper bone indices in animations.
edwardCarnbyBones = [0x50,0x00,0x70,0x00,0xA0,0x00,0xD0,0x00,0x00,0x01,0x40,0x00,0x90,0x00,0xC0,0x00,0xF0,
                     0x00,0x30,0x00,0x80,0x00,0xB0,0x00,0xE0,0x00,0x60,0x00,0x20,0x00,0x10,0x00,0x00,0x00]

# Edward Carnby Bone Structure:
# Bone2: Torso
# Bone3: Left Leg Top
# Bone4: Left Leg Bottom
# Bone5: Left Foot
# Bone6: Chest
# Bone7: Head
# Bone8: Left Arm Top
# Bone9: Left Arm Bottom
# Bone10: Left Hand
# Bone11: Right Arm Top
# Bone12: Right Arm Bottom
# Bone13: Right Hand
# Bone14: Right Leg Top
# Bone15: Right Leg Bottom
# Bone16: Right Foot
# Bone17: Lamp (Connected to Bone13)

# Vertex indices.
vertices = []

# Triangle properties.
triangles = []

triangles_x = []
triangles_y = []
triangles_z = []

triangles_1 = []
triangles_2 = []
triangles_3 = []

triangles_colors = []
triangle_normals = [] # Used for coloring (shading) the polygons.

triangle_index = 0
triangle_index_1 = 0



# Bone properties.
bones = []
bones_parents = []
bones_parents_indices = []
bones_num = [0]

bones_root_indices = []
bones_root_vertices = []

bones_vertices_x = []
bones_vertices_y = []
bones_vertices_z = []

bones_vertices_x_root = []
bones_vertices_y_root = []
bones_vertices_z_root = []

# Bone checkers.
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
bone_all_verts_offsets = []

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




# Begin sorting model's data.

# Append the head of the first bone's position.
bone_0_verts.append(0)
bones_vertices_x.append(bones[0].head[0])
bones_vertices_y.append(bones[0].head[1])
bones_vertices_z.append(bones[0].head[2])

bones_vertices_x_root.append(bones[0].head[0])
bones_vertices_y_root.append(bones[0].head[1])
bones_vertices_z_root.append(bones[0].head[2])

# Append the tail of the first bone's position.
bone_0_verts.append(0)
bones_vertices_x.append(bones[0].tail[0])
bones_vertices_y.append(bones[0].tail[1])
bones_vertices_z.append(bones[0].tail[2])

bones_vertices_x_root.append(bones[0].tail[0])
bones_vertices_y_root.append(bones[0].tail[1])
bones_vertices_z_root.append(bones[0].tail[2])

# Append the tail of the second bone's position.
bone_1_verts.append(0)
bones_vertices_x.append(bones[1].tail[0])
bones_vertices_y.append(bones[1].tail[1])
bones_vertices_z.append(bones[1].tail[2])

bones_vertices_x_root.append(bones[1].tail[0])
bones_vertices_y_root.append(bones[1].tail[1])
bones_vertices_z_root.append(bones[1].tail[2])

print("bones_num: " + str(bones_num[0]))

# Loop through existing vertex groups.
for i in range(0, bones_num[0]):
    
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.scene.objects.active.location = (bones[i].head[0], bones[i].head[1], bones[i].head[2])
    
    bpy.context.scene.objects.active.scale = (0.07, 0.07, 0.07)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bones_root_vertices.append(bpy.context.scene.objects.active)
    
    bpy.context.scene.objects.active.name = ("b%02d" % (i))
    
    # Set to object mode.
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Loop through existing vertices.
    for j in (bpy.data.objects["Mesh"].data.vertices):
        # Loop through existing vertex indices in vertex groups.
        for k in (j.groups):
            vg = bpy.data.objects["Mesh"].vertex_groups[i].index
            
            # Check if the vertex is in this bone.
            if (k.group == vg):
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[2].children[w].head[0], \
                                                                                     bones[2].children[w].head[1], \
                                                                                     bones[2].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 2: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[2].head[0])
                                        bones_vertices_y_root.append(bones[2].head[1])
                                        bones_vertices_z_root.append(bones[2].head[2])
                                
                        bone_2_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_2_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                    
                    bones_vertices_x_root.append(bones[2].head[0])
                    bones_vertices_y_root.append(bones[2].head[1])
                    bones_vertices_z_root.append(bones[2].head[2])
            
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[3].children[w].head[0], \
                                                                                     bones[3].children[w].head[1], \
                                                                                     bones[3].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 3: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[3].head[0])
                                        bones_vertices_y_root.append(bones[3].head[1])
                                        bones_vertices_z_root.append(bones[3].head[2])
                        else:
                            bone_3_parents_checked = True
                        bone_3_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_3_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                    
                    bones_vertices_x_root.append(bones[3].head[0])
                    bones_vertices_y_root.append(bones[3].head[1])
                    bones_vertices_z_root.append(bones[3].head[2])
            
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[4].children[w].head[0], \
                                                                                     bones[4].children[w].head[1], \
                                                                                     bones[4].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 4: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[4].head[0])
                                        bones_vertices_y_root.append(bones[4].head[1])
                                        bones_vertices_z_root.append(bones[4].head[2])
                        else:
                            bone_4_parents_checked = True
                        bone_4_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_4_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[4].head[0])
                    bones_vertices_y_root.append(bones[4].head[1])
                    bones_vertices_z_root.append(bones[4].head[2])
                
                if (vg == 5):
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[5].children[w].head[0], \
                                                                                     bones[5].children[w].head[1], \
                                                                                     bones[5].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 5: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[5].head[0])
                                        bones_vertices_y_root.append(bones[5].head[1])
                                        bones_vertices_z_root.append(bones[5].head[2])
                        else:
                            bone_5_parents_checked = True
                        bone_5_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_5_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[5].head[0])
                    bones_vertices_y_root.append(bones[5].head[1])
                    bones_vertices_z_root.append(bones[5].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[6].children[w].head[0], \
                                                                                     bones[6].children[w].head[1], \
                                                                                     bones[6].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 6: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[6].head[0])
                                        bones_vertices_y_root.append(bones[6].head[1])
                                        bones_vertices_z_root.append(bones[6].head[2])
                        else:
                            bone_6_parents_checked = True
                        bone_6_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_6_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[6].head[0])
                    bones_vertices_y_root.append(bones[6].head[1])
                    bones_vertices_z_root.append(bones[6].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[7].children[w].head[0], \
                                                                                     bones[7].children[w].head[1], \
                                                                                     bones[7].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 7: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[7].head[0])
                                        bones_vertices_y_root.append(bones[7].head[1])
                                        bones_vertices_z_root.append(bones[7].head[2])
                        else:
                            bone_7_parents_checked = True
                        bone_7_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_7_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[7].head[0])
                    bones_vertices_y_root.append(bones[7].head[1])
                    bones_vertices_z_root.append(bones[7].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[8].children[w].head[0], \
                                                                                     bones[8].children[w].head[1], \
                                                                                     bones[8].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 8: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[8].head[0])
                                        bones_vertices_y_root.append(bones[8].head[1])
                                        bones_vertices_z_root.append(bones[8].head[2])
                        else:
                            bone_8_parents_checked = True
                        bone_8_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_8_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[8].head[0])
                    bones_vertices_y_root.append(bones[8].head[1])
                    bones_vertices_z_root.append(bones[8].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[9].children[w].head[0], \
                                                                                     bones[9].children[w].head[1], \
                                                                                     bones[9].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 6: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[9].head[0])
                                        bones_vertices_y_root.append(bones[9].head[1])
                                        bones_vertices_z_root.append(bones[9].head[2])
                        else:
                            bone_9_parents_checked = True
                        bone_9_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_9_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[9].head[0])
                    bones_vertices_y_root.append(bones[9].head[1])
                    bones_vertices_z_root.append(bones[9].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[10].children[w].head[0], \
                                                                                     bones[10].children[w].head[1], \
                                                                                     bones[10].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 10: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[10].head[0])
                                        bones_vertices_y_root.append(bones[10].head[1])
                                        bones_vertices_z_root.append(bones[10].head[2])
                        else:
                            bone_10_parents_checked = True
                        bone_10_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_10_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[10].head[0])
                    bones_vertices_y_root.append(bones[10].head[1])
                    bones_vertices_z_root.append(bones[10].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[11].children[w].head[0], \
                                                                                     bones[11].children[w].head[1], \
                                                                                     bones[11].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 11: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[11].head[0])
                                        bones_vertices_y_root.append(bones[11].head[1])
                                        bones_vertices_z_root.append(bones[11].head[2])
                        else:
                            bone_11_parents_checked = True
                        bone_11_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_11_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[11].head[0])
                    bones_vertices_y_root.append(bones[11].head[1])
                    bones_vertices_z_root.append(bones[11].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[12].children[w].head[0], \
                                                                                     bones[12].children[w].head[1], \
                                                                                     bones[12].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 12: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[12].head[0])
                                        bones_vertices_y_root.append(bones[12].head[1])
                                        bones_vertices_z_root.append(bones[12].head[2])
                        else:
                            bone_12_parents_checked = True
                        bone_12_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_12_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[12].head[0])
                    bones_vertices_y_root.append(bones[12].head[1])
                    bones_vertices_z_root.append(bones[12].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[13].children[w].head[0], \
                                                                                     bones[13].children[w].head[1], \
                                                                                     bones[13].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 13: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[13].head[0])
                                        bones_vertices_y_root.append(bones[13].head[1])
                                        bones_vertices_z_root.append(bones[13].head[2])
                        else:
                            bone_13_parents_checked = True
                        bone_13_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_13_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[13].head[0])
                    bones_vertices_y_root.append(bones[13].head[1])
                    bones_vertices_z_root.append(bones[13].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[14].children[w].head[0], \
                                                                                     bones[14].children[w].head[1], \
                                                                                     bones[14].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 14: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[14].head[0])
                                        bones_vertices_y_root.append(bones[14].head[1])
                                        bones_vertices_z_root.append(bones[14].head[2])
                        else:
                            bone_14_parents_checked = True
                        bone_14_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_14_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[14].head[0])
                    bones_vertices_y_root.append(bones[14].head[1])
                    bones_vertices_z_root.append(bones[14].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[15].children[w].head[0], \
                                                                                     bones[15].children[w].head[1], \
                                                                                     bones[15].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 15: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[15].head[0])
                                        bones_vertices_y_root.append(bones[15].head[1])
                                        bones_vertices_z_root.append(bones[15].head[2])
                        else:
                            bone_15_parents_checked = True
                        bone_15_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_15_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[15].head[0])
                    bones_vertices_y_root.append(bones[15].head[1])
                    bones_vertices_z_root.append(bones[15].head[2])
                
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
                                        
                                        bpy.ops.mesh.primitive_cube_add()
                                        bpy.context.scene.objects.active.location = (bones[16].children[w].head[0], \
                                                                                     bones[16].children[w].head[1], \
                                                                                     bones[16].children[w].head[2])
                                        bpy.context.scene.objects.active.scale = (0.1, 0.1, 0.1)
                                        bpy.context.scene.objects.active.name = ("branch 16: " + str(w))
                                        
                                        bpy.context.scene.objects.active.hide = True
                                        
                                        bones_vertices_x.append(bpy.context.scene.objects.active.location.x)
                                        bones_vertices_y.append(bpy.context.scene.objects.active.location.y)
                                        bones_vertices_z.append(bpy.context.scene.objects.active.location.z)
                                        
                                        bones_vertices_x_root.append(bones[16].head[0])
                                        bones_vertices_y_root.append(bones[16].head[1])
                                        bones_vertices_z_root.append(bones[16].head[2])
                        else:
                            bone_16_parents_checked = True
                        bone_16_parents_checked = True
                    
                    # Get all other vertices in this vertex group.
                    bone_16_verts.append(0)
                    bones_vertices_x.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[0])
                    bones_vertices_y.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[1])
                    bones_vertices_z.append(bpy.data.objects["Mesh"].data.vertices[j.index].co[2])
                        
                    bones_vertices_x_root.append(bones[16].head[0])
                    bones_vertices_y_root.append(bones[16].head[1])
                    bones_vertices_z_root.append(bones[16].head[2])

print("bone_0_verts: " + str(bone_0_verts))
print("bone_1_verts: " + str(bone_1_verts))
print("bone_2_verts: " + str(bone_2_verts))
print("bone_3_verts: " + str(bone_3_verts))
print("bone_4_verts: " + str(bone_4_verts))

#print(bones_vertices)
#print(bones_vertices_x)
#print(len(bones_vertices_x))
#print(len(bpy.data.objects["Mesh"].data.vertices) + len(bones))

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

# Get vertices from existing mesh.
for i in range(0, len(bpy.data.objects["Mesh"].data.vertices) + len(bones)):
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.scene.objects.active.location = (bones_vertices_x[i], bones_vertices_y[i], bones_vertices_z[i])
    
    bpy.context.scene.objects.active.scale = (0.01, 0.01, 0.01)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    vertices.append(bpy.context.scene.objects.active)
    bpy.context.scene.objects.active.name = ("v%003d" % (i))

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
    
    my_obj = bpy.data.objects.new("t%03d" % (triangle_index_1), my_mesh)
    triangles.append(my_obj)
    
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

# Color triangles.
# This at least covers the polygons of a specific color with "shade".
startOfPalette = 64 # Must be a multiple of 16 and cannot exceed 256.
rowOfPalette = 16
for i in range(0, len(triangles)):
    triangles_colors.append(int(startOfPalette + (i * rowOfPalette) / len(triangles)))
print(triangles_colors)

#for i in range(0, len(triangles)):
#    triangles_colors.append(96)

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

bone_all_verts_offsets.append(0x00)
bone_all_verts_offsets.append(len(bone_0_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts) +
                              len(bone_12_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts) +
                              len(bone_12_verts) +
                              len(bone_13_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts) +
                              len(bone_12_verts) +
                              len(bone_13_verts) +
                              len(bone_14_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts) +
                              len(bone_12_verts) +
                              len(bone_13_verts) +
                              len(bone_14_verts) +
                              len(bone_15_verts))
bone_all_verts_offsets.append(len(bone_0_verts) + 
                              len(bone_1_verts) + 
                              len(bone_2_verts) + 
                              len(bone_3_verts) + 
                              len(bone_4_verts) +
                              len(bone_5_verts) +
                              len(bone_6_verts) +
                              len(bone_7_verts) +
                              len(bone_8_verts) +
                              len(bone_9_verts) +
                              len(bone_10_verts) +
                              len(bone_11_verts) +
                              len(bone_12_verts) +
                              len(bone_13_verts) +
                              len(bone_14_verts) +
                              len(bone_15_verts) +
                              len(bone_16_verts))

print("bone_offsets: " + str(bone_all_verts_offsets))
print("bones_root_indices: " + str(bones_root_indices))

# Begin writing to the model file.
model_path = "C:\\Users\\parke\\OneDrive\\Documents\\aitd_model.dat"

outfile = open(model_path, 'wb')

# Header data.
for i in range(0, len(edwardCarnbyHeader)):
    outfile.write(struct.pack('B', edwardCarnbyHeader[i]))
for i in range(0, 0x0A):
    outfile.write(struct.pack('B', 0x00)) # Padding

# Vertex data.
#rotmat =  Matrix.Rotation(radians(90), 4, 'X') # Rotation matrix to rotate vertices to AitD's up-axis.
rotmat = Matrix.Rotation(radians(-90), 4, 'X')
rotmat = rotmat * Matrix.Rotation(radians(-90), 4, 'Y')

outfile.write(struct.pack('h', len(vertices)))
for i in range(0, len(vertices)):
    
    # Rotate vertices.
    theVec = Vector()
    theVec.x = bones_vertices_x[i]
    theVec.y = bones_vertices_y[i]
    theVec.z = bones_vertices_z[i]
    theVec = theVec * rotmat
    
    # Rotate root vertices.
    rootVec = Vector()
    rootVec.x = bones_vertices_x_root[i]
    rootVec.y = bones_vertices_y_root[i]
    rootVec.z = bones_vertices_z_root[i]
    rootVec = rootVec * rotmat
    
    # Re-assign vertices.
    bones_vertices_x[i] = theVec.x
    bones_vertices_y[i] = theVec.y
    bones_vertices_z[i] = theVec.z
    
    # Re-assign root vertices.
    bones_vertices_x_root[i] = rootVec.x
    bones_vertices_y_root[i] = rootVec.y
    bones_vertices_z_root[i] = rootVec.z
    
    if (i >= 2):
        outfile.write(struct.pack('h', int((bones_vertices_x[i] - bones_vertices_x_root[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bones_vertices_y[i] - bones_vertices_y_root[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bones_vertices_z[i] - bones_vertices_z_root[i]) * global_scale)))
    else:
        outfile.write(struct.pack('h', int((bones_vertices_x[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bones_vertices_y[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bones_vertices_z[i]) * global_scale)))

# Bone index datas.
outfile.write(struct.pack('h', len(bones)))
for i in range(0, (len(bones)*2)):
    outfile.write(struct.pack('B', edwardCarnbyBones[i]))

# Bone datas.
for i in range(0, len(bones)):
    outfile.write(struct.pack('h', int(bone_all_verts_offsets[i] * 6))) # startIndex
    outfile.write(struct.pack('h', len(bone_all_verts[i])))             # numPoints
    outfile.write(struct.pack('h', bones_root_indices[i] * 6))          # vertexIndex
    outfile.write(struct.pack('b', int(bones_parents_indices[i])))      # parentIndex
    
    outfile.write(struct.pack('B', i)) # boneIndex
    for j in range(0, 0x08):
        outfile.write(struct.pack('B', 0x00)) # Padding

outfile.write(struct.pack('h', len(triangles)))
for i in range(0, len(triangles)):
    outfile.write(struct.pack('B', 0x01)) # 1 Primitive
    outfile.write(struct.pack('B', 0x03)) # 3 Points (Triangle)
    outfile.write(struct.pack('B', 0x01)) # Material (0x00 = Flat, 0x01 = Stippled)
    #outfile.write(struct.pack('B', 0x4C)) # Color
    outfile.write(struct.pack('B', triangles_colors[i])) # Color
    outfile.write(struct.pack('h', triangles_2[i] * 6))
    outfile.write(struct.pack('h', triangles_1[i] * 6))
    outfile.write(struct.pack('h', triangles_3[i] * 6))

outfile.close()