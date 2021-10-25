import hou

def get_material(prim):
    mat = prim.attribValue("shop_materialpath")
    mat = mat.replace("/mat/",'')
    return mat
    
    
def get_element(prim, elem_dic):
    strprim = str(prim.number())
    mat = ""
    for element in elem_dic:
        if strprim in elem_dic[element]:
            mat = element
            break
            
    return mat


def get_neighbours(prim, elem_dic):
    primPts = prim.points()
    mat = get_material(prim)
    neighs = []

    for pt in primPts:
        ptPrims = pt.prims()
    
        for ptPrim in ptPrims:
            if ptPrim != prim:
                auxPts = ptPrim.points()
                for auxPt in auxPts:
                    if auxPt != pt and auxPt in primPts:
                        aux_mat = get_material(ptPrim)
                        if aux_mat != mat:
                            element = get_element(ptPrim,elem_dic)
                            neighs.append(element)
                            
    return neighs
                            


path = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
f = open(path, 'r')

path2 = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Graph.txt"
f2 = open(path2, 'w')

node = hou.node("obj/COMMERCIALhouse_mesh0798/fuse1")
geo = node.geometry()

elem_dic = {}

for element in f:
    element = element.split()
    name = element.pop(0)
    elem_dic[name] = element
    
f.seek(0)

for element in f:
    element = element.split()
    name = element.pop(0)
    link = [name]
    
    for i in element:
        prim = geo.prim(int(i))
        neighs = get_neighbours(prim, elem_dic)
        
        for neigh in neighs:
            if neigh not in link:
                link.append(neigh)
    
    link = ' '.join(link)
    f2.write(link+"\n")
    
f.close()
f2.close()
    
print "completed"