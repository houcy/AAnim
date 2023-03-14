# 🍓 Welcome to AAnim 🍓

## What AAnim is

A(lgorithm)Anim(ation) is a library for data structure and algorithms animation by using a Python library called Manim.

## Installing Dependencies

1. ManimCE: This library uses ManimCE (instead of ManimGL) To set up the environment, follow [this tutorial](https://docs.manim.community/en/stable/installation.html).

2. Graphviz: If you are generating graph algorithms (vs. heap), you need to install graphviz [here](https://pypi.org/project/graphviz/) or [here](https://graphviz.org/download/)

3. Clone the code to your local environment. Make sure you are on the main branch.

## Validation

After installing, `cd source` and try `manim graph.py Test -ql`, if you see a video generared in a few seconds, you are good to go.

## How to use AAnim

You will need to `cd source` first. I made a [video](https://www.youtube.com/watch?v=Z6ImIFlK3tw) explaining what AAnim is in details. Starting at 4:02 there is a demo on how users interact with the tool to give you a more concrete idea of how it works. The instructions below are equivalent.

### Option 1: Animate a Heap

Heap operations that we currently support are build a heap, insert, and delete. Use the following default command to try: `python animate_heap.py command_heap.txt`

You can also customize your command in command_heap.txt. Please follow the following format strictly. It can take any combination of the following four commands:

1. Create a heap by giving a list of numbers less than 15 elements, seperated by space. This command always need to be the first one and no duplicates. For example: `19 18 17 16 15 14 13 12 11`
2. Build a heap: build [min/max]. For example: `build min`
3. Extract the Min/Max: extract.
4. Insert a value and heapify: insert [integer]. For example: `insert 1`

### Option 2: Animate a Graph

We use the layout engine from [Graphviz](https://graphviz.org) to get an optimized layout of a graph so you don't have to input the layout information.

1. Create a `.gv` file that describes all edges of the graph that you want to create. An example is `graph_blueprint.gv`. You need to follow the exact format to list out each edge as below:

   - 1a) For an un-weighted undirected graph:

   ```
   graph G {      # You can't modify the first line
   A -- B         # Use A -- B to represent an undirected edge
      B -- C      # Indentation is allowed but not encouraged
   C -- A
   C -- D
   Z              # An isolated node
   }              # You can't modify the last line
   ```

   - 1b) For an un-weighted directed graph:

   ```
   digraph G {    # Use digraph instead of graph
   A -> B         # Use A -> B to represent a directed edge.
   B -> C
   C -> A
   C -> D
   }
   ```

   - 1c) For a weighted unidrected graph:

   ```
   graph G {
   A -- B [xlabel=4]    # Add [xlabel=your_weight] at the end, the weight should be an integer
   B -- C [xlabel=5]
   C -- A [xlabel=2]
   C -- D [xlabel=3]
   }
   ```

2. Enter your command on termimal. The format of the command is: `python animate_graph.py [a) .gv file] [b) an algorithm] [c) source node]`. For example, `python animate_graph.py graph_blueprint.gv prim`.

   - 2a) [.gv file]: Required. The name of the .gv file you just created in step 1.
   - 2b) [an algorithm]: Required. The name of the algorithm you want to run on this graph. You can choose one from:
     - `bfs`, try `python animate_graph.py graph_blueprint4.gv bfs A`
     - `dfs`, try `python animate_graph.py graph_blueprint4.gv dfs A`
     - `prim-basic`, try `python animate_graph.py graph_blueprint3.gv prim-basic`
     - `prim`, try `python animate_graph.py graph_blueprint3.gv prim`
     - `kruskal-basic`, try ``python animate_graph.py graph_blueprint3.gv kruskal-basic`
     - `kruskal`, try `python animate_graph.py graph_blueprint3.gv kruskal`
     - `dijkstra`, try `python animate_graph.py graph_blueprint6.gv dijkstra A`
     - `bellmanford`, try `python animate_graph.py graph_blueprint6.gv bellmanford A`
   - 2c) [source node]: Optional. If you choose `bfs`, `dfs`, `dijkstra` or `bellmanford`, this argument is required. If you choose `kruskal-basic` or `kruskal`, the argument is not allowed. For other algorithms, the argument is optional.

A image, `output.png`, will be generated in about 3 seconds in `source` directory just in case you are curious what the graph look like after position being calculated.

WIP: We are working on a new feature to enable you to specify a layout engine among `dot`, `neato`, `twopi`, `circo`, `fdp`, `osage`, `sfdp`, which are supported by Graphviz. It's not implemented yet.

We thank you for choosing AAnim! If you have any suggestions or comments, feel free to contact Joy: zhuozhuo530[at]gmail.

## Resources

[SIGCSE 2023: Proceedings of the 54th ACM Technical Symposium on Computer Science Education](https://dl.acm.org/doi/abs/10.1145/3545947.3576233)
[Video explaining what AAnim is](https://www.youtube.com/watch?v=Z6ImIFlK3tw)
