# Cons over the second version
# 1 - Same Weighting Method (Bones must be weighted in order whose values are either 0 or 1)

# Pros over the second version
# 1 - Smaller Script
# 2 - Faster Export Time
# 3 - Edit Vertex Positions Before Export
# 4 - Place Materials On Model Before Export
# 5 - Supports Texture Mapping



# Import libraries
import os, bpy, sys, struct
from math import sqrt

# Clear debug messages
os.system("cls")



# Paths
model_path = "C:\\Users\\Parker\\Downloads\\custom_lba2.lm2"

# Macros
MAX_BONES       = 30
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

# Used for solid colors
MATERIAL_FLAT = 0x01
MATERIAL_GLASS = 0x02
MATERIAL_TRANSPARENT = 0x03
MATERIAL_CELL_SHADED = 0x04
MATERIAL_DITHERED = 0x05
MATERIAL_SPECULAR = 0x06

MATERIAL_REFLECTION_MAP = 0x08

# Used for texture mapping
MATERIAL_TEXTURED_CELL_SHADED = 0x0A
MATERIAL_TEXTURED_DITHERED = 0x0B
MATERIAL_TEXTURED_LIGHT = 0x0C
MATERIAL_TEXTURED_DARK = 0x0D
MATERIAL_TEXTURED_CELL_SHADED_ALPHA = 0x0E
MATERIAL_TEXTURED_DITHERED_ALPHA = 0x0F

COLOR_RED    = 0x40
COLOR_GREEN  = 0x80
COLOR_BLUE   = 0xC0
COLOR_YELLOW = 0x60
COLOR_ORANGE = 0x50
COLOR_TAN    = 0x20
COLOR_GRAY   = 0x30
COLOR_BROWN  = 0x10

# Variables
current_tri = 0
textured_tris = 0
totalVerts = 0
currentVert = 0
finalOffset = 0
hasTexture = False

colorsRed     = [1.0, 0.0, 0.0]
colorsGreen   = [0.0, 1.0, 0.0]
colorsBlue    = [0.0, 0.0, 1.0]
colorsYellow  = [1.0, 1.0, 0.0]
colorsOrange  = [1.0, 0.5, 0.0]
colorsTan     = [1.0, 1.0, 0.75]
colorsGray    = [0.5, 0.5, 0.5]
colorsBrown   = [0.5, 0.25, 0.0]
colorsTexture = [0.0, 0.0, 0.0]

# Bone variables
bones = []
bonesPose = []
bonesParents = []
bonesParentsNames = []
bonesParentsVertices = []

bonesChecked = [False,False,False,False,False, \
                False,False,False,False,False, \
                False,False,False,False,False, \
                False,False,False,False,False, \
                False,False,False,False,False, \
                False,False,False,False,False]

# 30 slots for bone vertices
bonesNumVerts = [[],[],[],[],[], \
                [],[],[],[],[], \
                [],[],[],[],[], \
                [],[],[],[],[], \
                [],[],[],[],[], \
                [],[],[],[],[]]

bonesVerticesX = []
bonesVerticesY = []
bonesVerticesZ = []

bonesNormalsX = []
bonesNormalsY = []
bonesNormalsZ = []

bonesOffsetsX = []
bonesOffsetsY = []
bonesOffsetsZ = []

bonesVertices = []

# Object variables
triangles0 = []
triangles1 = []
triangles2 = []

triangleLoops = []

triangles_u0 = []
triangles_v0 = []
triangles_u1 = []
triangles_v1 = []
triangles_u2 = []
triangles_v2 = []

polyColors = []

me = bpy.context.object.data
uv_layer = me.uv_layers.active.data
armature = bpy.context.scene.objects['Armature']
armatureData = bpy.data.armatures['Armature']

# Scale variables
global_scale = 100
normal_scale = 150



# Functions
def distance(first, second):
    x = second[0] - first[0]
    y = second[1] - first[1]
    z = second[2] - first[2]
    
    distance = sqrt((x)**2 + (y)**2 + (z)**2)
    return distance



