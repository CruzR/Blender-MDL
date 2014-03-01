"""This module contains the Model data structure."""


__all__ = ["Model", "ModelInfo"]


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


# helper functions
def _assert_ascii_len(x, n):
    if not isinstance(x, str):
        raise TypeError("must be a str")
    if len(x.encode('ascii')) > n:
        raise ValueError("must be <= %d bytes" % n)

def _assert_int(x):
    if not isinstance(x, int):
        raise TypeError("must be an int")

def _assert_float(x):
    if not isinstance(x, float):
        raise TypeError("must be a float")

def _assert_float_triple(x):
    if not isinstance(x, tuple) or not len(x) == 3 or \
            not all(map(lambda z: isinstance(z, float), x)):
        raise TypeError("must be a float triple")


# vim: set ts=4 sw=4 et:
