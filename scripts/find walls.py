import math
import sys
import config
reload(config)
sys.setrecursionlimit(100000)


def match_size(box, building):
    geo = building.geometry()
    bbox = geo.boundingBox()

    box.parm('sizex').set(bbox.sizevec().x())
    box.parm('sizey').set(bbox.sizevec().y())
    box.parm('sizez').set(bbox.sizevec().z())

    box.parm('tx').set(bbox.center().x())
    box.parm('ty').set(bbox.center().y())
    box.parm('tz').set(bbox.center().z())

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


def closest_object(object,list):
    min = 99999
    res = None
    
    for elem in list:
        dist = Hausdorff(object,elem)
        if dist < min:
            min = dist
            res = elem
    
    return res
        
    
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


def delete_digits(name):
    for letter in name:
        if letter.isdigit():
            name = name.replace(letter,'')
            
    return name
    
    
def extract_object(delete, object):
    string = []
    for prim in object:
        string.append(str(prim))
    string = ' '.join(string)
    delete.parm('group').set(string)
    delete.parm('negate').set(1)
    
    return delete
    
    
def extract_cardinal(cardinals, key):
    for cardinal in cardinals:
        if key in cardinal:
            return cardinal[0]
    
    return "Error"
    
    
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
    
    
def extract_type(type):
    type = type.replace("<hou.SopNodeType for Sop ",'')
    type = type.replace(">",'')
    return type
    
    
def add_to_dict(elem,dict,key):
    if key not in dict:
        dict[key] = []
        
    dict[key].append(elem)
    
    
def print_dict(dict):
    for key in dict:
        print str(key)+":"
        for elem in dict[key]:
            print "    "+str(elem)
            
            
def find_similar_normal(normal, dict):
    for key in dict:
        if key.dot(normal) > 0.5:
            return key
            
    return normal
    
    
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
    
    
def average(list):
    sum = 0
    for elem in list:
        sum += elem
        
    return sum/len(list)
    
    
def are_close(h1, h2):
    denom = max(h1,h2)
    if denom == 0:
        denom = (h1+h2)/2
        
    diff = abs(h2-h1)/denom
    if diff < 0.75:
        return True
    else:
        return False
    
    
def find_wall(prim,visited,wall):
    if prim.number() not in visited:
        visited.append(prim.number())
        wall.append(prim.number())
    
        primPts = prim.points()
        for primPt in primPts:
            ptPrims = primPt.prims()
            for ptPrim in ptPrims:
                if ptPrim != prim and ptPrim.number() not in visited:
                    find_wall(ptPrim,visited,wall)
                    
                    
def add_to_stories(stories, center, bottom, top, object):
    if stories == {}:
        stories[0] = [[center]]
        stories[0].append([bottom])
        stories[0].append([top])
        stories[0].append([object])
    
    else:
        for i in stories:
            auxCenter = average(stories[i][0])
            if are_close(center,auxCenter):
                stories[i][0].append(center)
                stories[i][1].append(bottom)
                stories[i][2].append(top)
                stories[i][3].append(object)
                return
        
        newLevel = len(stories)
        stories[newLevel] = [[center]]
        stories[newLevel].append([bottom])
        stories[newLevel].append([top])
        stories[newLevel].append([object])
        
        
def sort_stories(stories):
    for x in stories:
        min = 9999
        floor = None
        for y in stories:
            aux = average(stories[y][0])
            if aux < min:
                min = average(stories[y][0])
                floor = y
                
        if min < average(stories[x][0]):
            stories[x],stories[y] = stories[y],stories[x]
            
           
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
        
        
def find_index_of_wall(divisions, wall):
    for d in divisions:
        if wall == d[0]:
            return divisions.index(d)
            
    return "[NOT FOUND]"
    
    
def find_index_of_floor(divisions, floor):
    for walls in divisions:
        for floors in walls:
            if floor == floors[0]:
                return [divisions.index(walls),walls.index(floors)]
                
    return "[NOT FOUND]"
        
        
def add_to_divisions(divisions, object, code, wall=None, floor=None):
    if code == 'wall':
        divisions.append([object])
    elif code == 'floor':
        index = find_index_of_wall(divisions, wall)
        divisions[index].append([object])
    elif code == 'element':
        index = find_index_of_floor(divisions, floor)
        divisions[index[0]][index[1]].append(object)
        
        
def generate_elements_id(objects):
    id = "0"
    for i in objects:
        element = config.GET_CODE(delete_digits(objects[i][3]))
        id += str(element)+"0"
        
    return id
	
	
