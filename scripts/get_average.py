import hou

def main(object):
	sum = hou.Vector3()
	totalA = 0
	prims = object.geometry().prims()
	
	for prim in prims:
		area = prim.intrinsicValue("measuredarea")
		normal = prim.normal()

		sum += area * normal
		totalA += area

	return sum/totalA
