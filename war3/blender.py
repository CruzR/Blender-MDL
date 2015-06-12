"""Module that handles getting models into Blender."""

import bpy
import bmesh

__all__ = ["BlenderImporter", "save"]


class BlenderImporter:
    def __init__(self, model):
        self.model = model

    def save(self):
        # TODO: store textures
        # TODO: store materials
        self.save_geosets()
        # TODO: store bones
        # TODO: store lights
        # TODO: store cameras

    def save_geosets(self):
        for i, _ in enumerate(self.model.geosets):
            self.save_geoset(i)

    def save_geoset(self, i):
        # XXX: Perhaps we could use more of bmesh here.
        geoset = self.model.geosets[i]
        mesh = bpy.data.meshes.new("Geoset{}Mesh".format(i))
        obj = bpy.data.objects.new("Geoset{}".format(i), mesh)
        bpy.context.scene.objects.link(obj)

        verts = geoset.vertices
        # TODO: if war3 supports other primitive types
        # than triangles, this might not be sufficient
        faces = [p.indices for p in geoset.faces]
        mesh.from_pydata(verts, [], faces)
        mesh.update(calc_edges=True)

        # Add normals
        mesh.use_auto_smooth = True
        mesh.normals_split_custom_set_from_vertices(geoset.normals)
        mesh.update()

        # TODO: store geoset.vertex_groups
        # TODO: store geoset.groups
        # TODO: store geoset.attributes
        # TODO: store geoset.default_animation
        # TODO: store geoset.animations
        # TODO: store geoset.tvertices
        uvmap = geoset.tvertices[0]
        uvmap = [(uvmap[f[0]], uvmap[f[1]], uvmap[f[2]]) for f in faces]

        bpy.context.scene.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(mesh)
        uv_layer = bm.loops.layers.uv.verify()
        bm.faces.layers.tex.verify()

        for f, uvs in zip(bm.faces, uvmap):
            for l, uv in zip(f.loops, uvs):
                l[uv_layer].uv = uv

        bmesh.update_edit_mesh(mesh)
        bpy.ops.object.mode_set(mode='OBJECT')


def save(m):
    """Passes model `m` to Blender."""
    BlenderImporter(m).save()
