import math
import get_average
reload(get_average)

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


def main(obj, w1, w2):

	t1 = obj.createNode('xform')
	t1.setNextInput(w1)
	t1.moveToGoodPosition()
	
	t2 = obj.createNode('xform')
	t2.setNextInput(w2)
	t2.moveToGoodPosition()
	
	#normal1 = get_average.main(w1)
	#normal2 = get_average.main(w2)
	
	#d = normal1.angleTo(normal2)
	#t2.parm('ry').set(d)

	bbox1 = w1.geometry().boundingBox()
	bbox2 = w2.geometry().boundingBox()
	
	c1 = bbox1.center()
	c2 = bbox2.center()

	c = c1-c2

	t2.parm('tx').set(c.x())
	t2.parm('ty').set(c.y())
	t2.parm('tz').set(c.z())
	
	h = Hausdorff(t1,t2)
	
	t1.destroy()
	t2.destroy()
	
	return h