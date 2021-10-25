import hou

def get_material(prim):
    mat = prim.attribValue("shop_materialpath")
    mat = mat.replace("/mat/",'')
    return mat

node = hou.node("obj/COMMERCIALhouse_mesh0798/fuse1")
geo = node.geometry()

prims = geo.prims()
neighb = []

for prim in prims:
    primPts = prim.points()
    nearPrims = []
    mat = []

    for pt in primPts:
        ptPrims = pt.prims()
    
        for ptPrim in ptPrims:
            if ptPrim != prim and ptPrim.number() not in nearPrims:
                auxPts = ptPrim.points()
                for auxPt in auxPts:
                    if auxPt != pt and auxPt in primPts:
                        nearPrims.append(ptPrim.number())
                        mat.append(get_material(ptPrim))
    
    neighb.append([prim.number(), get_material(prim), mat])
    print str(prim.number()) + ": " + str(nearPrims)
    print get_material(prim) + ": " + str(mat)