"""This module contains the Model data structure."""


from collections.abc import MutableSequence

__all__ = [
    "Model", "ModelInfo", "Sequences", "Animation", "GlobalSequences",
    "Materials", "Material", "Layer", "Textures", "Texture"
]


class Model:
    """A data structure that can hold war3 3D models.

    All importers and exporters use this class to represent their data.
    Importers only ever convert external data to objects of this class.
    Exporters only ever convert objects of this class to external data.

    Note that in order to make debugging easier, and to make sure the
    import/export modules don't have to worry about data integrity,
    this class checks all property assignments and raises an exception
    if an argument is invalid. Please note that while you are able to
    assign to members of members of this class, doing so is severely
    discouraged.

    """
    def __init__(self):
        self._seqs = Sequences()
        self._glbs = GlobalSequences()
        self._mtls = Materials()
        self._texs = Textures()

    @property
    def version(self):
        """Version of the model format. An integer."""
        return self._version

    @version.setter
    def version(self, v):
        _assert_int(v)
        self._version = v

    @property
    def model(self):
        """General information about the model, a ModelInfo object."""
        return self._model

    @model.setter
    def model(self, v):
        if isinstance(v, ModelInfo):
            self._model = v
        else:
            self._model = ModelInfo(*v)

    @property
    def sequences(self):
        """Collection of Animation objects."""
        return self._seqs

    @sequences.setter
    def sequences(self, v):
        if isinstance(v, Sequences):
            self._seqs = v
        else:
            raise TypeError("must be a Sequences object")

    @property
    def global_sequences(self):
        """Collection of durations (ints)."""
        return self._glbs

    @global_sequences.setter
    def global_sequences(self, v):
        if isinstance(v, GlobalSequences):
            self._glbs = v
        else:
            raise TypeError("must be a GlobalSequences object")

    @property
    def materials(self):
        """Collection of Material objects."""
        return self._mtls

    @materials.setter
    def materials(self, v):
        if isinstance(v, Materials):
            self._mtls = v
        else:
            raise TypeError("must be a Materials object")

    @property
    def textures(self):
        """Collection of Texture objects."""
        return self._texs

    @textures.setter
    def textures(self, v):
        if isinstance(v, Textures):
            self._texs = v
        else:
            raise TypeError("must be a Textures object")


class ModelInfo:
    """General information about the model.

    This class exposes the following member variables:

    name: Name of the model (str)
    bounds_radius: ??? (float)
    minimum_extent: ??? (triple of floats)
    maximum_extent: ??? (triple of floats)
    blend_time: ??? (int)

    """
    def __init__(self, name, bounds_radius, min_extent, max_extent, blend_time):
        _assert_ascii_len(name, 0x150)
        _assert_float(bounds_radius)
        _assert_float_triple(min_extent)
        _assert_float_triple(max_extent)
        _assert_int(blend_time)

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


# helper class
class _TypedList(MutableSequence):
    def __init__(self, t, li=None):
        self._type = t
        if li is None:
            self._li = []
        elif all(map(lambda x: isinstance(x, t), li)):
            self._li = li
        else:
            raise TypeError("type must be %s" % t.__name__)

    def __getitem__(self, key):
        return self._li[key]

    def __setitem__(self, key, value):
        if isinstance(value, self._type):
            self._li[key] = value
        else:
            self._li[key] = self._type(*value)

    def __delitem__(self, key):
        del self._li[key]

    def __len__(self):
        return len(self._li)

    def insert(self, key, value):
        if isinstance(value, self._type):
            self._li.insert(key, value)
        else:
            self._li.insert(key, self._type(*value))

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self._li)


class Sequences(_TypedList):
    """A sequence container that accepts only Animation instances."""
    def __init__(self, li=None):
        _TypedList.__init__(self, Animation, li)


class Animation:
    """Metadata about an animation.

    Exposed member variables:

    name: Name of the animation (str)
    interval: Time interval during which the animation plays (pair of ints)
    move_speed: ??? (float)
    non_looping: Whether the animation should be played only once (bool)
    rarity: ??? (float)
    bounds_radius: ??? (float)
    minimum_extent: ??? (triple of floats)
    maximum_extent: ??? (triple of floats)

    """
    def __init__(self, name, ival, speed, noloop, rare, bounds, minext, maxext):
        _assert_ascii_len(name, 0x50)
        _assert_int_pair(ival)
        _assert_float(speed)
        _assert_bool(noloop)
        _assert_float(rare)
        _assert_float(bounds)
        _assert_float_triple(minext)
        _assert_float_triple(maxext)

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


class GlobalSequences(_TypedList):
    """A sequence container that accepts only durations (ints)."""
    def __init__(self, li=None):
        _TypedList.__init__(self, int, li)


class Materials(_TypedList):
    """A sequence container that accepts only materials."""
    def __init__(self, li=None):
        _TypedList.__init__(self, Material, li)


class Material(_TypedList):
    """A list of Layers.

    Exposed member variables:

    priority_plane: ??? (int)
    constant_color: ??? (bool)
    sort_prims_far_z: ??? (bool)
    full_resolution: ??? (bool)

    """
    def __init__(self, prio, const_color, sort_prims, full_res, lays=None):
        _TypedList.__init__(self, Layer, lays)

        _assert_int(prio)
        _assert_bool(const_color)
        _assert_bool(sort_prims)
        _assert_bool(full_res)

        self.priority_plane = prio
        self.constant_color = const_color
        self.sort_prims_far_z = sort_prims
        self.full_resolution = full_res

    def __repr__(self):
        return "Material(%r, %r, %r, %r, %r)" % (
            self.priority_plane, self.constant_color,
            self.sort_prims_far_z, self.full_resolution, self._li
        )


class Layer:
    """Class representing a single layer of a material.

    Exposed member variables:

    filter_mode: How to combine with other layers (one of the FM_ constants)
    unshaded: ??? (bool)
    sphere_env_map: ??? (bool)
    twosided: Render the layer from both sides (bool)
    unfogged: ??? (bool)
    no_depth_test: ??? (bool)
    no_depth_set: ??? (bool)
    texture_id: Texture ID of the layer (int)
    tvertex_anim_id: ??? (int)
    coord_id: ??? (int)
    alpha: Opacity of the layer (float, 0 == transparent, 1 == opaque)

    """
    FM_None = 0
    FM_Transparent = 1
    FM_Blend = 2
    FM_Additive = 3
    FM_AddAlpha = 4
    FM_Modulate = 5

    def __init__(self, fmode, noshade, senvmap, twosided, nofog,
                 nodtest, nodset, tid, tvaid, cid, alpha):
        _assert_int_range(fmode, Layer.FM_None, Layer.FM_Modulate)
        _assert_bool(noshade)
        _assert_bool(senvmap)
        _assert_bool(twosided)
        _assert_bool(nofog)
        _assert_bool(nodtest)
        _assert_bool(nodset)
        _assert_int(tid)
        _assert_int(tvaid)
        _assert_int(cid)
        _assert_float_range(alpha, 0.0, 1.0)

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


class Textures(_TypedList):
    """A list that accepts only textures."""
    def __init__(self, li=None):
        _TypedList.__init__(self, Texture, li)


class Texture:
    """Class representing a single Texture.

    Exposed member variables:

    replaceable_id: ??? (int)
    texture_path: Path of the .blp file (str)
    wrap_width: Whether to wrap the texture around horizontally (bool)
    wrap_height: Whether to wrap the texture around vertically (bool)

    """
    def __init__(self, replace_id, path, wrap_width, wrap_height):
        _assert_int(replace_id)
        _assert_ascii_len(path, 0x100)
        _assert_bool(wrap_width)
        _assert_bool(wrap_height)

        self.replaceable_id = replace_id
        self.texture_path = path
        self.wrap_width = wrap_width
        self.wrap_height = wrap_height

    def __repr__(self):
        return "Texture(%r, %r, %r, %r)" % (
            self.replaceable_id, self.texture_path,
            self.wrap_width, self.wrap_height
        )


# helper functions
def _assert_ascii_len(x, n):
    if not isinstance(x, str):
        raise TypeError("must be a str")
    if len(x.encode('ascii')) > n:
        raise ValueError("must be <= %d bytes" % n)

def _assert_bool(x):
    if not isinstance(x, bool):
        raise TypeError("must be a bool")

def _assert_int(x):
    if not isinstance(x, int):
        raise TypeError("must be an int")

def _assert_int_range(x, l, u):
    _assert_int(x)
    if not l <= x <= u:
        raise ValueError("not %d <= %d <= %d" % (l, x, u))

def _assert_int_pair(x):
    if not isinstance(x, tuple) or not len(x) == 2 or \
            not all(map(lambda z: isinstance(z, int), x)):
        raise TypeError("must be an int pair")

def _assert_float(x):
    if not isinstance(x, float):
        raise TypeError("must be a float")

def _assert_float_range(x, l, u):
    _assert_float(x)
    if not l <= x <= u:
        raise ValueError("not %d <= %d <= %d" % (l, x, u))

def _assert_float_triple(x):
    if not isinstance(x, tuple) or not len(x) == 3 or \
            not all(map(lambda z: isinstance(z, float), x)):
        raise TypeError("must be a float triple")

# vim: set ts=4 sw=4 et:
