What does currently work:
-------------------------
* Checking the version number, canceling if not 800
* Loading the vertices, normals and texture coords of each geoset


What doesn't work yet:
----------------------
* Integration with Blender
* Everything else


Dependencies:
-------------
You need to have Python 3.x installed.


Instructions:
-------------
In a future release, this will be a Blender plugin.
Currently, it isn't connected to Blender yet;
you have to run it from Python manually.

1. Start the Python shell from this directory
2. Run:

>>>	import importMDL
>>>	importMDL.run()

3. The program will ask you to enter the path to the MDL file.
   The path can either be absolute or relative.

4. The program will read the file and, if nothing goes wrong, print some debug
   information and the vertices, normals and texture coords ('tvertices') of
   each geoset to the console. (That's all it currently does.)
