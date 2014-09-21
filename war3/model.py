"""This module contains the Model data structure."""


from collections.abc import MutableSequence

__all__ = [
    "Model", "ModelInfo", "Animation", "Material", "Layer", "Texture",
    "TVertexAnim", "Geoset"
]


class Model:
    """A data structure that can hold war3 3D models.

    All importers and exporters use this class to represent their data.
    Importers only ever convert external data to objects of this class.
    Exporters only ever convert objects of this class to external data.

    .. attribute:: version
       Version of the model format. An integer.

    .. attribute:: model
       General information about the model, a :class:`ModelInfo` object.

    .. attribute:: sequences
       Collection of :class:`Animation` objects.

    .. attribute:: global_sequences
       Collection of durations (ints).

    .. attribute:: materials
       Collection of Material objects.

    .. attribute:: textures
       Collection of Texture objects.

    .. attribute:: texture_anims
       Collection of TVertexAnim objects.

    .. attribute:: geosets
       List of :class:`Geoset` objects.

    """
    def __init__(self):
        self.version = None
        self.model = None
        self.sequences = []
        self.global_sequences = []
        self.materials = []
        self.textures = []
        self.texture_anims = []
        self.geosets = []


class ModelInfo:
    """General information about the model.

    This class exposes the following member variables:

    .. attribute:: name
       Name of the model (str), max. 0x50 bytes.

    .. attribute:: bounds_radius
       ??? (float)

    .. attribute:: minimum_extent
       ??? (triple of floats)

    .. attribute:: maximum_extent
       ??? (triple of floats)

    .. attribute:: blend_time
       ??? (int)

    """
    def __init__(self, name, bounds_radius, min_extent, max_extent, blend_time):
        self.name = name
        self.bounds_radius = bounds_radius
        self.minimum_extent = min_extent
        self.maximum_extent = max_extent
        self.blend_time = blend_time

    def __repr__(self):
        return "ModelInfo(%r, %r, %r, %r, %r)" % (
            self.name, self.bounds_radius, self.minimum_extent,
            self.maximum_extent, self.blend_time
        )


class Animation:
    """Metadata about an animation.

    Exposed member variables:

    .. attribute:: name
       Name of the animation (str).

    .. attribute:: interval
       Time interval during which the animation plays (pair of ints).

    .. attribute:: move_speed
       ??? (float)

    .. attribute:: non_looping
       Whether the animation should be played only once (bool).

    .. attribute:: rarity
       ??? (float)

    .. attribute:: bounds_radius
       ??? (float)

    .. attribute:: minimum_extent
       ??? (triple of floats)

    .. attribute:: maximum_extent
       ??? (triple of floats)

    """
    def __init__(self, name, ival, speed, noloop, rare, bounds, minext, maxext):
        self.name = name
        self.interval = ival
        self.move_speed = speed
        self.non_looping = noloop
        self.rarity = rare
        self.bounds_radius = bounds
        self.minimum_extent = minext
        self.maximum_extent = maxext

    def __repr__(self):
        return "Animation(%r, %r, %r, %r, %r, %r, %r, %r)" % (
            self.name, self.interval, self.move_speed, self.non_looping,
            self.rarity, self.bounds_radius, self.minimum_extent,
            self.maximum_extent
        )


class Material:
    """Material data.

    Exposed member variables:

    .. attribute:: priority_plane
       ??? (int)

    .. attribute:: constant_color
       ??? (bool)

    .. attribute:: sort_prims_far_z
       ??? (bool)

    .. attribute:: full_resolution
       ??? (bool)

    .. attribute:: layers
       A list of :class:`Layer`s.

    """
    def __init__(self, prio, const_color, sort_prims, full_res, lays=[]):
        self.priority_plane = prio
        self.constant_color = const_color
        self.sort_prims_far_z = sort_prims
        self.full_resolution = full_res
        self.layers = lays

    def __repr__(self):
        return "Material(%r, %r, %r, %r, %r)" % (
            self.priority_plane, self.constant_color,
            self.sort_prims_far_z, self.full_resolution, self.layers
        )


