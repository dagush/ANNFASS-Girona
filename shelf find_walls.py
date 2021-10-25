import sys, os
sys.path.append(os.getcwd()+"\\scripts")

import find_walls
reload(find_walls) #ugly, but eases changes

path = "obj/RELIGIOUSchurch_mesh1365"

obj = hou.node(path)
node = hou.node(path + "/Transform2")
comp = hou.node(path + "/comp1")

find_walls.main(obj, node, comp)