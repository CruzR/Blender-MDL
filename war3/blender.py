"""Module that handles getting models into Blender."""

import bpy

__all__ = ["BlenderImporter", "save"]


class BlenderImporter:
    def __init__(self, model):
        self.model = model

    def save(self):
        self.save_geosets()

    def save_geosets(self):
        for i, _ in enumerate(self.model.geosets):
            self.save_geoset(i)

    def save_geoset(self, i):
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


def save(m):
    """Passes model `m` to Blender."""
    BlenderImporter(m).save()
