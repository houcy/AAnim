import os
import json
import sys
from style import *
from collections import defaultdict
from graph_algorithm import GraphAlgorithm

def get_adjacency_list(file_name):
    is_directed = False
    adjacency_list = defaultdict(list)
    with open(file_name) as f:
        if ">" in f.read():
            is_directed = True
    with open(file_name) as f:
        contents = f.readlines()
        for line in contents[1:-1]:
            line = line.strip("\n")
            line = line.strip("\t")
            line = line.strip(" ")
            start, end = "", ""
            i = 0
            while line[i].isalnum():
                start += line[i]
                i+=1
            i = len(line) - 1
            while line[i].isalnum():
                end += line[i]
                i-=1
            if end not in adjacency_list[start]:
                adjacency_list[start].append(end)
            if not is_directed:
                if start not in adjacency_list[end]:
                    adjacency_list[end].append(start)
    return adjacency_list, is_directed

def transform_position_to_manim(position):
    max_x, max_y= 0, 0
    for e in position:
        x, y = position[e]
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    ratio = max(max_x/FINAL_WIDTH, max_y/FINAL_HEIGHT)   # Change denominators here to adjust the size of the graph
    new_position = {}
    for e in position:
        x, y = position[e]
        new_position[e] = (x/ratio, y/ratio)
    return new_position

def get_position():
    print("command1", sys.argv[2] + " -Tpng " + sys.argv[1] + " -o output.png")
    print("command2", sys.argv[2] + " -Tjson0 " + sys.argv[1] + " -o output.json")

    os.system(sys.argv[2] + " -Tpng " + sys.argv[1] + " -o output.png")
    os.system(sys.argv[2] + " -Tjson " + sys.argv[1] + " -o output.json")
    output = json.load(open('output.json'))
    position = {}
    for e in output["objects"]:
        x, y = e["pos"].split(",")
        position[e["name"]] = (float(x), float(y))
    return transform_position_to_manim(position)
    
            
# Get the adjacency_list
adjacency_list, is_directed = get_adjacency_list(sys.argv[1])
print("adjacency_list", adjacency_list)

# Get the position
position = get_position()
print("position", position)

# Comment out to get position only
# # Call manim
# scene = GraphAlgorithm(adjacency_list, position, is_directed)
# scene.construct()

# # Use FFMPEG to combine partial videos      
# scene.renderer.scene_finished(scene)  