def init_cardinals(prims):
	normals = {}
	up = hou.Vector3(0,1,0)
	down = hou.Vector3(0,-1,0)
	front = hou.Vector3(1,0,0)
	back = hou.Vector3(-1,0,0)
	left = hou.Vector3(0,0,-1)
	right = hou.Vector3(0,0,1)
	cardinals = [["front",front],["back",back],["left",left],["right",right]]

	normals[front] = []
	normals[back] = []
	normals[left] = []
	normals[right] = []

    for prim in prims:
        normal = prim.normal()
        if normal != hou.Vector3(0,0,0):
            key = find_similar_normal(normal,normals)
            if normal.dot(up) < 0.5 and normal.dot(down) < 0.5:
                add_to_dict(prim.number(),normals,key)
				
	for key in normals:
		cardinal = extract_cardinal(cardinals,key)
		delete = obj.createNode('delete',cardinal)
		delete.setNextInput(node)
		delete.moveToGoodPosition()
    
		extract = []
		for prim in normals[key]:
			extract.append(str(prim))
        
		extract = ' '.join(extract)
		delete.parm('group').set(extract)
		delete.parm('negate').set(1)
        

def main(obj, node):    
	geo = node.geometry()

#path = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
#f = open(path, 'r')

	prims = geo.prims()
	init_cardinals(prims)

	bbox = geo.boundingBox()
	frontArea = bbox.sizevec().x()*bbox.sizevec().y()
	sideArea = bbox.sizevec().z()*bbox.sizevec().y()


	leftovers = []
	walls = []

	divisions = []
	
	for child in obj.children():
		type = extract_type(str(child.type()))
		if type == "delete": #and child.name() != "delete1":
			geo = child.geometry()
			prims = geo.prims()
			visited = []
			for prim in prims:
				wall = []
				if prim.number() not in visited:
					find_wall(prim,visited,wall)
					if len(visited) > 0:
						delete = obj.createNode('delete')
						delete.setNextInput(child)
						delete.moveToGoodPosition()
                    
						extract = []
						for i in wall:
							extract.append(str(i))
                        
						extract = ' '.join(extract)
						delete.parm('group').set(extract)
						delete.parm('negate').set(1)
                    
						bbox = delete.geometry().boundingBox()
						fArea = bbox.sizevec().x()*bbox.sizevec().y()
						sArea = bbox.sizevec().z()*bbox.sizevec().y()
                    
						if sArea != 0 or fArea != 0:
							if fArea > sArea:
								if frontArea/fArea > 20:
									leftovers.append(delete)
								else:  
									merge = obj.createNode('merge','Wall')
									merge.setNextInput(delete)
									walls.append(merge)
									add_to_divisions(divisions,merge.name(),'wall')
							else:
								if sideArea/sArea > 20:
									leftovers.append(delete)
								else:
									merge = obj.createNode('merge','Wall')
									merge.setNextInput(delete)
									walls.append(merge)
									add_to_divisions(divisions,merge.name(),'wall')
                
                                                       
            
	for left in leftovers:
		closest = closest_object(left,walls)
		closest.setNextInput(left)
    
    
	floors = []
    
	for wall in walls:
		prims = wall.geometry().prims()
		visited = []
		classified = []
		mat_dict = {}
    
		for prim in prims:
			if prim.number() not in visited:
				mat = get_material(prim)
				if mat != "":
					object = ""
					object = find_neighbours(prim, mat, mat_dict, visited, object)
    
					add_in_dic(prim, object, mat, mat_dict)
    
		if 'window' in mat_dict:
			stories = {}
			for window in mat_dict['window']:
				name = window.pop(0)
            
				delete = obj.createNode('delete')
				delete.setNextInput(wall)
				delete = extract_object(delete,window)
            
				bbox = delete.geometry().boundingBox()
				center = bbox.center().y()
				bottom = bbox.minvec().y()
				top = bbox.maxvec().y()
				add_to_stories(stories,center,bottom,top,name)
				delete.destroy()
        
			bbox = wall.geometry().boundingBox()
			sort_stories(stories)
    
			floor = bbox.minvec().y()
			roof = bbox.maxvec().y()
    
			nFloors = len(stories)-1
    
			for i in stories:
				if i < nFloors:
					distance = abs(floor-min(stories[i+1][1]))
					top = min(stories[i+1][1])-distance

					if top < max(stories[i][2]):
						distance = abs(max(stories[nFloors][2])-roof)
						top = max(stories[i][2])+distance
        
						if top > min(stories[i+1][1]):
							top = (max(stories[i][2])+min(stories[i+1][1]))/2
        
				else:
					top = roof

				center = (floor+top)/2
    
				box = obj.createNode('box')
				match_size(box,wall)
    
				box.parm('sizey').set(0)
				box.parm('ty').set(center)
    

				add = 0.0001
				loop = 0

				bbox2 = box.geometry().boundingBox()

				while bbox2.minvec().y() >= floor and loop < 1000000:
					sizey = box.evalParm('sizey')
					sizey += add
					box.parm('sizey').set(sizey)
					loop += 1
					bbox2 = box.geometry().boundingBox()
    
    
				boolean = obj.createNode('boolean',wall.name()+"_Floor"+str(i))
				boolean.setNextInput(wall)
				boolean.setNextInput(box)
    
				boolean.parm('asurface').set(1)
				boolean.parm('bsurface').set(0)
				boolean.parm('booleanop').set(1)
    
				box.moveToGoodPosition()
				boolean.moveToGoodPosition()
				floors.append(boolean)
				add_to_divisions(divisions,boolean.name(),'floor',wall.name())
    
				floor = top
            
		else:
			floors.append(wall)
			newName = wall.name()+"_Floor0"
			add_to_divisions(divisions,newName,'floor',wall.name())
			wall.setName(newName)
            
        
	for floor in floors:
		delete = obj.createNode('delete')
		delete.setNextInput(floor)
		delete.moveToGoodPosition()
    
		prims = floor.geometry().prims()
    
		visited = []
		classified = []
		mat_dict = {}
		objects = {}
    
		for prim in prims:
			if prim.number() not in visited:
				mat = get_material(prim)
				if mat != "":
					object = ""
					object = find_neighbours(prim,mat,mat_dict,visited,object)
                
					add_in_dic(prim,object,mat,mat_dict)
                
					if delete_digits(object) != "wall":
						delete = extract_object(delete,find_in_dict(mat_dict,object))
						bbox = delete.geometry().boundingBox()
						fArea = bbox.sizevec().x()*bbox.sizevec().y()
						sArea = bbox.sizevec().z()*bbox.sizevec().y()
                    
						floorbbox = floor.geometry().boundingBox()
						frontArea = floorbbox.sizevec().x()*floorbbox.sizevec().y()
						sideArea = floorbbox.sizevec().z()*floorbbox.sizevec().y()
                    
						if fArea != 0 or sArea != 0:
							if fArea > sArea:
								if frontArea/fArea > 5:
									center = bbox.center().x()
									left = bbox.minvec().x()
									right = bbox.maxvec().x()
									add_to_objects(objects,center,left,right,object)
                    
							else:
								if sideArea/sArea > 5:
									center = bbox.center().z()
									left = bbox.minvec().z()
									right = bbox.maxvec().z()
									add_to_objects(objects,center,left,right,object)
                    
                    
		sort_objects(objects)
		id = generate_elements_id(objects)
		add_to_divisions(divisions,id,'element',None,floor.name())
    
		floorbbox = floor.geometry().boundingBox()
		fArea = floorbbox.sizevec().x()*floorbbox.sizevec().y()
		sArea = floorbbox.sizevec().z()*floorbbox.sizevec().y()
    
		if fArea > sArea:
			center = floorbbox.center().x()
			left = floorbbox.minvec().x()
			right = floorbbox.maxvec().x()
			sizeparm = 'sizex'
			tparm = 'tx'
		else:
			center = floorbbox.center().z()
			left = floorbbox.minvec().z()
			right = floorbbox.maxvec().z()
			sizeparm = 'sizez'
			tparm = 'tz'
        
		i = 0
		iteration = 'wall'
    
		while iteration != 'finish':
			break
			box = obj.createNode('box')
			match_size(box,floor)
        
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
			if fArea > sArea:
				min = bbox2.minvec().x()
			else:
				min = bbox2.minvec().z()
            
			while min >= left and loop < 1000:
				size = box.evalParm(sizeparm)
				size += add
				box.parm(sizeparm).set(size)
				loop += 1
            
				bbox2 = box.geometry().boundingBox()
				if fArea > sArea:
					min = bbox2.minvec().x()
				else:
					min = bbox2.minvec().z()
                
			boolean = obj.createNode('boolean')
			boolean.setNextInput(floor)
			boolean.setNextInput(box)
        
			boolean.parm('asurface').set(1)
			boolean.parm('bsurface').set(0)
			boolean.parm('booleanop').set(1)
        
			box.moveToGoodPosition()
			boolean.moveToGoodPosition()
        
			if iteration == 'wall':
				iteration = 'other'
				left = objects[i][1]
			elif iteration == 'other':
				iteration = 'wall'
				left = objects[i][2]
				i += 1
            
            
	for walls in divisions:
		if divisions.index(walls) != 0:
			print walls[0]
			for floors in walls:
				print "    "+floors[0]
				for element in floors:
					print "        "+str(element)
            
            
	print "Done"