# ANNFASS-Girona
Code developed for the ANNFASS (An Artificial Neural Network Framework for understanding historical monuments Architectural Structure and Style) project:

http://annfass.cs.ucy.ac.cy/

https://annfass-srv.cs.ucy.ac.cy/home

(Code by Ruben Martinez, reviewed by Gustavo Patow)

To execute the code it is necessary to load a file with a "file" node, and then provide the path to the node in the form

path = "obj/RELIGIOUSchurch_mesh1365"

We do it through Houdini's tools, i.e., its shells, and provide a sample code at the file:
shelf find_walls.py

At this moment, execution is a bit "manual", and it requires to link the file node to a Transform node:

Node File -> Transform

Then we must execute two scripts, Transform Rotate, which rotates the building in small steps until it finds a position such that the depth (i.e., z) distance of the bounding box is minimal, and CleanBuilding, that removes ("cleans") the building from all the primitives of elements that do not interest us. Thus, the structure should be:

File -> Transform -> Delete

To what we add a Fuse node to simplify the geometry by eliminating repeated (or extremely close) vertices:

File -> Transform -> Delete -> Fuse -> Transform

This last transform is just a security one, that makes the building larger to prevent numerical errors in the following stages (subdiv)

Finally, we should also have the following structure:

Box -> Group -> Comp

We use the MatchSize script to do it, as it is easier to do it with a Box node to keep the building proportions, rather than using an extrusion. Finally, we apply the FindWalls script where we provide the last Transform, the Comp and the Object nodes.

This code runs on top of Houdini 17.5.258, it was not tested on other versions, but it should run without problems as well. Also, it needs to have the buildingEngine digital asset library (OTL) installed, which can be downloaded from here:

https://drive.google.com/file/d/1mguXpvz4plqHRtSOjrky-md5UUSAzHHC/view?usp=sharing

Older versions, with full documentation, are available at the old project page:
http://ggg.udg.edu/skylineEngine/modules/buildingEngine/
Unfortunately, buildingEngine is not maintained anymore, so the nodes work thanks to Houdini's backwards compatibility.

Copyright ANNFASS project.