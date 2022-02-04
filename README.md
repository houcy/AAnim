# manim-cs

## Description

This is a library for data structure animation by using a Python library called Manim.

## Installation

This library uses ManimCE (instead of ManimGL, learn differences between versions [here](https://docs.manim.community/en/stable/installation/versions.html)) To set up the environment, follow [this tutorial](https://docs.manim.community/en/stable/installation.html)

Also, you need to enable LaTeX, go to http://www.tug.org/mactex/ and download the full version of MacTeX.

## Validation

After installing, `cd practice` and try `manimgl make_image.py SquareToCircle`, if you see a window pop up which renders a blue circle, you are good to go.

## Working demo

You will need to `cd practice` first.

### Animate Heap

Heap operations that we currently support are build a heap, insert, and delete. Use the following default command to try: `python animate_heap.py command_heap.txt`

You can also customize your commands in commands.txt. It only takes one of the four commands:

1. Create a heap by giving a list of numbers less than 15 elements, seperated by space. For example: `19 18 17 16 15 14 13 12 11`
2. Build a heap: build [min/max]. For example: `build min`
3. Extract the Min/Max: extract.
4. Insert a value and heapify: insert [integer]. For example: `insert 1`

Please follow the format strictly.

### Animate Graph

Graph operations that we currently support is to build a graph, dfs. Use the following default command to try: `python animate_graph.py graph_blueprint.gv`

You can also customize the blueprint of the graph in graph_blueprint.gv. It has to follow the following format. Check [Graphviz](https://graphviz.org) to know more about this format.

graph G { # You can't modify the first line
A -- B # You can use A -- B to represent an undirected edge AB, or A -> B to represent a directed edge AB. It doesn't matter if there are aditional spaces.
B -- C
C -- A
C -- D
C -- E
C -- F
D -- F
E -- F
} # You can't modify the last line
