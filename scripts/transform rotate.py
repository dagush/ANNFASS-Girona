xform = hou.node("obj/COMMERCIALhouse_mesh0798/xform1")
SOPxform = xform.geometry()

z = 9999
ry = 0

for i in range(361):
    xform.parm('ry').set(i)
    bbox = SOPxform.boundingBox()
    vec = bbox.sizevec()
    if vec[2] < z:
        z = vec[2]
        ry = i
   
xform.parm('ry').set(ry)