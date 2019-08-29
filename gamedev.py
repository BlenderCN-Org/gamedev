'''
Author: Alexander Khorkov - playrix
'''

bl_info = {
    "name": "Gamedev Utilities",
    "description": "Utilities for game dev",
    "author": "Alexander Khorkov",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "warning": "Beta Release",
    "location": "3D View > Toolbox",
    "category": "Object",
}

import bpy
import bmesh

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        )

#-------------------------------------------------------

class Checker_Deselect(Operator):
    """Checker Deselect"""
    bl_idname = 'mesh.checker_deselect'
    bl_label = 'Checker Deselect'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects !=[]:
            return bpy.context.object.mode == 'EDIT' and bpy.context.object is not None

    def execute(self, context):
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_nth()
        return {"FINISHED"}

class Add_Bevel(Operator):
    """Add Bevel"""
    bl_idname = 'mesh.add_bevel'
    bl_label = 'Add Bevel'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects !=[]:
            return bpy.context.object.mode == 'OBJECT' and bpy.context.object is not None

    def execute(self, context):
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].segments = 3
        return {"FINISHED"}

class Add_Subsurf(Operator):
    """Add Subsurf"""
    bl_idname = 'mesh.add_subsurf'
    bl_label = 'Add Subsurf'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects !=[]:
            return bpy.context.object.mode == 'OBJECT' and bpy.context.object is not None

    def execute(self, context):
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subdivision"].render_levels = 3
        bpy.context.object.modifiers["Subdivision"].levels = 3
        bpy.context.object.modifiers["Subdivision"].show_on_cage = True
        return {"FINISHED"}

class Add_UV_To_Hard_Edges(Operator):
    """UVs to Hard Edges"""
    bl_idname = 'mesh.add_uv_to_hard_edges'
    bl_label = 'UVs to Hard Edges'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects !=[]:
            return bpy.context.object.mode == 'EDIT' and bpy.context.object is not None

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.uv.seams_from_islands()

        obj = bpy.context.active_object
        mesh = obj.data
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(mesh)
        for edge in bm.edges:
            if edge.seam:
                edge.select_set(True)
                break
        bpy.ops.mesh.select_similar(type='SEAM', threshold=0.01)

        bpy.ops.mesh.mark_sharp()
        return {"FINISHED"}

#-------------------------------------------------------
class VIEW3D_PT_checker_deselect(Panel):
    bl_idname = "panel.panel3"
    bl_label = "Gamedev Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Gamedev Utilities"

    def draw(self, context):
        self.layout.operator("mesh.checker_deselect", text="Checker Deselect")
        self.layout.operator("mesh.add_bevel", text="Add Bevel")
        self.layout.operator("mesh.add_subsurf", text="Add Subsurf")
        self.layout.operator("mesh.add_uv_to_hard_edges", text="UVs to Hard Edges")

#-------------------------------------------------------
classes = (
    VIEW3D_PT_checker_deselect,
    Checker_Deselect,
    Add_Bevel,
    Add_Subsurf,
    Add_UV_To_Hard_Edges
)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
