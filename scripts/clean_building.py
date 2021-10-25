import config
reload(config)

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
    
def main(obj, node):
	geo = node.geometry()
	prims = geo.prims()

	remove = []

	for prim in prims:
		if get_material(prim) == "undetermined" or get_material(prim) == "facade" or get_material(prim) == "roof":
			remove.append(str(prim.number()))

        
	delete = obj.createNode('delete')
	delete.setNextInput(node)
	delete.moveToGoodPosition()

	string = ' '.join(remove)
	delete.parm('group').set(string)
	delete.parm('negate').set(0)
	delete.setDisplayFlag(True)

	print "Cleaned"