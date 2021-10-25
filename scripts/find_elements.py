import config
import hou
import compare_elements
import get_average
reload(get_average)
reload(config)
reload(compare_elements)


def print_dict(dict):
	for key in dict:
		print str(key)+":"
		for elem in dict[key]:
			print "	   "+str(elem)


def get_material(prim):
	path = extract_path(prim)
	if config.GET_MATERIAL(path) == "other":
		print path
	return config.GET_MATERIAL(path)

def extract_path(prim):
	mat = prim.attribValue("path")
	mat = mat.replace("/",'')
	if mat.isdigit():
		mat = prim.attribValue("shop_materialpath")
	
	mat = mat.replace("/mat/",'')
	mat = mat.replace("Mesh",'')
	mat = mat.replace("/",'')
	mat = mat.replace("_",'')
	mat = mat.replace(".",'')
	for letter in mat:
		if letter.isdigit():
			mat = mat.replace(letter,'')
		
	return mat	
	
	
def extract_object(delete, object):
	string = []
	for elem in object:
		string.append(str(elem))

	string = ' '.join(string)
	delete.parm('group').set(string)
	delete.parm('negate').set(1)
	
	return delete
	
	
def find_neighbours(prim, mat, mat_dict, visited, object):	  
	visited.append(prim.number())	 
	
	
	classified = is_in_dic(prim, mat, mat_dict)
	if classified != "":
		return classified
		
	if object != "":
		add_in_dic(prim, object, mat, mat_dict)
		
	
	primPts = prim.points()		   
	
	for primPt in primPts:
		ptPrims = primPt.prims()
		
		for ptPrim in ptPrims:
			if get_material(ptPrim) == get_material(prim):
				if ptPrim != prim and ptPrim.number() not in visited:
					object = find_neighbours(ptPrim, mat, mat_dict, visited, object)
					found = is_in_dic(prim, mat, mat_dict)
					if found == "":
						add_in_dic(prim, object, mat, mat_dict)
				
				
	if object == "":
		object = search_object(prim, mat, mat_dict)
		add_in_dic(prim, object, mat, mat_dict)
			
	return object
	

def extract_type(type):
	type = type.replace("<hou.SopNodeType for Sop ",'')
	type = type.replace(">",'')
	return type
	
	
def add_in_dic(prim, object, mat, mat_dict):
	if mat not in mat_dict:
		mat_dict[mat] = []
		mat_dict[mat].append([object])
		mat_dict[mat][0].append(prim.number())
		
	else:
		for value in mat_dict[mat]:
			if value[0] == object:
				if prim.number() not in value:
					value.append(prim.number())
				break
				
				
def is_in_dic(prim, mat, mat_dict):
	found = ""
	
	if mat in mat_dict:
		for value in mat_dict[mat]:
			if prim.number() in value:
				found = value[0]
				break
			
	return found
	
	
def search_object(prim, mat, mat_dict):
	object = ""
	
	if mat not in mat_dict:
		mat_dict[mat] = []
		object = mat+"0"
		mat_dict[mat].append([object])
	
	else:
		size = len(mat_dict[mat])
		object = mat + str(size)
		mat_dict[mat].append([object])
			
	return object
	
	
def delete_numbers(name):
	for letter in name:
		if letter.isdigit():
			name = name.replace(letter,'')
			
	return name
	

def delete_digits(name):
	for letter in name:
		if not letter.isdigit():
			name = name.replace(letter,'')
			
	return name
	
	
def find_in_dict(dict,name):
	for key in dict:
		for list in dict[key]:
			if list[0] == name:
				return list
			
	return "[NOT FOUND]"
	
	
def add_to_objects(objects, center, left, right, object):
	if objects == {}:
		newLevel = 0
	else:
		newLevel = len(objects)

	objects[newLevel] = [center,left,right,object]
	
	
def match_size(box, building):
	geo = building.geometry()
	bbox = geo.boundingBox()

	box.parm('sizex').set(bbox.sizevec().x())
	box.parm('sizey').set(bbox.sizevec().y())
	box.parm('sizez').set(bbox.sizevec().z())

	box.parm('tx').set(bbox.center().x())
	box.parm('ty').set(bbox.center().y())
	box.parm('tz').set(bbox.center().z())
	
	
def sort_objects(objects):
	sorted = []
	for x in objects:
		min = 9999
		left = None
		for y in objects:
			if y not in sorted:
				aux = objects[y][0]
				if aux < min:
					min = aux
					left = y
				
		if min < objects[x][0]:
			objects[x],objects[left] = objects[left],objects[x]
			
		sorted.append(x)
	

