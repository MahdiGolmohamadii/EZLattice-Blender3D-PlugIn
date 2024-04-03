bl_info = {
    "name": "Lattice Tools",
    "author": "MahdiGLMD",
    "version": (0, 1),
    "blender": (3, 1, 0),
    "location": "View3D > Tools > Lattice Tools",
    "description": "Many lattice tools",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}




import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       PropertyGroup,
                       Operator,
                       AddonPreferences,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
        
    add_modifier : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    Lattice_U : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 2,
        min = 0,
        max = 1000
        )
    Lattice_V : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 2,
        min = 0,
        max = 1000
        )
    Lattice_W : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 2,
        min = 0,
        max = 1000
        )

    padding : FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 0,
        min = 0.01,
        max = 30.0
        )
        
        

class Make_Lattice_Bounding(bpy.types.Operator):
    bl_idname = "example.func_2"
    bl_label = "Generate the lattice"
    bl_options = {'REGISTER' , 'UNDO'}
    

    def execute(self, context):
        # Implement your second function here
        self.report({'INFO'}, f"This is {self.bl_idname}")
        ####variables

        padding = context.scene.my_tool.padding

        add_lattice_modifier = context.scene.my_tool.add_modifier
        U_count = context.scene.my_tool.Lattice_U
        V_count = context.scene.my_tool.Lattice_V
        W_count = context.scene.my_tool.Lattice_W

        all_selected = False



        #TODO#######################################Add multiple select option
        # Select the active object
        original_obj = bpy.context.active_object
        # Grab the active vertices form our object
        active_object_verts = original_obj.data.vertices

        # Store the vertices x, y, and z values
        xValues = []
        yValues = []
        zValues = []


        #TODO####################################### Add the possibility to add the lattice to selected vertices only
        # Only compute bounding box based on
        # the vertices if they are selected
        for v in active_object_verts:  
            if v.select == True: 
                xValues.append(v.co[0])   
                yValues.append(v.co[1])  
                zValues.append(v.co[2]) 
            

        #find bounds of the object
        minx =  min(xValues)
        maxx =  max(xValues)
        miny =  min(yValues)
        maxy =  max(yValues)
        minz =  min(zValues)
        maxz =  max(zValues)
        
        #make lattice
        #lattice name
        lt_name = "lattice_" + original_obj.name
        #make th lattice data
        lt_data = bpy.data.lattices.new("LATTICE")
        #creat the lattice
        lt_obj = bpy.data.objects.new(lt_name, lt_data)
        #set lattice dimensions with bounding dimentions
        lt_obj.dimensions = [abs(minx)+abs(maxx) + padding, abs(miny)+abs(maxy)+ padding, abs(minz)+abs(maxz)+ padding]
        #set location and rotation with the original obj
        lt_obj.location = original_obj.location
        lt_obj.rotation_euler = original_obj.rotation_euler
        #add the modifier if the checkbox is checked
        if add_lattice_modifier:
            mod = original_obj.modifiers.new("Lattice", 'LATTICE')
            mod.object = lt_obj
        #link the lattice
        bpy.context.view_layer.active_layer_collection.collection.objects.link(lt_obj)

        #set the u, v, w parameters
        lt_obj.data.points_u = U_count
        lt_obj.data.points_v = V_count
        lt_obj.data.points_w = W_count

        # Unselect every object
        for obj in bpy.data.objects:
            bpy.data.objects[obj.name].select_set(False)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "LatticeTools"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        
        layout.prop(mytool, "Lattice_U", text="u")
        layout.prop(mytool, "Lattice_V", text="v")
        layout.prop(mytool, "Lattice_W", text="w")
        layout.prop(mytool, "padding", text="padding")
        layout.prop(mytool, "add_modifier", text="Add modifier")
        layout.operator(Make_Lattice_Bounding.bl_idname)

        layout.separator()
        
        




# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    Make_Lattice_Bounding,
    OBJECT_PT_CustomPanel
    
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()