# manim-cs

## Description

This is a library for data structure animation by using a Python library called Manim.

## Installation

This library uses ManimCE (instead of ManimGL, learn differences between versions [here](https://docs.manim.community/en/stable/installation/versions.html)) To set up the environment, follow [this tutorial](https://docs.manim.community/en/stable/installation.html)

Also, you need to enable LaTeX, go and download the full version of [MacTeX](http://www.tug.org/mactex/).

## Validation

After installing, `cd practice` and try `manimgl make_image.py SquareToCircle`, if you see a window pop up which renders a blue circle, you are good to go.

## Working demo

You will need to `cd practice` first.

### Animate Heap

Heap operations that we currently support are build a heap, insert, and delete. Use the following default command to try: `python animate_heap.py command_heap.txt`

You can also customize your command in command_heap.txt. Please follow the following format strictly. It can take any combination of the following four commands:

1. Create a heap by giving a list of numbers less than 15 elements, seperated by space. This command always need to be the first one and no duplicates. For example: `19 18 17 16 15 14 13 12 11`
2. Build a heap: build [min/max]. For example: `build min`
3. Extract the Min/Max: extract.
4. Insert a value and heapify: insert [integer]. For example: `insert 1`

### Animate Graph

Graph operations that we currently support is to build a graph, dfs. Use the following default command to try: `python animate_graph.py graph_blueprint.gv`

You can also customize the blueprint of the graph in graph_blueprint.gv. Please follow the following format strictly. Check out [Graphviz](https://graphviz.org) to know more about this format.

```
graph G {      # You can't modify the first line
A -- B         # Use A -- B to represent an undirected edge, or A -> B to represent a directed edge.
   B -- C      # Indentation doesn't matter
C -- A
C -- D
}              # You can't modify the last line
```
