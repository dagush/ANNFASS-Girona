import config
import sys
import hou
import os
reload(config)
sys.setrecursionlimit(100000)


def delete_selected(delete, mat_dict, string):
    
    eliminar = ""
    for value in mat_dict:
        for object in mat_dict[value]:
            if string in object:
                for i in range(len(object)):
                    object[i] = str(object[i])
            
                #eliminar = object.remove(string)
                
                eliminar = ' '.join(object)
                delete.parm('group').set(eliminar)
                delete.parm('negate').set(1)
                delete.setDisplayFlag(True)
                
                break
            
    return None


def print_dic(mat_dict):
    for value in mat_dict:
        if mat_dict[value] != []:
            print value+":"
            for object in mat_dict[value]:
                print "    "+str(object)
                

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
	
	
	
def main(building):
	mat_dict = {}            
        
	node = hou.node(building)
	geo = node.geometry()

	prims = geo.prims()
	visited = []
	classified = []

	for prim in prims:
		if prim.number() not in visited:
			mat = get_material(prim)
			if mat != "":
				object = ""
				object = find_neighbours(prim, mat, mat_dict, visited, object)
    
				add_in_dic(prim, object, mat, mat_dict)        
            
 
	hipdir = os.environ["HIP"]
	path = hipdir+"/ANN_output_sample/comp_level/Elements.txt"
	f = open(path, 'w')

	for value in mat_dict:
		for material in mat_dict[value]:
			element = []
			for object in material:
				element.append(str(object))
        
			element = ' '.join(element)
			f.write(element+"\n")
    

	f.close()

	print "Classified"
            