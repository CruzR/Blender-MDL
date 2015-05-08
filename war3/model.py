"""This module contains the Model data structure."""


from enum import Enum
from collections import namedtuple
from functools import reduce


__all__ = [
    "Model", "ModelInfo", "Animation", "Material", "Layer", "Texture",
    "Geoset", "KF", "LineType", "KeyframeAnimation", "Keyframe",
    "PrimitiveType", "Primitives", "GeosetAttributes", "GAnimation",
    "GeosetAnimation", "ColorAnimation", "ObjectFlag", "Bone", "LightType",
    "Light", "Helper", "Attachement"
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
       Collection of :class:`Material` objects.

    .. attribute:: textures
       Collection of :class:`Texture` objects.

    .. attribute:: texture_animations
       Collection of lists of :class:`KeyframeAnimation` objects.

    .. attribute:: geosets
       List of :class:`Geoset` objects.

    .. attribute:: geoset_animations
       List of :class:`GeosetAnimation` objects.

    .. attribute:: bones
       List of :class:`Bone` objects.

    .. attribute:: lights
       List of :class:`Light` objects.

    .. attribute:: helpers
       List of :class:`Helper` objects.

    .. attribute:: attachements
       List of :class:`Attachement` objects.

    """
    def __init__(self):
        self.version = None
        self.model = None
        self.sequences = []
        self.global_sequences = []
        self.materials = []
        self.textures = []
        self.texture_animations = []
        self.geosets = []
        self.geoset_animations = []
        self.bones = []
        self.lights = []
        self.helpers = []
        self.attachements = []


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
    def __init__(self, prio, const_color, sort_prims, full_res, lays=None):
        self.priority_plane = prio
        self.constant_color = const_color
        self.sort_prims_far_z = sort_prims
        self.full_resolution = full_res
        self.layers = [] if lays is None else lays

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

    .. attribute:: animations
       A list of :class:`KeyframeAnimation`s.

    """
    FM_None = 0
    FM_Transparent = 1
    FM_Blend = 2
    FM_Additive = 3
    FM_AddAlpha = 4
    FM_Modulate = 5

    def __init__(self, fmode, noshade, senvmap, twosided, nofog,
                 nodtest, nodset, tid, tvaid, cid, alpha, anims=None):
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
        self.animations = [] if anims is None else anims

    def __repr__(self):
        return "Layer(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r)" % (
            self.filter_mode, self.unshaded, self.sphere_env_map,
            self.twosided, self.unfogged, self.no_depth_test,
            self.no_depth_set, self.texture_id, self.tvertex_anim_id,
            self.coord_id, self.alpha, self.animations
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


class Geoset:
    """A sub-object of a model.

    .. attribute:: vertices
       A list of vertices (3d vectors).

    .. attribute:: normals
       A list of normals (3d vectors).

    .. attribute:: faces
       A list of indices into the vertices list.

    .. attribute:: vertexgroups
       A partition (division into disjoint subsets) of the vertices.

    .. attribute:: groups
       ??? (list of lists of ints)

    .. attribute:: attributes
       Misc. geoset attributes (of type :class:`GeosetAttributes`).

    .. attribute:: default_animation
       The default animation state (a :class:`GAnimation`).

    .. attribute:: animations
       A list of animations (:class:`GAnimation`).

    .. attribute:: tvertices
       A list of lists of texture vertices (2d vectors).

    """
    def __init__(self, verts, normals, faces, vgrps, groups, attrs, danim, anims, tverts):
        self.vertices = verts
        self.normals = normals
        self.faces = faces
        self.vertexgroups = vgrps
        self.groups = groups
        self.attributes = attrs
        self.default_animation = danim
        self.animations = anims
        self.tvertices = tverts

    def __repr__(self):
        return "Geoset(%r, %r, %r, %r, %r, %r, %r, %r, %r)" % (
            self.vertices,
            self.normals,
            self.faces,
            self.vertexgroups,
            self.groups,
            self.attributes,
            self.default_animation,
            self.animations,
            self.tvertices
        )


class KF(Enum):
    MaterialAlpha = 0
    MaterialTexture = 1

    TextureAnimTranslation = 2
    TextureAnimRotation = 3
    TextureAnimScaling = 4

    GeosetAnimAlpha = 5
    GeosetAnimColor = 6

    ObjectTranslation = 7
    ObjectRotation = 8
    ObjectScaling = 9
    ObjectVisibility = 10

    LightVisibility = 11
    LightColor = 12
    LightIntensity = 13
    LightAmbientColor = 14
    LightAmbientIntensity = 15

    AttachementVisibility = 16


class LineType(Enum):
    NoInterpolation = 0
    Linear = 1
    Hermite = 2
    Bezier = 3


class KeyframeAnimation:
    """An animation of some property composed of keyframes.

    .. attribute:: target
       What is being animated; one of the enum values from :class:`KF`.

    .. attribute:: linetype
       How to interpolate between keyframes;
       one of the :class:`LineType` enum values.

    .. attribute global_sequence_id
       An integer defining the global sequence the animation belongs to.

    .. attribute:: keyframes
       A list of :class:`Keyframe` objects.

    """
    def __init__(self, target, linetype, gsid, frames=None):
        self.target = target
        self.linetype = linetype
        self.global_sequence_id = gsid
        self.keyframes = [] if frames is None else frames

    def __repr__(self):
        return "KeyframeAnimation(%s, %s, %r, %r)" % (
            self.target, self.linetype,
            self.global_sequence_id, self.keyframes
        )


class Keyframe:
    """A single keyframe of a keyframe animation.

    .. attribute:: frame
       The frame number, an integer.

    .. attribute:: value
       The value of the animated property at this keyframe.
       Its type depends on the owning animation's target.

    .. attribute:: tangent_in
       Tangent value. None unless the animation's linetype is Hermite
       or Bezier. Has the same type as value.

    .. attribute:: tangent_out
       Analogous to tangent_in.

    """
    def __init__(self, frame, value, tangent_in=None, tangent_out=None):
        self.frame = frame
        self.value = value
        self.tangent_in = tangent_in
        self.tangent_out = tangent_out

    def __repr__(self):
        if self.tangent_in is None and self.tangent_out is None:
            return "Keyframe(%r, %r)" % (self.frame, self.value)
        else:
            return "Keyframe(%r, %r, %r, %r)" % (
                self.frame, self.value, self.tangent_in, self.tangent_out
            )


class PrimitiveType(Enum):
    # TODO: Are these D3D primitives or GL primitives (both represent tris as 4)?
    # TODO: Does war3 accept other primitive types?
    TriangleList = 4


class Primitives:
    """A list of rendering primitives.

    .. attribute:: type_
       A value from the :class:`PrimitiveType` enum.

    .. attribute:: indices
       The indices into the vertex buffer that compromise the primitives.

    """
    def __init__(self, type_, indices):
        self.type_ = type_
        self.indices = indices

    def __repr__(self):
        return "Primitives(%s, %r)" % (self.type_, self.indices)


GeosetAttributes = namedtuple("GeosetAttributes",
                              "material_id selection_group selectable")
GAnimation = namedtuple("GAnimation",
                        "bounds_radius minimum_extent maximum_extent")

GeosetAnimation = namedtuple("GeosetAnimation",
                             "alpha color_animation color geoset_id animations")

class ColorAnimation(Enum):
    NoAnimation = 0
    DropShadow = 1
    Color = 2
    Both = 3

class ObjectType(Enum):
    Helper = 0
    Bone = 256
    Light = 512
    Event = 1024
    Attachement = 2048
    CollisionShape = 8192

class ObjectFlag(Enum):
    DontInheritTranslation = 1
    DontInheritScaling = 2
    DontInheritRotation = 4
    Billboarded = 8
    BillboardedLockX = 16
    BillboardedLockY = 32
    BillboardedLockZ = 64
    CameraAnchored = 128

    @staticmethod
    def set_from_int(i):
        s = {flag for flag in ObjectFlag if flag.value & i}
        return s

    @staticmethod
    def int_from_set(s):
        return reduce(lambda acc, flag: acc | flag.value, s, 0)

Bone = namedtuple("Bone",
                  "name object_id parent flags animations "
                  "geoset_id geoset_anim_id")

class LightType(Enum):
    Omnidirectional = 0
    Directional = 1
    Ambient = 2

Light = namedtuple("Light",
                   "name object_id parent flags animations "
                   "type_ attenuation color intensity "
                   "ambient_color ambient_intensity")

Helper = namedtuple("Helper", "name object_id parent flags animations")

Attachement = namedtuple("Attachement",
                         "name object_id parent flags animations "
                         "path attachement_id")

# vim: set ts=4 sw=4 et:
