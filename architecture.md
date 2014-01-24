Architecture
============

Why rewrite the addon?
----------------------

The old code was pretty crappy, and that's the nicest thing you could say about
it. It tried to parse the MDL file format and failed to properly do so.
Additionally, it was neither nice to maintain nor did it use the full potential
of the Blender Python API.

Overview
--------

The rewritten addon will be centered around the class `War3Model`, which will
be used to hold all internal data of the model being converted. Submodules will
implement import/export methods for various file formats / data representations
and will register them on the main class when imported. This way, each module
will only have to worry about the conversion file format <-> `War3Model` class,
and code can be separated more cleanly. As a bonus, we'll have a free
standalone MDL <-> MDX converter once those modules are both implemented.

<figure>
<pre><code>
                                                       +----------------+
                                                       |                |
                                       +--------------<|    from_mdx    |
                                       |               |                |
                                       |               +----------------+
+----------------+                     |               +----------------+
|                |                     |               |                |
|   to_blender   |<--------------+     |  +----------->|     to_mdx     |
|                |               |     |  |            |                |
+----------------+          +----------------+         +----------------+
                            |                |
                            |   War3Model    |
                            |                |
+----------------+          +----------------+         +----------------+
|                |               |     |  |            |                |
|  from_blender  |>--------------+     |  +-----------<|    from_mdl    |
|                |                     |               |                |
+----------------+                     |               +----------------+
                                       |               +----------------+
                                       |               |                |
                                       +-------------->|     to_mdl     |
                                                       |                |
                                                       +----------------+
</code></pre>
<figcaption>Figure 1. Architectural Overview</figcaption>
</figure>
