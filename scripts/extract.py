import config
import os
import hou
reload(config)



def delete_digits(name):
    for letter in name:
        if letter.isdigit():
            name = name.replace(letter,'')
            
    return name
            

def search_element(elem, file):
    element = []
    for line in file:
        split = line.split()
        if split[0] == elem:
            split.remove(elem)
            for prim in split:
                element.append(int(prim))
                
            break
                
    return element


def get_material(prim):
    path = extract_path(prim)
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


def main(obj, node, objective = None, element = None):
	hipdir = os.environ["HIP"]
	path = hipdir+"\ANN_output_sample\comp_level\Elements.txt"
	f = open(path, 'r')

	remove = [] 
	objects = []

	if objective != None:
		for object in f:
			object = object.split()
			name = object.pop(0)
			if delete_digits(name) in objective:
				objects.append(name)

		f.seek(0)

	if objective != None:
		for object in objects:
			prims = search_element(object,f)
			for prim in prims:
				remove.append(str(prim)) 
	else:
		prims = search_element(element,f)
		for prim in prims:
			remove.append(str(prim))    

	delete = obj.createNode('delete')
	delete.setNextInput(node)
	delete.moveToGoodPosition()

	string = ' '.join(remove)
	delete.parm('group').set(string)
	delete.parm('negate').set(1)
	delete.setDisplayFlag(True)

	print "Extracted"