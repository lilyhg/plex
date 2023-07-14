import bpy
import os
import subprocess
import sys
import mathutils
from math import radians
from mathutils import Vector

def install_addon(addon_path):
    bpy.ops.preferences.addon_install(filepath=addon_path)
    addon_name = os.path.splitext(os.path.basename(addon_path))[0]
    bpy.ops.preferences.addon_enable(module=addon_name)

def install_biotite():
    blender_python_exe = os.path.join(sys.prefix, 'bin', 'python3.10')
    cmd = [blender_python_exe, "-m", "pip", "install", "biotite"]
    subprocess.run(cmd, check=True)

def delete_existing_objects():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def set_import_properties(local_path, local_name, include_bonds, center, del_solvent, default_style):
    bpy.context.scene.mol_import_local_path = local_path
    bpy.context.scene.mol_import_local_name = local_name
    bpy.context.scene.mol_import_include_bonds = include_bonds
    bpy.context.scene.mol_import_center = center
    bpy.context.scene.mol_import_del_solvent = del_solvent
    bpy.context.scene.mol_import_default_style = default_style

def import_protein_local():
    bpy.ops.mol.import_protein_local()

def set_render_engine(engine):
    bpy.context.scene.render.engine = engine

def enable_gpu_rendering():
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'

def create_empty_objects():
    object_evaluated = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bbox_cos_local = [bbox_co[:] for bbox_co in object_evaluated.bound_box[:]]
    bbox_cos_global = [bpy.context.object.matrix_world @ Vector(bbox_co) for bbox_co in bbox_cos_local]
    empty_objects = []

    for co in bbox_cos_global:
        empty = bpy.data.objects.new(name='empty', object_data=None)
        bpy.context.scene.collection.objects.link(object=empty)
        empty.location = co
        empty.empty_display_type = 'CUBE'
        empty.empty_display_size = 0.6
        empty_objects.append(empty)

    lowest_empty = min(empty_objects, key=lambda empty: empty.location.z)
    return lowest_empty, bbox_cos_global

def add_camera(center):
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.location = center + Vector((0, -5, 0))
    camera.rotation_euler = (1.5708, 0, 0)
    bpy.context.scene.camera = camera
    return camera

def set_background_color(color):
    bpy.context.scene.world.use_nodes = True
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = color

def add_plane_below(lowest_empty):
    plane_size = 7.0
    plane_height = 0.1
    plane_location = lowest_empty.location - Vector((0, 0, plane_height / 2))
    bpy.ops.mesh.primitive_plane_add(size=plane_size, enter_editmode=False, location=plane_location)
    plane = bpy.context.active_object
    plane.name = 'plane'
    material = bpy.data.materials.new(name='PlaneMaterial')
    material.diffuse_color = (0.8, 0.8, 0.8, 1)
    plane.data.materials.append(material)

def add_point_light(location, energy):
    light_data = bpy.data.lights.new(name="PointLight", type='POINT')
    light_object = bpy.data.objects.new(name="PointLight", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = location
    light_object.data.energy = energy

def set_render_output(output_path, output_filename):
    render = bpy.context.scene.render
    render.filepath = os.path.join(output_path, output_filename)
    render.image_settings.file_format = 'PNG'

def render_scene():
    bpy.ops.render.render(write_still=True)

def main(input_file_path, output_file_name, output_file_path):
    addon_path = "./MolecularNodes.zip"
    install_addon(addon_path)
    install_biotite()
    delete_existing_objects()

    local_name = 'PROTEIN NAME'
    include_bonds = True
    center = False
    del_solvent = True
    default_style = 1
    set_import_properties(input_file_path, local_name, include_bonds, center, del_solvent, default_style)

    import_protein_local()
    set_render_engine('CYCLES')
    enable_gpu_rendering()

    lowest_empty, bbox_cos_global = create_empty_objects()
    camera = add_camera(sum(bbox_cos_global, Vector()) / 8)
    set_background_color((0, 0, 0, 1))
    add_plane_below(lowest_empty)
    add_point_light((0, 0, 0), 15.0)

    set_render_output(output_file_path, output_file_name)
    render_scene()

    output_filepath = os.path.join(output_file_path, output_file_name)
    print("Rendered image saved to:", output_filepath)


if __name__ == "__main__":
    if "--" not in sys.argv:
        argv = []  # as if no args are passed
    else:
        argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
    input_file_path = argv[0]
    output_file_name = argv[1]
    output_file_path = argv[2]
    main(input_file_path, output_file_name, output_file_path)

