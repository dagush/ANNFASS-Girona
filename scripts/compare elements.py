import math

def Hausdorff(a, b):
    ageo = a.geometry()
    bgeo = b.geometry()
    apoints = ageo.points()
    bpoints = bgeo.points()
    min = 99999
    
    for ap in apoints:
        for bp in bpoints:
            dist = distance(ap,bp)
            if dist < min:
                min = dist
                
    return min
        
        
def distance(a, b):
    apos = a.position()
    bpos = b.position()
    x = apos.x() - bpos.x()
    y = apos.y() - bpos.y()
    z = apos.z() - bpos.z()
    
    return math.sqrt(x**2 + y**2 + z**2)


def main()
	obj = hou.node("obj/RESIDENTIALhouse_mesh2331/")    
    
	w1 = hou.node("obj/RESIDENTIALhouse_mesh2331/delete2")
	w2 = hou.node("obj/RESIDENTIALhouse_mesh2331/delete3")

	t1 = hou.node("obj/RESIDENTIALhouse_mesh2331/xform1")
	t2 = hou.node("obj/RESIDENTIALhouse_mesh2331/xform2")


	c1 = w1.geometry().boundingBox().center()
	c2 = w2.geometry().boundingBox().center()

	z = c1.z()-c2.z()

	t2.parm('tz').set(z)

	print Hausdorff(t1,t2)