# Get pose bones in the order they exist in the armature
for i in range(0, MAX_BONES):
    if (i == 0):
        bonesPose.append(bpy.data.objects["Armature"].pose.bones.get("Bone"))
    else:
        bonesPose.append(bpy.data.objects["Armature"].pose.bones.get("Bone.%03d" % i))

# Loop through the pose bones we appended and check if they really exist
for i in range(0, len(bonesPose)):
    if (bonesPose[i] is not None):
        # If they do exist then append the actual bones and their parents
        bones.append(bonesPose[i])
        bonesParents.append(bonesPose[i].parent)
        
        # Check parents names and append them as ints for later
        if (bonesPose[i].parent is not None):
            if (i == 1):
                bonesParentsNames.append(0)
            else:
                name = bonesPose[i].parent.name
                name = name.lstrip("Bone.")
                bonesParentsNames.append(name)
        else:
            bonesParentsNames.append(-1)

# Append the head of the first bone's position
bonesVerticesX.append(bones[0].head[0])
bonesVerticesY.append(bones[0].head[1])
bonesVerticesZ.append(bones[0].head[2])

bonesOffsetsX.append(bones[0].head[0])
bonesOffsetsY.append(bones[0].head[1])
bonesOffsetsZ.append(bones[0].head[2])

bonesNormalsX.append(0)
bonesNormalsY.append(0)
bonesNormalsZ.append(0)

bonesVertices.append(0)

# Append the tail of the first bone's position
bonesVerticesX.append(bones[0].tail[0])
bonesVerticesY.append(bones[0].tail[1])
bonesVerticesZ.append(bones[0].tail[2])

bonesOffsetsX.append(bones[0].tail[0])
bonesOffsetsY.append(bones[0].tail[1])
bonesOffsetsZ.append(bones[0].tail[2])

bonesNormalsX.append(0)
bonesNormalsY.append(0)
bonesNormalsZ.append(0)

bonesVertices.append(0)

# Append the tail of the second bone's position
bonesVerticesX.append(bones[1].tail[0])
bonesVerticesY.append(bones[1].tail[1])
bonesVerticesZ.append(bones[1].tail[2])

bonesOffsetsX.append(bones[1].tail[0])
bonesOffsetsY.append(bones[1].tail[1])
bonesOffsetsZ.append(bones[1].tail[2])

bonesNormalsX.append(0)
bonesNormalsY.append(0)
bonesNormalsZ.append(0)

bonesVertices.append(1)

bonesNumVerts[0].append(0)
bonesNumVerts[0].append(0)
bonesNumVerts[1].append(0)

# Loop through pose bones
for bone_id in range(0, len(armature.pose.bones)):
    # Loop through vertices
    for vert in me.vertices:
        # Loop through vertex groups
        for j in vert.groups:
            
            # Get vertex group
            vg = bpy.data.objects["Mesh"].vertex_groups[bone_id].index
            
            # Check if the vertex is in this bone
            if (j.group == vg):
                # Skip first two bones as those vertices are already appended before the loop
                for k in range(2, MAX_BONES):
                    if (vg == k):
                        if (bonesChecked[vg] == False):
                            #print(len(boneNumVerts[vg]))
                            #print("bone %d vert group %d" % (bone_id, vg))
                            
                            # Check for children
                            if (len(bones[vg].children) >= 1):
                                # Check for 30 possible child bones
                                for q in range(0, MAX_BONES):
                                    # Check if this child is a part of this bone
                                    if (len(bones[vg].children) == q):
                                        # Loop through each child in this bone
                                        for w in range(0, len(bones[vg].children)):
                                            bonesVerticesX.append(bones[vg].children[w].head[0])
                                            bonesVerticesY.append(bones[vg].children[w].head[1])
                                            bonesVerticesZ.append(bones[vg].children[w].head[2])
                                            
                                            #print(len(bones[vg].children))
                                                    
                                            bonesNormalsX.append(0)
                                            bonesNormalsY.append(0)
                                            bonesNormalsZ.append(0)
                                            
                                            bonesOffsetsX.append(bones[vg].head[0])
                                            bonesOffsetsY.append(bones[vg].head[1])
                                            bonesOffsetsZ.append(bones[vg].head[2])
                                            
                                            bonesNumVerts[vg].append(0)
                                            
                                            bonesVertices.append(vg)
                            
                            bonesChecked[vg] = True
                        
                        # Get all other vertices in this vertex group
                        bonesVerticesX.append(bpy.data.objects["Mesh"].data.vertices[vert.index].co[0])
                        bonesVerticesY.append(bpy.data.objects["Mesh"].data.vertices[vert.index].co[1])
                        bonesVerticesZ.append(bpy.data.objects["Mesh"].data.vertices[vert.index].co[2])
                        
                        bonesNormalsX.append(bpy.data.objects["Mesh"].data.vertices[vert.index].normal[0])
                        bonesNormalsY.append(bpy.data.objects["Mesh"].data.vertices[vert.index].normal[1])
                        bonesNormalsZ.append(bpy.data.objects["Mesh"].data.vertices[vert.index].normal[2])
                        
                        bonesOffsetsX.append(bones[vg].head[0])
                        bonesOffsetsY.append(bones[vg].head[1])
                        bonesOffsetsZ.append(bones[vg].head[2])
                        
                        bonesVertices.append(vg)
                        
                        bonesNumVerts[vg].append(0)

