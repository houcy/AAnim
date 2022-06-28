from manim import *
from style import *
from graph_node import GraphNode
from graph_edge import GraphEdge

# For Testing
# Limit input to:
# Directed:
# {'A': {'B': 3}, 'B': {'A': 2}}
# Undirected:
# {'A': {'B': 3}, 'B': {'A': 3}}
MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
POSITION1 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

POSITION_CYCLE = {'A': (-1, -1), 'B': (1, 1)}
POSITION_CYCLE2 = {'A': (-0.5, -0.5), 'B': (0.5, 0.5)}
POSITION_CYCLE3 = {'A': (-2, -2), 'B': (2, 2)}

MAP_CYCLE = {'A': {'B': 3}, 'B': {'A': 2}}

class GraphObject:
    def __init__(self, adjacency_list, position, is_topological_graph=False, edge_radius=RADIUS, node_radius=RADIUS, is_cyclic=False):
        self.graph_mobject = VGroup()
        self.value2node = {}
        visited_edge = set()
        self.adjacency_list = adjacency_list
        self.edges = []
        self.position = position
        self.nodes2edge = {}
        for start in self.adjacency_list:
            if start not in self.value2node:
                position_x, position_y = position[start]
                self._create_node(start, position_x, position_y, node_radius)
            for end in self.adjacency_list[start]:
                if end not in self.value2node:
                    position_x, position_y = position[end]
                    self._create_node(end, position_x, position_y, node_radius)
                is_directed = True
                not_created = True
                # Not directed
                if end in self.adjacency_list and start in self.adjacency_list[end]:
                    is_directed = False
                    if (end, start) in visited_edge:
                        not_created = False
                if is_directed or (not is_directed and not_created):
                    self._create_edge(start, end, is_directed, is_topological_graph, edge_radius, is_cyclic=is_cyclic)
                    visited_edge.add((start, end))
        self.graph_mobject = self.graph_mobject.move_to(ORIGIN)

    def show(self, x_offset=0, y_offset=0):
        return FadeIn(self.graph_mobject.shift(RIGHT*x_offset+UP*y_offset))

    def get_node_names(self):
        return list(self.value2node.keys())

    def get_edges_no_duplicate(self):
        return self.edges

    def get_edges_duplicate(self):
        # For an undirected eedge, count it twice: start -> end, end -> start
        pass

    def get_nodes(self):
        return list(self.value2node.values())

    def fade_in(self, graph_scale=1, x_offset=0, y_offset=0):
        return FadeIn(self.graph_mobject.scale(graph_scale).shift(x_offset*RIGHT+y_offset*UP))

    def fade_out(self):
        return AnimationGroup(*[e.fade_out() for e in self.get_nodes() + self.get_edges()])
    
    def n_nodes(self):
        return len(self.value2node)

    def n_edges(self):
        return len(self.edges)
                
    def _create_node(self, value, position_x, position_y, node_radius):
        node = GraphNode(value, position_x, position_y, node_radius=node_radius)
        self.value2node[value] = node
        self.graph_mobject += node.mobject

    def get_edge(self, start, end):
        return self.nodes2edge[(start, end)]

    def get_edge_from_value(self, start_value, end_value):
        return self.nodes2edge[(self.value2node[start_value], self.value2node[end_value])]

    def _create_edge(self, start, end, is_directed, is_topological_graph, edge_radius, is_cyclic=False):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        weight = self.adjacency_list[start][end]
        # if start -> end && end -> strt, we need to use curved edges
        if end in self.adjacency_list and start in self.adjacency_list[end]:
            is_cyclic = True
        edge_object = GraphEdge(start_node=start_node, end_node=end_node, weight=weight, is_cyclic=is_cyclic, is_directed=is_directed, is_topological_graph=is_topological_graph, edge_radius=4)
        start_node.neighbor2edge[end_node] = edge_object
        start_node.neighbors.append(end_node)
        start_node.edges.append(edge_object)
        self.edges.append(edge_object)
        self.nodes2edge[(start_node, end_node)] = edge_object
        # for undirected graph, mark the edge on end -> start as well
        if not is_directed:
            end_node.neighbor2edge[start_node] = edge_object
            end_node.neighbors.append(start_node)
            end_node.edges.append(edge_object)
            self.nodes2edge[(end_node, start_node)] = edge_object
        self.graph_mobject += edge_object.mobject

    def get_path(self, start, end, visited_edges=None):
        def helper(curr, end, path, visited, depth):
            if curr in visited:
                return False
            visited.add(curr)
            if curr == end and depth > 1:
                return True
            for edge in curr.edges:
                if visited_edges and edge in visited_edges:
                    neighbor_node = edge.get_the_other_end(curr)
                    path.append(edge)
                    if helper(neighbor_node, end, path, visited, depth+1):
                        return True
                    path.pop()
            return False
        path = []
        visited = set()
        helper(start, end, path, visited, 0)
        return path
    
    def highlight(self, node_name, fill_color=PINK2, stroke_color=PINK3,  stroke_width=WIDTH, text_color=BACKGROUND):
        node = self.value2node[node_name]        
        return node.color(fill_color=fill_color, stroke_color=stroke_color, stroke_width=stroke_width, text_color=text_color)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        # graph = Graph(MAP_UNDIRECTED, POSITION1, is_directed=False)
        # self.add(graph.graph_mobject)
        # self.play(FadeOut(graph.graph_mobject))
        # graph = Graph(MAP_DIRECTED, POSITION1, is_directed=True)
        # self.add(graph.graph_mobject)
        # self.play(FadeOut(graph.graph_mobject))
        # graph = Graph(MAP_UNDIRECTED_WEIGHT, POSITION1, is_directed=False)
        # self.add(graph.graph_mobject)
        # self.play(FadeOut(graph.graph_mobject))
        # graph = Graph(MAP_DIRECTED_WEIGHT, POSITION1, is_directed=True)
        # self.add(graph.graph_mobject)
        # self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_CYCLE, POSITION_CYCLE, is_directed=True)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_CYCLE, POSITION_CYCLE2, is_directed=True)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_CYCLE, POSITION_CYCLE3, is_directed=True)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
    