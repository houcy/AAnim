from manim import *
from style import *
from util import *
from graph_node import GraphNode
from graph_edge import GraphEdge
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from sub_graph import SubGraph


class GraphObject:
    def __init__(self, adjacency_list, position, is_topological_graph=False, edge_radius=RADIUS, edge_color=GRAY, node_radius=RADIUS, node_fill_color=BACKGROUND, node_stroke_color=GRAY, is_cyclic=False, font_color=GRAY, node_font_size=VALUE_SIZE, weight_font_size=WEIGHT_SIZE, zoom_in_power=1):
        self.mobject = VGroup()
        self.value2node = {}
        visited_edge = set()
        self.adjacency_list = adjacency_list
        self.edges = []
        self.position = position
        self.nodes2edge = {}
        for start in self.adjacency_list:
            if start not in self.value2node:
                position_x, position_y = position[start]
                self._create_node(start, position_x, position_y, node_radius, font_color=font_color, font_size=node_font_size, fill_color=node_fill_color, stroke_color = node_stroke_color, zoom_in_power=zoom_in_power)
            for end in self.adjacency_list[start]:
                if end not in self.value2node:
                    position_x, position_y = position[end]
                    self._create_node(end, position_x, position_y, node_radius, font_color=font_color, font_size=node_font_size, fill_color=node_fill_color, stroke_color = node_stroke_color, zoom_in_power=zoom_in_power)
                is_directed = True
                not_created = True
                # Not directed
                if end in self.adjacency_list and start in self.adjacency_list[end]:
                    is_directed = False
                    if (end, start) in visited_edge:
                        not_created = False
                if is_directed or (not is_directed and not_created):
                    self._create_edge(start, end, is_directed, is_topological_graph, edge_radius, edge_color, is_cyclic=is_cyclic, weight_font_size=weight_font_size, zoom_in_power=zoom_in_power)
                    visited_edge.add((start, end))
        self.mobject = self.mobject.move_to(ORIGIN)
        self.sub_graph_dict = {}

    def show(self, x_offset=0, y_offset=0):
        return FadeIn(self.mobject.shift(RIGHT*x_offset+UP*y_offset))

    def get_node_names(self):
        return list(self.value2node.keys())

    def get_node_by_name(self, node_name):
        return self.value2node[node_name]

    def get_edges(self):
        return self.edges

    def get_edges_duplicate(self):
        # For an undirected eedge, count it twice: start -> end, end -> start
        edges = self.get_edges()
        edges_with_duplicate = edges[:]
        for edge in edges:
            if not edge.is_directed:
                edge_object = GraphEdge(start_node=edge.end_node, end_node=edge.start_node, line_mobject=edge.mobject['line'], weight=edge.weight, is_directed=edge.is_directed)
                edges_with_duplicate.append(edge_object)
        return edges_with_duplicate

    def get_nodes(self):
        return list(self.value2node.values())

    def fade_in(self, x_offset=0, y_offset=0, scale=1):
        self.mobject.scale(scale).shift(x_offset*RIGHT+y_offset*UP)
        self.mobject.save_state()
        return FadeIn(self.mobject)

    def fade_out(self):
        return AnimationGroup(*[e.fade_out() for e in self.get_nodes() + self.get_edges()])

    def restore_graph(self):
        return Restore(self.mobject)
    
    def n_nodes(self):
        return len(self.value2node)

    def n_edges(self):
        return len(self.edges)
                
    def _create_node(self, value, position_x, position_y, node_radius, font_color, font_size, zoom_in_power, fill_color, stroke_color):
        node = GraphNode(value, position_x, position_y, node_radius=node_radius, font_color=font_color, fill_color=fill_color, stroke_color=stroke_color, font_size=font_size, zoom_in_power=zoom_in_power)
        self.value2node[value] = node
        self.mobject += node.mobject

    def get_edge(self, start_node, end_node):
        return self.nodes2edge[(start_node, end_node)]

    def get_edge_by_name(self, start, end):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        return self.get_edge(start_node, end_node)

    def get_edge_from_value(self, start_value, end_value):
        return self.nodes2edge[(self.value2node[start_value], self.value2node[end_value])]

    def _create_edge(self, start, end, is_directed, is_topological_graph, edge_radius, edge_color, is_cyclic=False, weight_font_size=WEIGHT_SIZE, zoom_in_power=1):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        weight = self.adjacency_list[start][end]
        # if start -> end && end -> strt, we need to use curved edges
        if end in self.adjacency_list and start in self.adjacency_list[end]:
            is_cyclic = True
        edge_object = GraphEdge(start_node=start_node, end_node=end_node, weight=weight, weight_font_size=weight_font_size, color=edge_color, is_cyclic=is_cyclic, is_directed=is_directed, is_topological_graph=is_topological_graph, edge_radius=4, zoom_in_power=zoom_in_power)
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
        self.mobject += edge_object.mobject

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

    def get_shortest_paths(self):
        path_edges = []
        for node in self.get_nodes():
            if node.min_edge:
                path_edges.append(node.min_edge)
        return set(path_edges)

    def get_mst_edges(self):
        def extract_min_node(list):
            min_so_far = float('inf')
            min_node = None
            for n in list:
                if n.key < min_so_far:
                    min_so_far = n.key
                    min_node = n
            list.remove(min_node)
            return min_node
        edges = []
        unreached = self.get_nodes()
        for node in unreached:
            node.key = float('inf')
        source = self.get_nodes()[0]
        source.key = 0
        while unreached:
            min_node = extract_min_node(unreached)
            if min_node != source:
                edges.append(min_node.min_edge)
            for neighbor in min_node.neighbors:
                edge = self.get_edge(min_node, neighbor)
                if edge.weight < neighbor.key:
                    neighbor.key = edge.weight
                    neighbor.min_edge = edge
        return GraphEdgesGroup(edges)

    def get_mst_nodes(self):
        return GraphNodesGroup(self.get_nodes())

    def mst_highlight(self):
        mst_edges_group = self.get_mst_edges()
        mst_nodes_group = self.get_mst_nodes()
        return AnimationGroup(mst_edges_group.highlight(width=EDGE_HIGHLIGHT_STROKE_WIDTH), mst_nodes_group.fill())

    def shortest_path_highlight(self):
        nodes_list = self.graph.get_nodes()
        edges_list = None # Need to update - this is incorrect
        subgraph = SubGraph(edges_list, nodes_list)
        return subgraph.highlight(node_stroke_color=PINK3)
    
    def highlight(self, node_name, fill_color=PINK2, stroke_color=PINK3,  stroke_width=WIDTH, text_color=BACKGROUND):
        node = self.value2node[node_name]        
        return node.color(fill_color=fill_color, stroke_color=stroke_color, stroke_width=stroke_width, text_color=text_color)

    def shift(self, x_offset=0, y_offset=0):
        return self.mobject.animate.shift(x_offset*RIGHT + y_offset*UP)

    def save_state(self):
        self.mobject.save_state()

    def restore(self):
        return Restore(self.mobject)

    def create_sub_graph(self, name, edge_list):
        """
        edge_list example: [('A', 'B'), ('C', 'D')]
        """
        edges = []
        nodes = []
        for start, end in edge_list:
            edges.append(self.get_edge_by_name(start, end))
            start_node = self.get_node_by_name(start)
            end_node = self.get_node_by_name(end)
            if start_node not in nodes:
                nodes.append(start_node)
            if end_node not in nodes:
                nodes.append(end_node)
        self.sub_graph_dict[name] = SubGraph(edges_list=edges, node_list=nodes)
        return self.sub_graph_dict[name]
        


class Test(Scene):
    def construct(self):
        # For Testing
        MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
        MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
        MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
        MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
        POSITION1 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}
        POSITION_CYCLE = {'A': (-1, -1), 'B': (1, 1)}
        POSITION_CYCLE2 = {'A': (-0.5, -0.5), 'B': (0.5, 0.5)}
        POSITION_CYCLE3 = {'A': (-2, -2), 'B': (2, 2)}
        MAP_CYCLE = {'A': {'B': 3}, 'B': {'A': 2}}
        position = scale_position(POSITION1, 1.5, 1.5)
        self.camera.background_color = BACKGROUND
        graph = GraphObject(MAP_UNDIRECTED, position)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))
        graph = GraphObject(MAP_DIRECTED, position)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))
        graph = GraphObject(MAP_UNDIRECTED_WEIGHT, position)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))
        graph = GraphObject(MAP_CYCLE, POSITION_CYCLE)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))
        graph = GraphObject(MAP_CYCLE, POSITION_CYCLE2)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))
        graph = GraphObject(MAP_CYCLE, POSITION_CYCLE3)
        self.add(graph.mobject)
        self.play(FadeOut(graph.mobject))