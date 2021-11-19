# +----------------------------------------------------------------------------+
# | LBA2 Model Exporter Color Rollout - Blender Python (v2.79)                 |
# |    By Quilty from the LBA Discord server.                                  |
# |                                                                            |
# | Not entirely perfect, but it gets the job done.                            |
# | Though, you will need a hex editor to copy the color data for now.         |
# | This should be resolved as well in the future.                             |
# |                                                                            |
# | 1 - Copy all of the bytes from the "colors only" file.                     |
# | 2 - Go to the bottom of the "custom model" file.                           |
# | 3 - Offset how many bytes are from the "colors only" file and paste.       |
# |                                                                            |
# | The model should now be colored when viewed in a viewer or played in-game. |
# |                                                                            |
# | Make sure you edit the paths for your liking.                              |
# +----------------------------------------------------------------------------+

import os, bpy, struct
from bpy.types import (Panel, Operator)

os.system('cls')

POLYGONS        = 0x40
POLYGONS_OFFSET = 0x44

triangles = [0]
tempTriangles = [0]

trianglesOffset = [0]
tempTrianglesOffset = [0]

byteSeeker = [0]
colorSeeker = [0]
trianglesBytes = [0]

trianglesObjects = []

old_model_path = "C:\\Users\\SomePerson\\custom_model.lm2"
new_model_path = "C:\\Users\\SomePerson\\custom_model_colors_only.lm2"

# Some colors don't appear correctly, but they get saved correctly.
# We might change the colors in the viewport later.
colorsRed = [0.25, 0, 0]
colorsGreen = [0, 0.25, 0]
colorsBlue = [0, 0, 0.25]
colorsYellow = [0.25, 0.25, 0]
colorsOrange = [0.25, 1, 0]
colorsTan = [0.25, 1, 1]
colorsGray = [1, 1, 1]
colorsBrown = [1, 0, 0]

