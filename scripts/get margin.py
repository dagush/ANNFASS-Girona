import config
reload(config)


def print_dic(mat_dic):
    for value in mat_dic:
        if mat_dic[value] != []:
            print value+":"
            for object in mat_dic[value]:
                print "    "+str(object)


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
    
def get_element(prim,elem_dic):
    for element in elem_dic:
        if prim.number() in elem_dic[element]:
            return element
            
    return None
    
    
def get_edge(prim, edges):
    points = prim.points()
    for x in points:
        for y in points:
            edge = geo.findEdge(x, y)
            if edge != None and edge not in edges:
                #if get_element(prim,elem_dic) == "window9":
                #    print geo.findEdge(x,y).edgeId()
                f.write(str(geo.findEdge(x,y).edgeId())+"\n")
                f.write(str(geo.findEdge(y,x).edgeId())+"\n")

    
path = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Edges.txt"
f = open(path, 'w')
path2 = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
f2 = open(path2, 'r')

elem_dic = {}

for element in f2:
    element = element.split()
    name = element.pop(0)
    elem_dic[name] = []
    for elem in element:
        elem_dic[name].append(int(elem))
        

node = hou.node("obj/COMMERCIALhouse_mesh0798/fuse1")
geo = node.geometry()
prims = geo.prims()

margin = []

prim_dic = {}

for prim in prims:
    if get_material(prim) != "":
    #if get_element(prim,elem_dic) == "window8":
        edges = []
        primPts = prim.points()
        neigh = 0
        used = []
        for pt in primPts:
            ptPrims = pt.prims()    
            for ptPrim in ptPrims:
                if ptPrim != prim and get_material(ptPrim) == get_material(prim) and ptPrim.points() != prim.points():
                    auxPts = ptPrim.points()
                    for auxPt in auxPts:
                        if auxPt != pt and auxPt in primPts and ptPrim.number() not in used:
                            edge = geo.findEdge(auxPt,pt)
                            edge2 = geo.findEdge(pt,auxPt)
                            if edge not in edges and edge2 not in edges:
                                neigh += 1
                                used.append(ptPrim.number())
                                edges.append(edge)
                                edges.append(edge2)
            
        if neigh < len(primPts):
            #if get_element(prim,elem_dic) == "window9":
            #    print prim.number()
            #    for edge in edges:
            #        print edge.edgeId()
                    
            #    print "\n"
            margin.append(str(prim.number()))
            get_edge(prim, edges)               
            
    
f.close()
f2.close()

print "Get Margin Done"