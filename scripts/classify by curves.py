import hou
import math

def extract_element(elem, node):
    string = ' '.join(elem)
    node.parm('group').set(string)
    node.parm('negate').set(1)
                
    return node


def extract_type(type):
    type = type.replace("<hou.SopNodeType for Sop ",'')
    type = type.replace(">",'')
    return type
    
    
def extract_material(name):
    for letter in name:
        if letter.isdigit():
            name = name.replace(letter,'')
        
    return name
    
    
def get_curve(name,curves):
    for curve in curves:
        if curve.name() == name:
            return curve
            
    return None
    
    
def closest_object(object,curves):
    min = 99999
    res = None
    
    for curve in curves:
        dist = Hausdorff(object,curve)
        if dist < min:
            min = dist
            res = curve
    
    return res
    
            
        
def closest_curve(curve, wall, curves):
    min = 99999
    res = None
    
    if wall == None:
        for c in curves:
            if len(c.evalParm('coords').split()) > 4:
                if extract_material(c.name()) == "wall":
                    dist = Hausdorff(curve,c)
                    if dist < min:
                        res = c
                        min = dist
                    
    else:
        for x in wall:
            c = get_curve(x,curves)
            if len(c.evalParm('coords').split()) > 4:
                dist = Hausdorff(curve, c)
                if dist < min:
                    res = c
                    min = dist
            
    return res,min
    
    
def Hausdorff(a, b):
    ageo = a.geometry()
    bgeo = b.geometry()
    apoints = ageo.points()
    bpoints = bgeo.points()
    max = -99999
    
    for ap in apoints:
        for bp in bpoints:
            dist = distance(ap,bp)
            if dist > max:
                max = dist
                
    return max
        
        
def distance(a, b):
    apos = a.position()
    bpos = b.position()
    x = apos.x() - bpos.x()
    y = apos.y() - bpos.y()
    z = apos.z() - bpos.z()
    
    return math.sqrt(x**2 + y**2 + z**2)
    
        
path= "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Object Curves.txt"
f = open(path, 'r')

path2= "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
f2 = open(path2, 'r')

object_curves = {}
for line in f:
    line = line.split()
    name = line.pop(0)
    object_curves[name] = []
    for i in line:
        object_curves[name].append(i)


obj = hou.node("obj/RELIGIOUSchurch_mesh1365/")

curves = []

for node in obj.children():
    type = extract_type(str(node.type()))
    if type == "curve":
        curves.append(node)

node = hou.node("obj/RELIGIOUSchurch_mesh1365/fuse1")
#geo = node.geometry()

delete = hou.node("obj/RELIGIOUSchurch_mesh1365/delete2")

window_curves = []

for object in f2:
    object = object.split()
    name = object.pop(0)
    if extract_material(name) == "window":
        delete = extract_element(object,delete)
        curve = closest_object(delete,curves)
        window_curves.append(curve)
        
for curve in curves:
    if curve not in window_curves:
        curve.destroy()
        
        
#wall = object_curves["wall0"]

#curve_dict = {}

#for curve in curves:
#    if extract_material(curve.name()) == "window":
#        res = closest_curve(curve, wall, curves)
#        if res[0].name() not in curve_dict:
#            curve_dict[res[0].name()] = []
        
#        curve_dict[res[0].name()].append(curve.name())
#        print curve.name() + " -> " + res[0].name() + ": " + str(res[1])

#for key in curve_dict:
#    print key
#    for elem in curve_dict[key]:
#        print "    "+elem
        
    
    
#print curve_dict["wall16"]
print "Done" 

f.close()
f2.close()
