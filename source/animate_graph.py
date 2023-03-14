import os
import json
import sys
from style import *
from collections import defaultdict
from graph_algorithm import GraphAlgorithm


def get_adjacency_list(file_name):
    is_directed = False
    adjacency_list = defaultdict(dict)
    with open(file_name) as f:
        if ">" in f.read():
            is_directed = True
    with open(file_name) as f:
        contents = f.readlines()
        for line in contents[1:-1]:
            line = line.strip("\n").strip().replace(" ", "")
            start, end = "", ""
            i = 0
            while i < len(line) and line[i].isalnum():
                start += line[i]
                i+=1
            i+=2
            while i < len(line) and line[i].isalnum():
                end += line[i]
                i+=1
            weight = ""
            if "xlabel" in line:
                i+=8
            while i < len(line) and line[i].isalnum():
                weight += line[i]
                i+=1
            if weight:
                adjacency_list[start][end] = int(weight)
            else:
                adjacency_list[start][end] = None
            if not is_directed:
                if weight:
                    adjacency_list[end][start] = int(weight)
                else:
                    adjacency_list[end][start] = None
    return adjacency_list, is_directed

def scale_position_to_fit(position):
    # Scale position numbers so that it fits in the canvas
    max_x, max_y= 0, 0
    for e in position:
        x, y = position[e]
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    ratio = max(max_x/FINAL_LENGTH, max_y/FINAL_LENGTH)   # Change denominators here to adjust the size of the graph
    new_position = {}
    for e in position:
        x, y = position[e]
        new_position[e] = (x/ratio, y/ratio)
    return new_position

def get_position():
    '''
    The command line should be: python animate_graph.py [.gv file] [algo: prim/kruskal/...]
    An example command: python animate_graph.py graph_blueprint.gv prim
    '''
    os.system("sfdp -Tpng " + sys.argv[1] + " -o output.png")   # Generate output.png in this dir
    os.system("sfdp -Tjson " + sys.argv[1] + " -o output.json") # Generate output.json in this dir

    output = json.load(open('output.json'))
    position = {}
    for e in output["objects"]:
        x, y = e["pos"].split(",")
        position[e["name"]] = (float(x), float(y))
    return scale_position_to_fit(position)


### Main starts here
if len(sys.argv) < 3:
    print("Error: the command is not correct")
graph_blueprint, algo_command = sys.argv[1], sys.argv[2]
# Get the adjacency_list
adjacency_list, is_directed = get_adjacency_list(graph_blueprint)
print("Adjacency list", dict(adjacency_list))

# Get the position
position = get_position()
print("Optimized position", position)
print("A `output.png` file has been generated. If you are curious what the graph look like, find it in `source` directory.")

# Get source (if any, optional)
source = None
if len(sys.argv) > 3:
    source = sys.argv[3]

# Comment out to get position only
# Call manim to generate partial video clips (in high resolution)
scene = GraphAlgorithm(adjacency_list, position, is_directed, source)
scene.construct(algo_command)

# Call FFMPEG to combine video clips     
scene.renderer.scene_finished(scene)