def generate_elements_id(objects):
	id = "Wall"
	for i in objects:
		id += "_"
		object = objects[i][3]
		#code = config.GET_CODE(delete_numbers(object))
		id += object + "_Wall"
		#id += str(code)+delete_digits(object)+"_0"
        
	return id
	
	
def find_similar_object(obj, object, elements):
	for elem in elements:
		if object.name() != elem.name():
			if delete_numbers(object.name()) == delete_numbers(elem.name()):
				if compare_elements.main(obj,object,elem) < 0.00001:
					return elem.name()
					
	return object.name()
	
	
def get_area_of_object(object,obj):
	prims = object.geometry().prims()
	totalarea = 0
	for prim in prims:
		totalarea += prim.intrinsicValue("measuredarea")
	return totalarea
	
	
def find_similar_normal(normal, list):
    for elem in list:
        if elem.dot(normal) > 0.5:
            return elem
            
    return normal


def main(obj, node):
	right = hou.Vector3(1,0,0)
	left = hou.Vector3(-1,0,0)
	back = hou.Vector3(0,0,-1)
	front = hou.Vector3(0,0,1)
	cardinals = [front,back,left,right]
	
	prims = node.geometry().prims()

	visited = []
	classified = []
	mat_dict = {}
	objects = {}
	elements = []
	
	normal = get_average.main(node)
	similar = find_similar_normal(normal,cardinals)
	if similar == right or similar == left:
		index = 2
		sizeparm = 'sizez'
		tparm = 'tz'
	else:
		index = 0
		sizeparm = 'sizex'
		tparm = 'tx'

	for prim in prims:
		if prim.number() not in visited:
			mat = get_material(prim)
			if mat != "":
				object = ""
				object = find_neighbours(prim, mat, mat_dict, visited, object)
	
				add_in_dic(prim, object, mat, mat_dict)
			
				if delete_numbers(object) != "wall":
					delete = obj.createNode('delete', object)
					delete.setNextInput(node)
					delete.moveToGoodPosition()
					elements.append(delete)
					
					detele = extract_object(delete,find_in_dict(mat_dict,object))
					
					totalarea = get_area_of_object(node,obj)
					area = get_area_of_object(delete,obj)
					if area == 0:
						area = 0.00001
					
					if totalarea / area < 50:
						bbox = delete.geometry().boundingBox()

						center = bbox.center()[index]
						left = bbox.minvec()[index]
						right = bbox.maxvec()[index]
						object = find_similar_object(obj,delete,elements)
						add_to_objects(objects,center,left,right,object)
						
				
	sort_objects(objects)
	print generate_elements_id(objects)
#print_dict(objects)
				
	wallbbox = node.geometry().boundingBox()
	
	center = wallbbox.center()[index]
	left = wallbbox.minvec()[index]
	right = wallbbox.maxvec()[index]


	i = 0
	iteration = 'wall'
	
	result = []

	while iteration != 'finish':
		box = obj.createNode('box')
		match_size(box,node)	
	
		if iteration == 'wall':
			if i < len(objects):
				newcenter = (left+objects[i][1])/2
			else:
				newcenter = (left+right)/2
				iteration = 'finish'
		else:
			newcenter = objects[i][0]		

		box.parm(sizeparm).set(0)
		box.parm(tparm).set(newcenter)

		add = 0.0001
		loop = 0

		bbox2 = box.geometry().boundingBox()
		min = bbox2.minvec()[index]

	
		while min >= left:# and loop < 1000:
			size = box.evalParm(sizeparm)
			size += add
			box.parm(sizeparm).set(size)
			loop += 1
	
			bbox2 = box.geometry().boundingBox()
			min = bbox2.minvec()[index]

		
		
		boolean = obj.createNode('boolean')
		boolean.setNextInput(node)
		boolean.setNextInput(box)

		boolean.parm('asurface').set(1)
		boolean.parm('resolvea').set(False)
		boolean.parm('bsurface').set(0)
		boolean.parm('booleanop').set(1)

		box.moveToGoodPosition()
		boolean.moveToGoodPosition()
		boolean.setDisplayFlag(True)
		result.append(boolean)
	
		if iteration == 'wall':
			iteration = 'other'
			left = objects[i][1]
		elif iteration == 'other':
			iteration = 'wall'
			left = objects[i][2] 
			i += 1
		

	print "Done"
	return list(reversed(result))