# Get total number of vertices 
for i in range(0, len(armature.pose.bones)):
    totalVerts += len(bonesNumVerts[i])

# Begin the export
outfile = open(model_path, 'wb')

# Stub the header
for i in range(0, 0x60):
    outfile.write(struct.pack('B', 0x00))

# Loop through bones
for i in range(0, len(armature.pose.bones)):
    # Loop through vertices
    for j in range(0, len(bonesVertices)):
        # Get reference vertex
        vertRef = [bonesVerticesX[j], bonesVerticesY[j], bonesVerticesZ[j]]
        
        # Get distance from vertex to bone
        if (distance(bones[i].head, vertRef) <= 0.001):
            bonesParentsVertices.append(j)

# Write the bones
for i in range(0, len(armature.pose.bones)):
    
    outfile.write(struct.pack('h', int(bonesParentsNames[i]))) # Parent Bone
    outfile.write(struct.pack('h', int(bonesParentsVertices[i]))) # Parent Vertex
    outfile.write(struct.pack('h', int(len(bonesNumVerts[i])))) # Number Of Vertices
    outfile.write(struct.pack('h', 0x00))

# Vertices
for i in range(0, len(bonesVertices)):
    if (i >= 2): # Skip the first two vertices
        outfile.write(struct.pack('h', int((-bonesVerticesX[i] + bonesOffsetsX[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bonesVerticesZ[i] - bonesOffsetsZ[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bonesVerticesY[i] - bonesOffsetsY[i]) * global_scale)))
    else:
        # Align the model to the ground
        outfile.write(struct.pack('h', int((-bonesVerticesX[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bonesVerticesZ[i]) * global_scale)))
        outfile.write(struct.pack('h', int(( bonesVerticesY[i]) * global_scale)))
    outfile.write(struct.pack('h', int(bonesVertices[i])))

# Normals
for i in range(0, len(bonesVertices)):
    outfile.write(struct.pack('h', int((-bonesNormalsX[i]) * global_scale * normal_scale)))
    outfile.write(struct.pack('h', int(( bonesNormalsZ[i]) * global_scale * normal_scale)))
    outfile.write(struct.pack('h', int(( bonesNormalsY[i]) * global_scale * normal_scale)))
    outfile.write(struct.pack('h', int(bonesVertices[i])))

# Get UVs separately as they cannot be done in the same manner as everything else
for poly in me.polygons:
    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
        triangleLoops.append(loop_index)

# Loop through polygons
for i in range(0, len(me.polygons)):
    # Get vertex indices from polygon
    v0 = me.polygons[i].vertices[0]
    v1 = me.polygons[i].vertices[1]
    v2 = me.polygons[i].vertices[2]
    
    # Get vertex texture coordinates
    triangles_u0.append(round(uv_layer[triangleLoops[currentVert + 0]].uv.x * 255))
    triangles_v0.append(round(uv_layer[triangleLoops[currentVert + 0]].uv.y * 255))
    triangles_u1.append(round(uv_layer[triangleLoops[currentVert + 1]].uv.x * 255))
    triangles_v1.append(round(uv_layer[triangleLoops[currentVert + 1]].uv.y * 255))
    triangles_u2.append(round(uv_layer[triangleLoops[currentVert + 2]].uv.x * 255))
    triangles_v2.append(round(uv_layer[triangleLoops[currentVert + 2]].uv.y * 255))
    
    currentVert += 3
    
    # Loop through vertices
    for j in range(0, len(bonesVertices)):
        # Get vertex positions from vertex indices
        vert0 = [bpy.context.object.data.vertices[v0].co[0],
                 bpy.context.object.data.vertices[v0].co[1],
                 bpy.context.object.data.vertices[v0].co[2]]
        vert1 = [bpy.context.object.data.vertices[v1].co[0],
                 bpy.context.object.data.vertices[v1].co[1],
                 bpy.context.object.data.vertices[v1].co[2]]
        vert2 = [bpy.context.object.data.vertices[v2].co[0],
                 bpy.context.object.data.vertices[v2].co[1],
                 bpy.context.object.data.vertices[v2].co[2]]
        
        # Get reference vertex
        vertRef = [bonesVerticesX[j], bonesVerticesY[j], bonesVerticesZ[j]]
        
        # Get distance from vertex to reference vertex
        # These will be used in the place of the triangle vertex indices
        if (distance(vert0, vertRef) <= 0.001):
            triangles0.append(int(j))
            
        if (distance(vert1, vertRef) <= 0.001):
            triangles1.append(int(j))
            
        if (distance(vert2, vertRef) <= 0.001):
            triangles2.append(int(j))

# Polygons
for poly in me.polygons:
    # Get material slots from mesh object
    mat_slots = bpy.data.objects["Mesh"].material_slots
    # Get the material from the slot
    theMat = mat_slots[poly.material_index].material
    colorR = theMat.diffuse_color[0]
    colorG = theMat.diffuse_color[1]
    colorB = theMat.diffuse_color[2]
    
    # Compare colors and append the right data to the triangle
    if (colorR == colorsRed[0] and colorG == colorsRed[1] and colorB == colorsRed[2]):
        polyColors.append(COLOR_RED)
        
    elif (colorR == colorsGreen[0] and colorG == colorsGreen[1] and colorB == colorsGreen[2]):
        polyColors.append(COLOR_GREEN)
        
    elif (colorR == colorsBlue[0] and colorG == colorsBlue[1] and colorB == colorsBlue[2]):
        polyColors.append(COLOR_BLUE)
        
    elif (colorR == colorsYellow[0] and colorG == colorsYellow[1] and colorB == colorsYellow[2]):
        polyColors.append(COLOR_YELLOW)
    
    elif (colorR == colorsOrange[0] and colorG == colorsOrange[1] and colorB == colorsOrange[2]):
        polyColors.append(COLOR_ORANGE)
    
    elif (colorR == colorsTan[0] and colorG == colorsTan[1] and colorB == colorsTan[2]):
        polyColors.append(COLOR_TAN)
    
    elif (colorR == colorsGray[0] and colorG == colorsGray[1] and colorB == colorsGray[2]):
        polyColors.append(COLOR_GRAY)
    
    elif (colorR == colorsBrown[0] and colorG == colorsBrown[1] and colorB == colorsBrown[2]):
        polyColors.append(COLOR_BROWN)
    
    elif (colorR == colorsTexture[0] and colorG == colorsTexture[1] and colorB == colorsTexture[2]):
        polyColors.append(0x01)
    
    else:
        polyColors.append(0x00)
    
    if (polyColors[poly.index] == 0x01): # Textured triangle
        outfile.write(struct.pack('B', MATERIAL_REFLECTION_MAP)) # Material
        outfile.write(struct.pack('B', 0x00)) # Triangle / Quad
        outfile.write(struct.pack('B', 0x01)) # 1 Triangle
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x20)) # Size In Bytes
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x00))
        
        outfile.write(struct.pack('h', triangles0[current_tri])) # Vertex Index 1
        outfile.write(struct.pack('h', triangles1[current_tri])) # Vertex Index 2
        outfile.write(struct.pack('h', triangles2[current_tri])) # Vertex Index 3
        outfile.write(struct.pack('h', 0x00))
        outfile.write(struct.pack('B', polyColors[poly.index])) # Color
        outfile.write(struct.pack('B', 0x10))
        outfile.write(struct.pack('h', 0x00))
        
        # If your texture coordinates still do not export correctly
        # You need to flip the texture in Blender and flip your UV's as well
        # This is the case since LBA2 uses Y as the up-axis, not Z
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_u0[current_tri])))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_v0[current_tri])))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_u1[current_tri])))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_v1[current_tri])))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_u2[current_tri])))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', int(triangles_v2[current_tri])))
        
        current_tri += 1
        textured_tris += 1
        
        # At least one polygon with a texture needs to exist for them to be added to the file
        if (hasTexture == False):
            hasTexture = True
        
    else: # Colored triangle
        outfile.write(struct.pack('B', MATERIAL_DITHERED)) # Material
        outfile.write(struct.pack('B', 0x00)) # Triangle / Quad
        outfile.write(struct.pack('B', 0x01)) # 1 Triangle
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x14)) # Size In Bytes
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x00))
        outfile.write(struct.pack('B', 0x00))
        
        outfile.write(struct.pack('h', triangles0[current_tri])) # Vertex Index 1
        outfile.write(struct.pack('h', triangles1[current_tri])) # Vertex Index 2
        outfile.write(struct.pack('h', triangles2[current_tri])) # Vertex Index 3
        outfile.write(struct.pack('h', 0x00))
        outfile.write(struct.pack('B', polyColors[poly.index])) # Color
        outfile.write(struct.pack('B', 0x10))
        outfile.write(struct.pack('h', 0x00))
    
        current_tri += 1

