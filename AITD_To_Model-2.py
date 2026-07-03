# Cons over the second version
# 1 - Same Weighting Method (Bones must be weighted in order whose values are either 0 or 1)

# Pros over the second version
# 1 - Smaller Script
# 2 - Faster Export Time
# 3 - Edit Vertex Positions Before Export
# 4 - Place Materials On Model Before Export



# Import libraries
import os, bpy, sys, struct
from math import sqrt, radians
from mathutils import Vector, Matrix

# Clear debug messages
os.system("cls")



# Paths
model_path = "C:\\Users\\Parker\\Downloads\\custom_aitd.dat"

# Macros
MAX_BONES       = 30

MATERIAL_FLAT = 0x00
MATERIAL_STIPPLED = 0x01

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

bonesVerticesXCopy = []
bonesVerticesYCopy = []
bonesVerticesZCopy = []

bonesOffsetsX = []
bonesOffsetsY = []
bonesOffsetsZ = []

bonesVertices = []

bonesVerticesOffsets = []

boneTempOffset = 0

# Object variables
triangles0 = []
triangles1 = []
triangles2 = []

polyColors = []

me = bpy.context.object.data
armature = bpy.context.scene.objects['Armature']

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

# Scale variables
global_scale = 300



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

bonesVertices.append(0)

# Append the tail of the first bone's position
bonesVerticesX.append(bones[0].tail[0])
bonesVerticesY.append(bones[0].tail[1])
bonesVerticesZ.append(bones[0].tail[2])

bonesOffsetsX.append(bones[0].tail[0])
bonesOffsetsY.append(bones[0].tail[1])
bonesOffsetsZ.append(bones[0].tail[2])

bonesVertices.append(0)

# Append the tail of the second bone's position
bonesVerticesX.append(bones[1].tail[0])
bonesVerticesY.append(bones[1].tail[1])
bonesVerticesZ.append(bones[1].tail[2])

bonesOffsetsX.append(bones[1].tail[0])
bonesOffsetsY.append(bones[1].tail[1])
bonesOffsetsZ.append(bones[1].tail[2])

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
                        
                        bonesOffsetsX.append(bones[vg].head[0])
                        bonesOffsetsY.append(bones[vg].head[1])
                        bonesOffsetsZ.append(bones[vg].head[2])
                        
                        bonesVertices.append(vg)
                        
                        bonesNumVerts[vg].append(0)

# Begin the export
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

outfile.write(struct.pack('h', len(bonesVertices)))
for i in range(0, len(bonesVertices)):
    
    # Make copies of the original vertex positions.
    bonesVerticesXCopy.append(bonesVerticesX[i])
    bonesVerticesYCopy.append(bonesVerticesY[i])
    bonesVerticesZCopy.append(bonesVerticesZ[i])
    
    # Rotate vertices.
    theVec = Vector()
    theVec.x = bonesVerticesX[i]
    theVec.y = bonesVerticesY[i]
    theVec.z = bonesVerticesZ[i]
    theVec = theVec * rotmat
    
    # Rotate root vertices.
    rootVec = Vector()
    rootVec.x = bonesOffsetsX[i]
    rootVec.y = bonesOffsetsY[i]
    rootVec.z = bonesOffsetsZ[i]
    rootVec = rootVec * rotmat
    
    # Re-assign vertices.
    bonesVerticesX[i] = theVec.x
    bonesVerticesY[i] = theVec.y
    bonesVerticesZ[i] = theVec.z
    
    # Re-assign root vertices.
    bonesOffsetsX[i] = rootVec.x
    bonesOffsetsY[i] = rootVec.y
    bonesOffsetsZ[i] = rootVec.z
    
    if (i >= 2):
        outfile.write(struct.pack('h', int((bonesVerticesX[i] - bonesOffsetsX[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bonesVerticesY[i] - bonesOffsetsY[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bonesVerticesZ[i] - bonesOffsetsZ[i]) * global_scale)))
    else:
        outfile.write(struct.pack('h', int((bonesVerticesX[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bonesVerticesY[i]) * global_scale)))
        outfile.write(struct.pack('h', int((bonesVerticesZ[i]) * global_scale)))

# Loop through bones
for i in range(0, len(armature.pose.bones)):
    # Loop through vertices
    for j in range(0, len(bonesVertices)):
        # Get reference vertex
        # Use the copies from earlier since the originals got rotated by the matrix
        vertRef = [bonesVerticesXCopy[j], bonesVerticesYCopy[j], bonesVerticesZCopy[j]]
        
        # Get distance from vertex to bone
        if (distance(bones[i].head, vertRef) <= 0.001):
            bonesParentsVertices.append(j)

# Loop through polygons
for i in range(0, len(me.polygons)):
    # Get vertex indices from polygon
    v0 = me.polygons[i].vertices[0]
    v1 = me.polygons[i].vertices[1]
    v2 = me.polygons[i].vertices[2]
    
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
        vertRef = [bonesVerticesXCopy[j], bonesVerticesYCopy[j], bonesVerticesZCopy[j]]
        
        # Get distance from vertex to reference vertex
        # These will be used in the place of the triangle vertex indices
        if (distance(vert0, vertRef) <= 0.001):
            triangles0.append(int(j))
            
        if (distance(vert1, vertRef) <= 0.001):
            triangles1.append(int(j))
            
        if (distance(vert2, vertRef) <= 0.001):
            triangles2.append(int(j))

# Bone index datas.
outfile.write(struct.pack('h', len(armature.pose.bones)))
for i in range(0, (len(armature.pose.bones)*2)):
    outfile.write(struct.pack('B', edwardCarnbyBones[i]))

# Calculate running total for bone vertex offsets.
for boneVerts in bonesNumVerts:
    bonesVerticesOffsets.append(boneTempOffset)
    boneTempOffset += len(boneVerts)

# Bone datas.
for i in range(0, len(armature.pose.bones)):
    outfile.write(struct.pack('h', int(bonesVerticesOffsets[i] * 6))) # startIndex
    outfile.write(struct.pack('h', int(len(bonesNumVerts[i])))) # numPoints
    outfile.write(struct.pack('h', int(bonesParentsVertices[i] * 6))) # vertexIndex
    outfile.write(struct.pack('b', int(bonesParentsNames[i]))) # parentIndex
    
    outfile.write(struct.pack('B', i)) # boneIndex
    for j in range(0, 0x08):
        outfile.write(struct.pack('B', 0x00)) # Padding

# Get poly colors.
for face in bpy.context.active_object.data.polygons:
    mat = bpy.context.active_object.data.materials[face.material_index]

    mat_index = 0
    if mat and mat.name.startswith("DOS_PAL_"):
        mat_index = int(mat.name.split("_")[-1])

    polyColors.append(mat_index)

# Polygon datas.
outfile.write(struct.pack('h', len(me.polygons)))
for i in range(0, len(me.polygons)):
    outfile.write(struct.pack('B', 0x01)) # 1 Primitive
    outfile.write(struct.pack('B', 0x03)) # 3 Points (Triangle)
    outfile.write(struct.pack('B', MATERIAL_FLAT)) # Material (0x00 = Flat, 0x01 = Stippled)
    outfile.write(struct.pack('B', polyColors[i])) # Color
    outfile.write(struct.pack('h', triangles1[i] * 6))
    outfile.write(struct.pack('h', triangles0[i] * 6))
    outfile.write(struct.pack('h', triangles2[i] * 6))

# Close the file
outfile.close()