class colorExport(Operator):
    bl_idname = 'color.export'
    bl_label = 'Color Export'
    
    def execute(self, context):
        
        byteSeeker[0] = 0
        colorSeeker[0] = 0
        
        trianglesBytes.clear()
        trianglesObjects.clear()
        
        outfile = open(old_model_path, 'rb')
        outfile_new = open(new_model_path, 'wb')
        
        # Get triangles amount.
        outfile.seek(POLYGONS, 0)
        
        tempTriangles[0] = struct.unpack('h', outfile.read(2))
        triangles[0] = tempTriangles[0][0]
        
        # Get triangles offset amount.
        outfile.seek(POLYGONS_OFFSET, 0)
        
        tempTrianglesOffset[0] = struct.unpack('h', outfile.read(2))
        trianglesOffset[0] = tempTrianglesOffset[0][0]
        
        print(hex(triangles[0]))
        print(hex(trianglesOffset[0]))
        
        # Go to triangles offset amount.
        outfile.seek(trianglesOffset[0], 0)
        
        for i in range(0, triangles[0]):
            trianglesObjects.append(bpy.data.objects["t%03d" % i])
        
        #print(trianglesObjects)
        
        # Get the original triangle data.
        for i in range(0, (triangles[0] * 0x14)):
            
            outfile.seek(trianglesOffset[0] + byteSeeker[0], 0)
            
            trianglesBytes.append(0)
            trianglesBytes[i] = struct.unpack('B', outfile.read(1))
            outfile_new.write(struct.pack('B', trianglesBytes[i][0]))
            
            byteSeeker[0] = (byteSeeker[0] + 1)
        
        outfile_new.seek(0, 0)
        
        # Set the new triangle data.
        for i in range(0, triangles[0]):
            # Set the color seeker to 16 bytes forward.
            colorSeeker[0] = (colorSeeker[0] + 16)
            
            # Seek to the triangle offset and color seeker amount.
            outfile_new.seek(colorSeeker[0], 0)
            
            # Red
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsRed[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsRed[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsRed[2]):
                outfile_new.write(struct.pack('B', 0x40))
            # Green
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsGreen[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsGreen[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsGreen[2]):
                outfile_new.write(struct.pack('B', 0x80))
            # Blue
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsBlue[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsBlue[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsBlue[2]):
                outfile_new.write(struct.pack('B', 0xC0))
            # Yellow
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsYellow[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsYellow[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsYellow[2]):
                outfile_new.write(struct.pack('B', 0x60))
            # Orange
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsOrange[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsOrange[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsOrange[2]):
                outfile_new.write(struct.pack('B', 0x50))
            # Tan
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsTan[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsTan[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsTan[2]):
                outfile_new.write(struct.pack('B', 0x20))
            # Gray
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsGray[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsGray[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsGray[2]):
                outfile_new.write(struct.pack('B', 0x30))
            # Brown
            if (trianglesObjects[i].data.materials[0].diffuse_color[0] == colorsBrown[0] and
                trianglesObjects[i].data.materials[0].diffuse_color[1] == colorsBrown[1] and
                trianglesObjects[i].data.materials[0].diffuse_color[2] == colorsBrown[2]):
                outfile_new.write(struct.pack('B', 0x10))
            
            # Set the color seeker to 4 bytes forward.
            colorSeeker[0] = (colorSeeker[0] + 4)
        
        outfile.close()
        outfile_new.close()
        
        #outfile = open(old_model_path, 'wb')
        
        #outfile.seek(trianglesOffset[0], 0)
        #for i in range(0, (triangles[0] * 0x14)):
        #    outfile.write(struct.pack('B', trianglesBytes[i][0]))
        
        #outfile.close()
        
        self.report({'INFO'}, "Colors exported to " + new_model_path + "!")
        return {'FINISHED'}

class colorRed(Operator):
    bl_idname = 'color.red'
    bl_label = 'Color Red'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsRed[0]
            material.diffuse_color[1] = colorsRed[1]
            material.diffuse_color[2] = colorsRed[2]
        
        return {'FINISHED'}

class colorGreen(Operator):
    bl_idname = 'color.green'
    bl_label = 'Color Green'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsGreen[0]
            material.diffuse_color[1] = colorsGreen[1]
            material.diffuse_color[2] = colorsGreen[2]
        return {'FINISHED'}

class colorBlue(Operator):
    bl_idname = 'color.blue'
    bl_label = 'Color Blue'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsBlue[0]
            material.diffuse_color[1] = colorsBlue[1]
            material.diffuse_color[2] = colorsBlue[2]
        return {'FINISHED'}

class colorYellow(Operator):
    bl_idname = 'color.yellow'
    bl_label = 'Color Yellow'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsYellow[0]
            material.diffuse_color[1] = colorsYellow[1]
            material.diffuse_color[2] = colorsYellow[2]
        return {'FINISHED'}

class colorOrange(Operator):
    bl_idname = 'color.orange'
    bl_label = 'Color Orange'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsOrange[0]
            material.diffuse_color[1] = colorsOrange[1]
            material.diffuse_color[2] = colorsOrange[2]
        return {'FINISHED'}

class colorTan(Operator):
    bl_idname = 'color.tan'
    bl_label = 'Color Tan'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsTan[0]
            material.diffuse_color[1] = colorsTan[1]
            material.diffuse_color[2] = colorsTan[2]
        return {'FINISHED'}

class colorGray(Operator):
    bl_idname = 'color.gray'
    bl_label = 'Color Gray'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsGray[0]
            material.diffuse_color[1] = colorsGray[1]
            material.diffuse_color[2] = colorsGray[2]
        return {'FINISHED'}

class colorBrown(Operator):
    bl_idname = 'color.brown'
    bl_label = 'Color Brown'
    
    def execute(self, context):
        
        for i in range(0, len(bpy.context.selected_objects)):
            object = bpy.context.selected_objects[i]
            
            material = bpy.data.materials.get(object.name)
            if (material is None):
                material = bpy.data.materials.new(name=str(object.name))
            
            if (object.data.materials):
                object.data.materials[0] = material
            else:
                object.data.materials.append(material)
            
            material.diffuse_color[0] = colorsBrown[0]
            material.diffuse_color[1] = colorsBrown[1]
            material.diffuse_color[2] = colorsBrown[2]
        return {'FINISHED'}

class LBA2Colors(Panel):
    bl_label = "LBA2 Colors"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    
    def draw(self, context):
        layout = self.layout
        
        label_path = layout.row()
        label_path.label(text=str(new_model_path))
        
        button_color_export = layout.row()
        button_color_export.operator('color.export', text='Color Export')
        
        button_color_red = layout.row()
        button_color_red.operator('color.red', text='Color Red')
        
        button_color_green = layout.row()
        button_color_green.operator('color.green', text='Color Green')
        
        button_color_blue = layout.row()
        button_color_blue.operator('color.blue', text='Color Blue')
        
        button_color_yellow = layout.row()
        button_color_yellow.operator('color.yellow', text='Color Yellow')
        
        button_color_orange = layout.row()
        button_color_orange.operator('color.orange', text='Color Orange')
        
        button_color_tan = layout.row()
        button_color_tan.operator('color.tan', text='Color Tan')
        
        button_color_gray = layout.row()
        button_color_gray.operator('color.gray', text='Color Gray')
        
        button_color_brown = layout.row()
        button_color_brown.operator('color.brown', text='Color Brown')

def register():
    bpy.utils.register_class(LBA2Colors)
    
    bpy.utils.register_class(colorExport)
    bpy.utils.register_class(colorRed)
    bpy.utils.register_class(colorGreen)
    bpy.utils.register_class(colorBlue)
    bpy.utils.register_class(colorYellow)
    bpy.utils.register_class(colorOrange)
    bpy.utils.register_class(colorTan)
    bpy.utils.register_class(colorGray)
    bpy.utils.register_class(colorBrown)

def unregister():
    bpy.utils.unregister_class(LBA2Colors)
    
    bpy.utils.unregister_class(colorExport)
    bpy.utils.unregister_class(colorRed)
    bpy.utils.unregister_class(colorGreen)
    bpy.utils.unregister_class(colorBlue)
    bpy.utils.unregister_class(colorYellow)
    bpy.utils.unregister_class(colorOrange)
    bpy.utils.unregister_class(colorTan)
    bpy.utils.unregister_class(colorGray)
    bpy.utils.unregister_class(colorBrown)

if __name__ == "__main__":
    register()