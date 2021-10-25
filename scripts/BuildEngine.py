import get_average
import hou
reload(get_average)


def find_similar_normal(normal, dict):
	for key in dict:
		if key.dot(normal) > 0.5:
			return key
            
	return normal


def BuildWall(wall, elements, comp, obj, stories, filter):
	right = hou.Vector3(1,0,0)
	left = hou.Vector3(-1,0,0)
	back = hou.Vector3(0,0,-1)
	front = hou.Vector3(0,0,1)
	cardinals = [front,back,left,right]
	
	merge = obj.createNode('merge')
	
	bbox = wall.geometry().boundingBox()
	totalsize = bbox.sizevec().z()
	values = []
			
	normal = get_average.main(wall)
	similar = find_similar_normal(normal,cardinals)
	
	if similar == right or similar == left:
		index = 2
		if similar == right:
			ry = 270
		else:
			ry = 90
	else:
		index = 0
		if similar == front:
			ry = 0
		else:
			ry = 180


	for element in elements:
		bbox = element.geometry().boundingBox()
		size = bbox.sizevec()[index]
		if totalsize == 0:
			totalsize = 0.0001
		values.append(size/totalsize)
		

	subdiv = obj.createNode("Subdiv")
	subdiv.setNextInput(stories)
	subdiv.moveToGoodPosition()

	subdiv.parm("filter").set(filter)
	subdiv.parm("axis").set(0)
	subdiv.parm("Divisions").set(len(elements))

	
	for i in range(len(elements)):
		element = elements[i]
		xform = obj.createNode("xform")
		xform.setNextInput(element)
		xform.parm("ry").set(ry)

		value = "value" + str(i)
		product = "product" + str(i)
		subdiv.parm(value).set(values[i])
		subdiv.parm(product).set(element.name())
		subdiv.parm("rel"+str(i)).set(True)
		
		
		xform.parm("movecentroid").pressButton()
		path = hou.hipFile.path().replace(hou.hipFile.basename(),'')
		path += "elements/"+element.name()+".bgeo"
		xform.geometry().saveToFile(path)
		xform.destroy()
		
		
		insert = obj.createNode("Insert")
		insert.setNextInput(subdiv)
		insert.moveToGoodPosition()
		
		insert.parm("filter").set(element.name())
		insert.parm("product0").set(element.name()+"OK")
		insert.parm("asset").set(path)
		
		merge.setNextInput(insert)
		merge.setDisplayFlag(True)
		
		
	
	
	merge.moveToGoodPosition()
	
	return merge
	
		