if (hasTexture == True):
    outfile.write(struct.pack('B', 0x00)) # X
    outfile.write(struct.pack('B', 0x00)) # Y
    outfile.write(struct.pack('B', 0xFF)) # W
    outfile.write(struct.pack('B', 0xFF)) # H

# Go back to the header and fill it out with the right data
outfile.seek(BONES, 0)
outfile.write(struct.pack('h', len(armature.pose.bones)))

outfile.seek(BONES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER))

outfile.seek(VERTICES, 0)
outfile.write(struct.pack('h', totalVerts))

outfile.seek(VERTICES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8)))

outfile.seek(NORMALS, 0)
outfile.write(struct.pack('h', totalVerts))

outfile.seek(NORMALS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts * 8)))

outfile.seek(UNKNOWNS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts * 8) + (totalVerts * 8)))

outfile.seek(POLYGONS, 0)
outfile.write(struct.pack('h', len(me.polygons)))

outfile.seek(POLYGONS_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts* 8) + (totalVerts * 8)))

# Get number of polys, subtract from the textured ones, and return the correct sizes
finalOffset = ((len(me.polygons) - textured_tris) * 0x14) + (textured_tris * 0x20)
print(hex(finalOffset))

outfile.seek(LINES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts * 8) + (totalVerts * 8) + finalOffset))

outfile.seek(SPHERES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts * 8) + (totalVerts * 8) + finalOffset))

if (hasTexture == True):
    outfile.seek(TEXTURES, 0)
    outfile.write(struct.pack('h', 0x01))

outfile.seek(TEXTURES_OFFSET, 0)
outfile.write(struct.pack('h', HEADER + (len(armature.pose.bones) * 8) + (totalVerts * 8) + (totalVerts * 8) + finalOffset))

# Close the file
outfile.close()