class Layer:
    """Class representing a single layer of a material.

    Exposed member variables:

    .. attribute:: filter_mode
       How to combine with other layers (one of the FM_ constants).

    .. attribute:: unshaded
       ??? (bool)

    .. attribute:: sphere_env_map
       ??? (bool)

    .. attribute:: twosided
       Render the layer from both sides (bool).

    .. attribute:: unfogged
       ??? (bool)

    .. attribute:: no_depth_test
       ??? (bool)

    .. attribute:: no_depth_set
       ??? (bool)

    .. attribute:: texture_id
       Texture ID of the layer (int).

    .. attribute:: tvertex_anim_id
       ??? (int)

    .. attribute:: coord_id
       ??? (int)

    .. attribute:: alpha
       Opacity of the layer (float, 0 == transparent, 1 == opaque).

    """
    FM_None = 0
    FM_Transparent = 1
    FM_Blend = 2
    FM_Additive = 3
    FM_AddAlpha = 4
    FM_Modulate = 5

    def __init__(self, fmode, noshade, senvmap, twosided, nofog,
                 nodtest, nodset, tid, tvaid, cid, alpha):
        self.filter_mode = fmode
        self.unshaded = noshade
        self.sphere_env_map = senvmap
        self.twosided = twosided
        self.unfogged = nofog
        self.no_depth_test = nodtest
        self.no_depth_set = nodset
        self.texture_id = tid
        self.tvertex_anim_id = tvaid
        self.coord_id = cid
        self.alpha = alpha

    def __repr__(self):
        return "Layer(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r)" % (
            self.filter_mode, self.unshaded, self.sphere_env_map,
            self.twosided, self.unfogged, self.no_depth_test,
            self.no_depth_set, self.texture_id, self.tvertex_anim_id,
            self.coord_id, self.alpha
        )


class Texture:
    """Class representing a single Texture.

    Exposed member variables:

    .. attribute:: replaceable_id
       ??? (int)

    .. attribute:: texture_path
       Path of the .blp file (str), max. 0x100 bytes.

    .. attribute:: wrap_width
       Whether to wrap the texture around horizontally (bool).

    .. attribute:: wrap_height
       Whether to wrap the texture around vertically (bool).

    """
    def __init__(self, replace_id, path, wrap_width, wrap_height):
        self.replaceable_id = replace_id
        self.texture_path = path
        self.wrap_width = wrap_width
        self.wrap_height = wrap_height

    def __repr__(self):
        return "Texture(%r, %r, %r, %r)" % (
            self.replaceable_id, self.texture_path,
            self.wrap_width, self.wrap_height
        )


class TVertexAnim:
    """A class representing the animaton of texture vertices.

    Exposed member variables:

    .. attribute:: translation
       Translation of the texture vertices (float triple).

    .. attribute:: rotation
       Rotation of the texture vertices (float quadruple).

    .. attribute:: scaling
       Scaling of the texture vertices (float triple).

    """
    def __init__(self, trans, rot, scale):
        self.translation = trans
        self.rotation = rot
        self.scaling = scale

    def __repr__(self):
        return "TVertexAnim(%r, %r, %r)" % (
            self.translation,
            self.rotation,
            self.scaling
        )


class Geoset:
    """A sub-object of a model.

    .. attribute:: vertices
       A list of vertices (3d vectors).

    .. attribute:: normals
       A list of normals (3d vectors).

    .. attribute:: faces
        A list of indices into the vertices list.

    .. attribute:: tvertices
       A list of texture vertices (2d vectors).

    """
    def __init__(self, verts, normals, faces, tverts):
        self.vertices = verts
        self.normals = normals
        self.faces = faces
        self.tvertices = tverts

    def __repr__(self):
        return "Geoset(%r, %r, %r, %r)" % (
            self.vertices,
            self.normals,
            self.faces,
            self.tvertices
        )


# vim: set ts=4 sw=4 et:
