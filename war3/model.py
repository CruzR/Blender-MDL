"""This module contains the Model data structure."""


from collections.abc import MutableSequence

__all__ = ["Model", "ModelInfo", "Sequences", "Animation"]


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

def _assert_int_pair(x):
    if not isinstance(x, tuple) or not len(x) == 2 or \
            not all(map(lambda z: isinstance(z, int), x)):
        raise TypeError("must be an int pair")

def _assert_float(x):
    if not isinstance(x, float):
        raise TypeError("must be a float")

def _assert_float_triple(x):
    if not isinstance(x, tuple) or not len(x) == 3 or \
            not all(map(lambda z: isinstance(z, float), x)):
        raise TypeError("must be a float triple")

# vim: set ts=4 sw=4 et:
