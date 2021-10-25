import config
reload(config)


def print_dict(dict):
    for key in dict:
        print str(key)+":"
        for elem in dict[key]:
            print "    "+str(elem)


def match_size(box, building):
    geo = building.geometry()
    bbox = geo.boundingBox()

    box.parm('sizex').set(bbox.sizevec().x())
    box.parm('sizey').set(bbox.sizevec().y())
    box.parm('sizez').set(bbox.sizevec().z())

    box.parm('tx').set(bbox.center().x())
    box.parm('ty').set(bbox.center().y())
    box.parm('tz').set(bbox.center().z())

    
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
    

def search_element(elem, file):
    element = []
    for line in file:
        split = line.split()
        if split[0] == elem:
            split.remove(elem)
            for prim in split:
                element.append(int(prim))
                
            break
                
    file.seek(0)
    return element


def delete_digits(name):
    for letter in name:
        if letter.isdigit():
            name = name.replace(letter,'')
            
    return name
    
    
def extract_object(delete, object):
    string = ' '.join(object)
    delete.parm('group').set(string)
    delete.parm('negate').set(1)
    
    return delete
    
    
def are_close(h1, h2):
    diff = abs(h2-h1)/max(h1,h2)
    if diff < 0.75:
        return True
    else:
        return False
        
        
def average(list):
    sum = 0
    for elem in list:
        sum += elem
        
    return sum/len(list)
    
    
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
        
               

path = "C:\Users\GL553\Documents\HoudiniProjects\ANNFASS\ANN_output_sample\comp_level\Elements.txt"
f = open(path, 'r')

node = hou.node("obj/16_English_school_refinedTextures/")

building = hou.node("obj/16_English_school_refinedTextures/fuse2")
bbox = building.geometry().boundingBox()
delete = node.createNode('delete')
delete.setNextInput(building)
delete.moveToGoodPosition()
   
stories = {}

for object in f:
    object = object.split()
    name = object.pop(0)
    if delete_digits(name) == "window":
        delete = extract_object(delete,object)
        bbox = delete.geometry().boundingBox()
        center = bbox.center().y()
        bottom = bbox.minvec().y()
        top = bbox.maxvec().y()
        add_to_stories(stories,center,bottom,top,name)

        

bbox = building.geometry().boundingBox()
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
    
    box = node.createNode('box')
    match_size(box,building)
    
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
    
    
    boolean = node.createNode('boolean',"floor"+str(i))
    boolean.setNextInput(building)
    boolean.setNextInput(box)
    
    boolean.parm('asurface').set(1)
    boolean.parm('bsurface').set(0)
    boolean.parm('booleanop').set(1)
    
    box.moveToGoodPosition()
    boolean.moveToGoodPosition()
    
    floor = top

