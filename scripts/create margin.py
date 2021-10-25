import config
reload(config)

def extract_material(name):
    for letter in name:
        if letter.isdigit():
            name = name.replace(letter,'')
        
    return name


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
    
def get_points(edge):
    edge = edge.replace('p','')
    edge = edge.replace('-',' ')
    return [geo.point(int(s)) for s in edge.split() if s.isdigit()]
    
    
def common_prims(pointA, pointB):
    edge = geo.findEdge(pointA,pointB)
    common = edge.prims()
    
    return common
    
    
def get_object_of_prim(prim, elem_dic):
    for object in elem_dic:
        if prim.number() in elem_dic[object]:
            return object
            
    return None
    
    
def has_common_object(pointA, pointB, object_name, elem_dic):
    prims = common_prims(pointA,pointB)
    
    for prim in prims:
        if get_object_of_prim(prim, elem_dic) == object_name:
            return True
            
    return False
    
    
    
def get_coord(point):
    xyz = []
    for i in point.position():
        xyz.append(str(i))
    
    return ','.join(xyz)    
    
    
def create_curve(coord,name,merge):
    curve = hou.node("obj/COMMERCIALhouse_mesh0798/").createNode('curve',name)
    curve.moveToGoodPosition()
    coord = ' '.join(coord)
    
    curve.parm('coords').set(coord)
    curve.parm('close').set(False)
    merge.setNextInput(curve)   
    return curve
    
    
def find_point(point, visited, created_edges, coord, edges, object, elem_dic):
    prims = point.prims()
    finished = False
    for prim in prims:
        auxPts = prim.points()
        for auxPt in auxPts:
            if auxPt != point and has_common_object(point,auxPt,object,elem_dic):
                edge = geo.findEdge(auxPt,point).edgeId()
                if edge in edges and edge not in created_edges:
                    visited.append(point.number())
                    created_edges.append(edge)
                    created_edges.append(geo.findEdge(point,auxPt).edgeId())
                    coord.append(get_coord(point))
                    
                    if auxPt.number() not in visited:
                        find_point(auxPt,visited,created_edges,coord,edges,object,elem_dic)
                        
                    else:
                        coord.append(get_coord(auxPt))
                    

                    finished = True
                    break
                        
        if finished:
            break
                    
                    
    

path= "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Edges.txt"
f = open(path, 'r')

path2 = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
f2 = open(path2, 'r')

path3 = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Object Curves.txt"
f3 = open(path3, 'w')

node = hou.node("obj/COMMERCIALhouse_mesh0798/fuse1")
geo = node.geometry()

edges = []

for edge in f:
    edge = edge.replace("\n",'')
    edges.append(edge)
    
elem_dic = {}

for object in f2:
    object = object.split()
    name = object.pop(0)
    elem_dic[name] = []
    for prim in object:
        elem_dic[name].append(int(prim))
 

merge = hou.node("obj/COMMERCIALhouse_mesh0798/").createNode('merge')

object_curves = {}

f2.seek(0)

for object in f2:
    object = object.split()
    name = object.pop(0)
    
    if extract_material(name) == "wall":
        object_curves[name] = []
    
        visited = []
        created_edges = []
    
        for i in object:
            prim = geo.prim(int(i))
            points = prim.points()
            for point in points:
                if point.number() not in visited:
                    coord = []
                    find_point(point,visited,created_edges,coord,edges,name,elem_dic)
                
                    if len(coord) > 1:
                        if coord[0] == coord[len(coord)-1]:
                            curve = create_curve(coord,name,merge)
                            object_curves[name].append(curve.name())
                   
                
for name in object_curves:
    line = [name]
    
    if object_curves[name] != []:
        for value in object_curves[name]:
            line.append(value)
    
        line = ' '.join(line)
        f3.write(line+"\n")
                    
merge.setDisplayFlag(True)
merge.moveToGoodPosition()

f.close()
f2.close()
f3.close()

print "Margin Created"