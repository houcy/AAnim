from re import X
from manim import *
from style import *
from code_constant import *
from graph import GraphObject
from code_block import CodeBlock
from legend import Legend
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *
from union_find import UnionFind
from color_generator import ColorGenerator
from sub_graph import SubGraph
import copy

MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
BFS_POSITION = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

# MST
MAP_MST = {'A': {'B': 4, 'H': 8}, 'B': {'A': 4, 'C': 8, 'H': 11}, 'H': {'A': 8, 'B': 11, 'G': 1, 'I': 7}, 'C': {'B': 8, 'D': 7, 'I': 2, 'F': 4}, 'D': {'C': 7, 'F': 14, 'E': 9}, 'I': {'C': 2, 'G': 6, 'H': 7}, 'F': {'C': 4, 'G': 2, 'D': 14, 'E': 10}, 'G': {'I': 6, 'F': 2, 'H': 1}, 'E': {'D': 9, 'F': 10}}
POSITION_MST = {'A': (0.7, 0.6), 'B': (1.4402327576560112, 2.1393785668991754), 'H': (2.5, -0.1), 'C': (2.9889216307956286, 3.1086575403782315), 'D': (4.368905964414935, 4.2), 'I': (3.082024693200045, 1.457062926629117), 'F': (4.744899101048156, 2.3), 'G': (4.4, 0.5), 'E': (6.0, 3.649819090603902)}

MAP_HARD = {'Src': {'B': 7, 'D': 8, 'G': 8}, 'B': {'Src': 7, 'C': 5, 'D': 6}, 'C': {'B': 5, 'D': 5, 'E': 7}, 'D': {'C': 5, 'E': 3, 'Src': 8, 'B': 6, 'F': 5, 'G': 9}, 'E': {'D': 3, 'F': 2, 'C': 7, 'N': 8, 'M': 6}, 'F': {'E': 2, 'G': 5, 'D': 5, 'M': 7}, 'G': {'F': 5, 'H': 5, 'Src': 8, 'D': 9, 'M': 6}, 'H': {'G': 5, 'I': 5, 'M': 9}, 'P': {'Q': 5, 'O': 5, 'K': 8}, 'Q': {'P': 5, 'R': 5, 'K': 6, 'T': 7}, 'I': {'H': 5, 'J': 3, 'M': 6, 'L': 6, 'K': 9}, 'J': {'I': 3, 'K': 5, 'U': 6, 'T': 6}, 'K': {'J': 5, 'L': 3, 'P': 8, 'O': 5, 'I': 9, 'Q': 6, 'T': 9, 'U': 6}, 'L': {'K': 3, 'M': 3, 'O': 9, 'I': 6}, 'M': {'L': 3, 'N': 3, 'E': 6, 'F': 7, 'G': 6, 'O': 8, 'H': 9, 'I': 6}, 'N': {'M': 3, 'O': 2, 'E': 8}, 'O': {'N': 2, 'P': 5, 'L': 9, 'M': 8, 'K': 5}, 'R': {'Q': 5, 'S': 2, 'T': 5}, 'S': {'R': 2, 'T': 6}, 'T': {'R': 5, 'U': 3, 'K': 9, 'J': 6, 'S': 6, 'Q': 7}, 'U': {'T': 3, 'K': 6, 'J': 6}}
POSITION_HARD = {'Src': (-4, -1), 'B': (-4, 0), 'C': (-4, 1), 'D': (-3, 0), 'E': (-2, 1), 'F': (-2, 0), 'G': (-2, -1), 'H': (-1, -1), 'I': (0, -1), 'J': (1, -1), 'K': (1, 0), 'L': (0, 0), 'M': (-1, 0), 'N': (-1, 1), 'O': (0, 1), 'P': (1, 1), 'Q': (2, 1), 'R': (3, 1), 'S': (4, 1), 'T': (3, 0), 'U': (3, -1)}

# DIJKSTRS
DIMAP_DIJKASTRA_CLRS = {'Src': {'B': 10, 'E': 5}, 'B': {'C': 1, 'E': 2}, 'C': {'D': 4}, 'D': {'C': 6}, 'E': {'C': 9, 'D': 2, 'B': 3}}
DIPOSITION_DIJKASTRA_CLRS = {'Src': (1, 2), 'B': (2, 1), 'E': (0, 1), 'C': (2, 0), 'D': (0, 0)}
MAP_HARD_DIJKSTRA = {'Src': {'B': 7, 'D': 8, 'G': 8}, 'B': {'Src': 7, 'C': 5, 'D': 6}, 'C': {'B': 5, 'D': 5, 'E': 7}, 'D': {'C': 5, 'E': 3, 'Src': 8, 'B': 6, 'F': 5, 'G': 9}, 'E': {'D': 3, 'F': 2, 'C': 7, 'N': 8, 'M': 6}, 'F': {'E': 2, 'G': 5, 'D': 5, 'M': 7}, 'G': {'F': 5, 'H': 5, 'Src': 8, 'D': 9, 'M': 6}, 'H': {'G': 5, 'I': 5, 'M': 9}, 'P': {'Q': 5, 'O': 5, 'K': 8}, 'Q': {'P': 5, 'R': 5, 'K': 6, 'T': 7}, 'I': {'H': 5, 'J': 3, 'M': 6, 'L': 6, 'K': 9}, 'J': {'I': 3, 'K': 5, 'U': 6, 'T': 6}, 'K': {'J': 5, 'L': 3, 'P': 8, 'O': 5, 'I': 9, 'Q': 6, 'T': 9, 'U': 6}, 'L': {'K': 3, 'M': 3, 'O': 9, 'I': 6}, 'M': {'L': 3, 'N': 3, 'E': 6, 'F': 7, 'G': 6, 'O': 8, 'H': 9, 'I': 6}, 'N': {'M': 3, 'O': 2, 'E': 8}, 'O': {'N': 2, 'P': 5, 'L': 9, 'M': 8, 'K': 5}, 'R': {'Q': 5, 'S': 2, 'T': 5}, 'S': {'R': 2, 'T': 6}, 'T': {'R': 5, 'U': 3, 'K': 9, 'J': 6, 'S': 6, 'Q': 7}, 'U': {'T': 3, 'K': 6, 'J': 6}}
POSITION_HARD_DIJKSTRA = {'Src': (-4, -1), 'B': (-4, 0), 'C': (-4, 1), 'D': (-3, 0), 'E': (-2, 1), 'F': (-2, 0), 'G': (-2, -1), 'H': (-1, -1), 'I': (0, -1), 'J': (1, -1), 'K': (1, 0), 'L': (0, 0), 'M': (-1, 0), 'N': (-1, 1), 'O': (0, 1), 'P': (1, 1), 'Q': (2, 1), 'R': (3, 1), 'S': (4, 1), 'T': (3, 0), 'U': (3, -1)}

MAP_DIJKSTRA_NEGATIVE_CH = {'始': {'B': 2, 'C': 1}, 'B': {'C': -100}}
POSITION_DIJKSTRA_NEGATIVE_CH = {'始': (0, 1.73), 'B': (-1, 0), 'C': (1, 0)}
MAP_DIJKSTRA_NEGATIVE_EN = {'Src': {'B': 2, 'C': 1}, 'B': {'C': -100}}
POSITION_DIJKSTRA_NEGATIVE_EN = {'Src': (0, 1.73), 'B': (-1, 0), 'C': (1, 0)}
MAP_TRIANGLE_NEGATIVE_CYCLE = {'Src': {'B': 2}, 'B': {'C': -100}, 'C': {'Src': 1}}
POSITION_TRIANGLE_NEGATIVE_CYCLE = {'Src': (0, 1.73), 'B': (-1, 0), 'C': (1, 0)}

# RELAX - SIMPLE
MAP_RELAX = {'u': {'v': 2}}
MAP_RELAX_UNDIRECTED = {'u': {'v': 2}, 'v': {'u': 2}}
POSITION_RELAX = {'u': (0, 0), 'v': (1, 0)}

# Square for comparing Prim and Dijkstra
MAP_SQUARE_1 = {
    'A': {'B': 1, 'D': 1, 'E': 1}, 
    'B': {'A': 1, 'E': 1, 'C': 1}, 
    'C': {'B': 1, 'E': 1, 'F': 1}, 
    'D': {'A': 1, 'E': 1, 'G': 1}, 
    'E': {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 1, 'E': 1, 'I': 1},
    'G': {'D': 1, 'E': 1, 'H': 1},
    'H': {'E': 1, 'G': 1, 'I': 1},
    'I': {'F': 1, 'E': 1, 'H': 1}
}
MAP_SQUARE_SRC_1 = {
    'Src': {'B': 1, 'D': 1, 'E': 1}, 
    'B': {'Src': 1, 'E': 1, 'C': 1}, 
    'C': {'B': 1, 'E': 1, 'F': 1}, 
    'D': {'Src': 1, 'E': 1, 'G': 1}, 
    'E': {'Src': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 1, 'E': 1, 'I': 1},
    'G': {'D': 1, 'E': 1, 'H': 1},
    'H': {'E': 1, 'G': 1, 'I': 1},
    'I': {'F': 1, 'E': 1, 'H': 1}
}
MAP_SQUARE_2 = {
    'A': {'B': 2, 'D': 2, 'E': 1}, 
    'B': {'A': 2, 'E': 1, 'C': 2}, 
    'C': {'B': 2, 'E': 1, 'F': 2}, 
    'D': {'A': 2, 'E': 1, 'G': 2}, 
    'E': {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 2, 'E': 1, 'I': 2},
    'G': {'D': 2, 'E': 1, 'H': 2},
    'H': {'E': 1, 'G': 2, 'I': 2},
    'I': {'F': 2, 'E': 1, 'H': 2}
}
MAP_SQUARE_SRC_2 = {
    'Src': {'B': 2, 'D': 2, 'E': 1}, 
    'B': {'Src': 2, 'E': 1, 'C': 2}, 
    'C': {'B': 2, 'E': 1, 'F': 2}, 
    'D': {'Src': 2, 'E': 1, 'G': 2}, 
    'E': {'Src': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 2, 'E': 1, 'I': 2},
    'G': {'D': 2, 'E': 1, 'H': 2},
    'H': {'E': 1, 'G': 2, 'I': 2},
    'I': {'F': 2, 'E': 1, 'H': 2}
}
MAP_SQUARE_3 = {
    'A': {'B': 3, 'D': 3, 'E': 1}, 
    'B': {'A': 3, 'E': 1, 'C': 3}, 
    'C': {'B': 3, 'E': 1, 'F': 3}, 
    'D': {'A': 3, 'E': 1, 'G': 3}, 
    'E': {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 3, 'E': 1, 'I': 3},
    'G': {'D': 3, 'E': 1, 'H': 3},
    'H': {'E': 1, 'G': 3, 'I': 3},
    'I': {'F': 3, 'E': 1, 'H': 3}
}
MAP_SQUARE_SRC_3 = {
    'Src': {'B': 3, 'D': 3, 'E': 1}, 
    'B': {'Src': 3, 'E': 1, 'C': 3}, 
    'C': {'B': 3, 'E': 1, 'F': 3}, 
    'D': {'Src': 3, 'E': 1, 'G': 3}, 
    'E': {'Src': 1, 'B': 1, 'C': 1, 'D': 1, 'F': 1, 'G': 1, 'H': 1, 'I': 1}, 
    'F': {'C': 3, 'E': 1, 'I': 3},
    'G': {'D': 3, 'E': 1, 'H': 3},
    'H': {'E': 1, 'G': 3, 'I': 3},
    'I': {'F': 3, 'E': 1, 'H': 3}
}
POSITION_SQUARE = {'A': (-1, 1), 'B': (0, 1), 'C': (1, 1), 'D': (-1, 0), 'E': (0, 0), 'F': (1, 0), 'G': (-1, -1), 'H': (0, -1), 'I': (1, -1)}
POSITION_SQUARE_SRC = {'Src': (-1, 1), 'B': (0, 1), 'C': (1, 1), 'D': (-1, 0), 'E': (0, 0), 'F': (1, 0), 'G': (-1, -1), 'H': (0, -1), 'I': (1, -1)}

# Double square for bellman-ford
MAP_DOUBLE_SQUARE = {
    'F': {'E': 1},
    'D': {'E': 4, 'F': 3, 'C': 1},
    'B': {'C': 3, 'D': 2},
    'Src': {'B': 1, 'F': 7, 'D': 4},
}
POSITION_DOUBLE_SQUARE = {
    'Src': (1, 1),
    'B': (0, 1),
    'C': (0, 0),
    'D': (1, 0),
    'E': (2, 0),
    'F': (2, 1),
}

MAP_6_NODES_HORIZONTAL = {'E': {'F': 1}, 'D': {'E': 1}, 'C': {'D': 1}, 'B': {'C': 1}, 'Src': {'B': 1}, }
POSITION_6_NODES_HORIZONTAL = {'Src': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0), 'E': (4, 0), 'F': (5, 0)}

FAIRYTALE_POSITION = {'A': (0, 0), 'B': (1, 1), 'C': (2, 0), 'D': (1, -1), 'E': (3, 1), 'F': (3, -1), 'G': (4, 0)}
FAIRYTALE_MAP = {
    'A': {'B': 4, 'D': 8}, 
    'B': {'A': 4, 'C': 7, 'D': 9, 'E': 10}, 
    'C': {'B': 7, 'E': 7, 'D': 2, 'F': 10},
    'D': {'A': 8, 'B': 9, 'C': 2, 'F': 1},
    'E': {'B': 10, 'C': 7, 'F': 5, 'G': 6},
    'F': {'C': 10, 'D': 1, 'E': 5, 'G': 2},
    'G': {'E': 6, 'F': 2}
}

FAIRYTALE_POSITION = {'E': (0, 0), 'B': (0, 1), 'C': (1, 1), 'F': (1, 0), 'A': (1, 2), 'D': (2, 1), 'G': (2, 0)}
FAIRYTALE_MAP = {
    'A': {'B': 11, 'C': 6, 'D': 5},
    'B': {'E': 4, 'C': 7, 'F': 9, 'A': 11}, 
    'C': {'B': 7, 'A': 6, 'F': 2, 'D': 12},
    'D': {'C': 12, 'F': 1, 'A': 5, 'G': 3},
    'E': {'B': 4, 'F': 8}, 
    'F': {'E': 8, 'B': 9, 'C': 2, 'D': 1, 'G': 10},
    'G': {'F': 10, 'D': 3}
}


class GraphAlgorithm(MovingCameraScene):
    # Comment out code for testing
    # def __init__(self, adjacency_list, position, is_directed):
    #     self.adjacency_list = adjacency_list
    #     self.position = position
    #     self.is_directed = is_directed
    #     super().__init__()

    def _remove_edges(self, graph, selected_edges, speed=0.5, is_sync=False):
        animations = []
        for edge in graph.edges:
            if edge not in selected_edges:
                if not is_sync:
                    self.play(edge.fade_out(), run_time=speed)
                else:
                    animations.append(edge.fade_out())
        if is_sync:
            self.play(*animations)

    def _restore_edges(self, graph, selected_edges, speed=1, is_sync=False):
        animations = []
        for edge in graph.edges:
            if edge not in selected_edges:
                if not is_sync:
                    self.play(edge.fade_in(), run_time=speed)
                else:
                    animations.append(edge.fade_in())
        if is_sync:
            self.play(*animations)

    def _fade_out_key_restore_names(self, node_list, color=BACKGROUND):
        animations = []
        for node in node_list:
            animations.append(node.fade_out_key_restore_name(color=color))
        self.play(*animations)

    def flash(self, temp_group):
        self.play(*[m.animate.set_color(BACKGROUND) for m in temp_group])
        self.play(*[m.animate.set_color(GRAY) for m in temp_group])

    # def show_only(self, concepts_map, mobject_to_keep):
    #     # all is a list of mobjects
    #     animations = []
    #     for e in concepts_map:
    #         if e not in mobject_to_keep:
    #             animations.append(FadeOut(e))
    #     return AnimationGroup(*animations)
    # def show_all(self, concepts_map, mobject_to_keep):
    #     # all is a list of mobjects
    #     animations = []
    #     for e in concepts_map:
    #         if e not in mobject_to_keep:
    #             animations.append(FadeIn(e))
    #     return AnimationGroup(*animations)   
    
    ##################################
    # DFS
    ##################################

    # Option 2 to implement topo
    def _dfs_helper(self, graph, l, node, discovered, code_block, post_order, topo_value2node):
        # self.play(code_block.highlight(7))
        discovered.add(node)
        # self.play(code_block.highlight(8))
        self.play(node.mark_pink1())
        # self.play(code_block.highlight(9))
        for neighbor in node.neighbor2edge:
            # self.play(code_block.highlight(10))
            if neighbor not in discovered:
                self.play(neighbor.highlight_stroke())
                # self.play(code_block.highlight(11))
                self.play(node.mark_line_pink1(neighbor))
                self.play(node.highlight_stroke(PINK1))
                self._dfs_helper(graph, l, neighbor, discovered, code_block, post_order, topo_value2node)
                self.play(node.highlight_stroke())
                self.play(node.mark_line_blue1(neighbor))
        # self.play(code_block.highlight(12))
        self.play(node.mark_blue1())
        self.play(node.highlight_stroke(BLUE1))
        if node not in post_order:
            topo_node = copy.deepcopy(node)
            topo_node.mark_blue1()
            if not post_order:
                self.play(l.mobjects.animate.shift(UP), graph.mobject.animate.shift(1 * UP))
                topo_node.mobject.to_edge(DR, buff=1.5)
            else:
                topo_node.mobject.next_to(post_order[0].mobject, LEFT, buff=0.5)
            topo_value2node[topo_node.value] = topo_node
            self.play(Create(topo_node.mobject))
            post_order.insert(0, topo_node)

    def dfs(self, graph, show_topological_sort=False):
        """
        DFS on the graph to traver every node
        """
        code_block = CodeBlock(CODE_FOR_DFS)
        self.add(code_block.code)
        discovered = set()
        post_order = []
        topo_value2node = {}
        l = Legend({PINK1: "discovered", BLUE1: "finished"})
        l.mobjects.next_to(graph.mobject, RIGHT, buff=0.5)
        self.play(l.animation)
        # self.play(code_block.highlight(1))
        for curr in graph.value2node:
            # self.play(code_block.highlight(2))
            node = graph.value2node[curr]
            # self.play(code_block.highlight(3))
            if node not in discovered:
                # self.play(code_block.highlight(4))
                self.play(node.highlight_stroke())
                self._dfs_helper(graph, l, node, discovered, code_block, post_order, topo_value2node)
                node.highlight_stroke(LINE_COLOR)
        # self.play(code_block.highlight(5))
        self.play(FadeOut(code_block.code, l.mobjects))
        if show_topological_sort:
            _, graph_y, _ = graph.mobject.get_center()
            topo_vgroup = VGroup()
            for node in post_order:
                topo_vgroup += node.mobject
            _, topo_y, _ = topo_vgroup.get_center()
            self.play(graph.mobject.animate.move_to(graph_y * UP), topo_vgroup.animate.move_to(topo_y * UP))
            # draw lines on topological sort graph
            topo_edges = VGroup()
            for start_node in post_order:
                if start_node.value in graph.adjacency_list:
                    for end_value in graph.adjacency_list[start_node.value]:
                        end_node = topo_value2node[end_value]
                        line = CurvedArrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH).set_z_index(0)
                        topo_vgroup += line
                        topo_edges += line
            self.play(FadeIn(topo_edges))
        self.wait(2)
        self.play(FadeOut(topo_vgroup, graph.mobject))

    ##################################
    # BFS
    ##################################

    # Mirror DFS on coloring (same with CLRS) doesn't look very clear so comment out
    # def bfs(self, graph, s):
    #     """
    #     BFS: mark 2 colors for discovered, and finished
    #     """
        # code_block = CodeBlock(CODE_FOR_BFS)
        # self.add(code_block)
    #     discovered = set()
    #     queue = []
    #     s_node = graph.value2node[s]
    #     queue.append(s_node)
    #     discovered.add(s_node)
    #     self.play(s_node.mark_pink1())
    #     while queue:
    #         curr = queue.pop(0)
    #         for neighbor in curr.neighbor2edge:
    #             if neighbor not in discovered:
    #                 queue.append(neighbor)
    #                 discovered.add(curr)
    #                 self.play(neighbor.mark_pink1())
    #         self.wait(1)
    #         self.play(curr.mark_pink1())

    def mark_levels(self, level, color):
        animation = []
        for node in level:
            animation.append(node.mobject["c"].animate.set_fill(color).set_stroke(color))
            animation.append(node.mobject["t"].animate.set_color(BACKGROUND))
        return AnimationGroup(*animation)
    
    def bfs(self, graph, s, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
        """
        BFS: traverse the tree starting from source s. 
        Mark 3 colors for curr level, next level, and finished
        """
        speed = 1 / speed
        if create_legend:
            l = Legend({(PINK1, PINK1): "curr level", (PINK3, PINK3): "next level", (BLUE1, BLUE1): "finished"})
            l.mobjects.next_to(graph.mobject, RIGHT, buff=0.5)
            self.play(l.animation)
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE2_FOR_BFS)
            self.add(code_block.code)
        self.play(code_block.highlight(1)) if animate_code_block else None
        discovered = set()
        s_node = graph.value2node[s]
        curr_level = []
        next_level = []
        self.play(code_block.highlight(2)) if animate_code_block else None
        curr_level.append(s_node)
        self.play(code_block.highlight(3)) if animate_code_block else None
        discovered.add(s_node)
        self.play(code_block.highlight(4)) if animate_code_block else None
        self.play(s_node.mark_pink1())
        while curr_level:
            self.play(code_block.highlight(5)) if animate_code_block else None
            for curr in curr_level:
                self.play(code_block.highlight(6)) if animate_code_block else None
                self.play(curr.highlight_stroke())
                for neighbor in curr.neighbor2edge:
                    self.play(code_block.highlight(7)) if animate_code_block else None
                    if neighbor not in discovered:
                        self.play(code_block.highlight(8)) if animate_code_block else None
                        next_level.append(neighbor)
                        self.play(code_block.highlight(9)) if animate_code_block else None
                        discovered.add(curr)
                        self.play(code_block.highlight(10)) if animate_code_block else None
                        self.play(neighbor.mark_pink3())
                self.play(curr.highlight_stroke(PINK1))
                self.wait(1)
                self.play(code_block.highlight(11)) if animate_code_block else None
                self.play(curr.mark_blue1())
            self.play(code_block.highlight(12)) if animate_code_block else None
            # self.play(self.mark_levels(curr_level, BLUE1))
            curr_level = next_level
            self.play(code_block.highlight(13)) if animate_code_block else None
            self.play(self.mark_levels(curr_level, PINK1))
            next_level = []
            self.play(code_block.highlight(14)) if animate_code_block else None
        self.play(code_block.highlight(15)) if animate_code_block else None

    ##################################
    # MST: Prim
    ##################################

    def mst_prim_basic(self, graph, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1):
        speed = 1 / speed
        if create_legend:
            l = Legend({PINK2: "MST so far"}, is_horizontal=show_horizontal_legend)
            l.mobjects.move_to(1.6*UP+1.7*RIGHT)
            self.play(l.animation)
            self.wait()
        # l.mobjects.next_to(graph.mobject, DOWN, buff=0.3)
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
            self.play(Create(code_block.code))
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        selected_edges = set()
        selected = set()
        first_node_key = list(graph.adjacency_list.keys())[0]
        first_node = graph.value2node[first_node_key]
        self.play(code_block.highlight(2, 3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        selected.add(first_node)
        self.play(first_node.color(fill_color=PINK4), run_time=speed)
        while len(selected) != len(graph.adjacency_list):
            self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            self.play(code_block.if_true()) if animate_code_block else None
            minimum = float("inf")
            minimum_node = None
            minimum_edge = None
            for v in selected:
                for e in v.edges:
                    u = e.get_the_other_end(v)
                    if u not in selected:
                        if graph.adjacency_list[u.value][v.value] < minimum:
                            minimum = graph.adjacency_list[u.value][v.value]
                            minimum_node = u
                            minimum_edge = e
            selected_edges.add(minimum_edge)
            # show all available edges
            self.play(code_block.highlight(7, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            print(minimum_edge)
            u = minimum_edge.start_node
            v = minimum_edge.end_node
            if v in selected:
                u, v = v, u
            self.play(minimum_edge.highlight(color=GREEN), u.fade_in_label('u', direction='DOWN'), v.fade_in_label('v', direction='DOWN'))
            self.wait()
            # show the shortest edge - the next edge to add
            self.play(code_block.highlight(9, 3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            selected.add(minimum_node)
            self.play(minimum_node.color(fill_color=PINK4), minimum_edge.highlight(color=PINK4))
            self.play(u.fade_out_label(), v.fade_out_label())
        self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.if_true(False)) if animate_code_block else None
        self.play(code_block.highlight(12, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self._remove_edges(graph, selected_edges)
        self.play(code_block.highlight(13, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        

    # Classical version with queue implementation (matched with Dijkstra)
    def mst_prim_queue(self, graph, graph_position=(3.5, 0), graph_scale=1, create_graph=True, source=None, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=True, character_object=None):
        speed = 1 / speed
        def extract_min_node(list):
            min_so_far = float('inf')
            min_node = None
            for n in list:
                if n.key < min_so_far:
                    min_so_far = n.key
                    min_node = n
            list.remove(min_node)
            return min_node
        if animate_code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            self.play(code_block.create(-3.3))
        if create_graph:
            x_offset, y_offset = graph_position
            self.play(graph.fade_in(scale=graph_scale, x_offset=x_offset, y_offset=y_offset))
        if create_legend:
            l = Legend({(PINK4, PINK4): "MST so far", (PINK4, PINK5): "min node v"}, is_horizontal=show_horizontal_legend)
            l.mobjects.next_to(graph.mobject, UP, buff=0.3)
            self.play(l.animation)
            self.wait()
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(4, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        # Accumulate animations for all nodes and show them at once
        transforms = []
        for node in graph.value2node.values():
            node.initialize_key('∞', show_value=False)
            transforms += node.animations
        unreach_nodes_group = GraphNodesGroup(unreach)
        self.play(*transforms, run_time=1.5*speed)
        self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0), run_time=1.5*speed)
        while unreach:
            # Show group of unreached nodes
            self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            self.play(code_block.if_true()) if animate_code_block else None
            self.play(code_block.highlight(7, wait_time_after=WAIT_TIME_AFTER, character_object=character_object, company='MST')) if animate_code_block else None
            # Color the min node
            v = extract_min_node(unreach)
            self.play(
                v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, has_key=True), 
                v.fade_in_label('u', direction='DOWN')
            )
            self.play(code_block.dehighlight_character(character_object)) if character_object else None

            # Comment out temperarily the complex version of adding edge (one by one)
            if not hide_details:
                self.play(code_block.highlight(8, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                if v in min_edge:
                    self.play(code_block.if_true()) if animate_code_block else None
                    self.play(code_block.highlight(9, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                    edges.append(min_edge[v])
                    self.play(min_edge[v].highlight(color=PINK4))
                else:
                    self.play(code_block.if_true(False)) if animate_code_block else None
            else:
                self.play(code_block.highlight(8, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                if v in min_edge:
                    self.play(code_block.if_true()) if animate_code_block else None
                    edges.append(min_edge[v])
                    self.play(
                        min_edge[v].highlight(color=PINK4, width=EDGE_HIGHLIGHT_STROKE_WIDTH), 
                        v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, 
                        has_key=True)
                    )
                else:
                    self.play(code_block.if_true(False)) if animate_code_block else None
            self.wait(speed)

            # Decrease key and save the min edge
            # Full version - playing each for loop one by one
            if not hide_details:
                nodes_to_keep = [u for u in v.neighbors]
                nodes_to_keep.append(v)
                edges_to_keep = list(v.neighbor2edge.values())
                nodes_to_disappear = [n for n in graph.get_nodes() if n not in nodes_to_keep]
                edges_to_disappear = [e for e in graph.get_edges() if e not in edges_to_keep]
                nodes_to_disappear_group = GraphNodesGroup(nodes_to_disappear)
                edges_to_disappear_group = GraphEdgesGroup(edges_to_disappear)
                self.play(edges_to_disappear_group.disappear(include_label=True), nodes_to_disappear_group.disappear(), run_time=0.8*speed)
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    self.play(code_block.highlight(10, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                    self.play(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH), u.fade_in_label('v', direction='DOWN'))
                    self.play(code_block.highlight(11, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                    if u in unreach and edge_v_u.weight < u.key:
                        self.play(code_block.if_true()) if animate_code_block else None
                        self.play(code_block.highlight(13, 2, wait_time_after=WAIT_TIME_AFTER), run_time=1.5*speed) if animate_code_block else None
                        self.wait()
                        u.key = edge_v_u.weight + v.key
                        update_key_color = GRAY
                        self.play(u.update_key(u.key, color=update_key_color), run_time=1.5*speed)
                        min_edge[u] = edge_v_u
                        self.wait()
                    else:
                        self.play(code_block.if_true(False)) if animate_code_block else None
                self.play(u.dehighlight(), u.fade_out_label())
                self.play(edges_to_disappear_group.appear(include_label=True), nodes_to_disappear_group.appear(), run_time=0.8*speed)
                self.play(v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True), v.fade_out_label())
            # Shortened version - playing all for loops at the same time
            else:
                # Accumulate animations for all qualified nodes and show them at once
                self.play(code_block.highlight(10, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                nodes_to_keep = [u for u in v.neighbors]
                nodes_to_keep.append(v)
                edges_to_keep = list(v.neighbor2edge.values())
                nodes_to_disappear = [n for n in graph.get_nodes() if n not in nodes_to_keep]
                edges_to_disappear = [e for e in graph.get_edges() if e not in edges_to_keep]
                nodes_to_disappear_group = GraphNodesGroup(nodes_to_disappear)
                edges_to_disappear_group = GraphEdgesGroup(edges_to_disappear)
                fade_in_labels_animation = []
                fade_out_labels_animation = []
                for u in v.neighbors:
                    fade_in_labels_animation.append(u.fade_in_label('v', direction='DOWN'))
                    fade_out_labels_animation.append(u.fade_out_label())
                self.play(edges_to_disappear_group.disappear(include_label=True), nodes_to_disappear_group.disappear(), AnimationGroup(*fade_in_labels_animation), run_time=0.8*speed)
                self.play(code_block.highlight(11, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                highlight_animations = []
                relax_animations = []
                dehighlight_animations = []
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    if u in unreach and edge_v_u.weight < u.key:
                        highlight_animations.append(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
                        u.key = edge_v_u.weight
                        update_key_color = GRAY
                        relax_animations.append(u.update_key(u.key, color=update_key_color))
                        min_edge[u] = edge_v_u
                        dehighlight_animations.append(u.dehighlight())
                self.play(code_block.highlight(13, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                if highlight_animations:
                    self.wait(speed)
                    self.play(*highlight_animations)
                if relax_animations:
                    self.wait(speed)
                    self.play(*relax_animations)
                if dehighlight_animations:
                    self.wait(speed)
                    self.play(*dehighlight_animations)
                if not highlight_animations and not relax_animations and not dehighlight_animations:
                    self.wait(speed)
                self.wait(speed)
                self.play(
                    edges_to_disappear_group.appear(include_label=True), 
                    nodes_to_disappear_group.appear(), 
                    AnimationGroup(*fade_out_labels_animation), 
                    v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True), 
                    v.fade_out_label(), 
                    run_time=speed
                )
        self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.if_true(False)) if animate_code_block else None
        self.play(code_block.highlight(15, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self._fade_out_key_restore_names(graph.get_nodes())
        self._remove_edges(graph, edges)
        self.play(code_block.highlight(16, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        return edges


    ##################################
    # MST: Kruskal
    ##################################

    def mst_kruskal_basic(self, graph, graph_position=(3.5, 0), graph_scale=1, create_graph=True, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, add_sound=False):
        speed = 1 / speed
        if animate_code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            self.play(code_block.create(-3.3))
        if create_graph:
            x_offset, y_offset = graph_position
            self.play(graph.fade_in(scale=graph_scale, x_offset=x_offset, y_offset=y_offset))
        if create_legend:
            l = Legend({(PINK2, PINK2): "MST so far", (PURPLE, PURPLE): "curr min edge"}, is_horizontal=show_horizontal_legend)
            l.mobjects.next_to(graph.mobject, UP, buff=0.3)
            self.play(l.animation)
            self.wait()
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        mst_edges = []
        mst_nodes = []
        all_edges = graph.edges
        all_edges.sort(key=lambda edge: edge.weight)
        union_find = UnionFind(graph.get_nodes())
        for i in range(0, graph.n_edges()):
            self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            min_edge = all_edges[i]
            self.play(min_edge.highlight(color=GREEN))
            start_node = min_edge.start_node
            end_node = min_edge.end_node
            parent_of_start = union_find.find(start_node)
            parent_of_end = union_find.find(end_node)
            self.play(code_block.highlight(4, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            if parent_of_start != parent_of_end:
                self.play(code_block.if_true())
                self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                animations = []
                if start_node not in mst_nodes:
                    mst_nodes.append(start_node)
                    animations.append(start_node.color(fill_color=PINK4, stroke_color=PINK3))
                if end_node not in mst_nodes:
                    mst_nodes.append(end_node)
                    animations.append(end_node.color(fill_color=PINK4, stroke_color=PINK3))
                if animations:
                    self.play(min_edge.highlight(color=PINK4), *animations)
                else:
                    self.play(min_edge.highlight(color=PINK4))
                union_find.union(start_node, end_node)
                mst_edges.append(min_edge)
            else:
                cycle_array = graph.get_path(start_node, end_node, mst_edges)
                # edges which are not part of the cycle will disappear, to make the cycle prominent
                non_cycle_array = [e for e in graph.edges if (e not in cycle_array and e != min_edge)]
                non_cycle_group = GraphEdgesGroup(non_cycle_array)
                self.play(non_cycle_group.disappear(include_label=True))
                self.add_sound("wrong.wav") if add_sound else None
                self.play(non_cycle_group.appear(include_label=True))
                self.play(code_block.if_true(False))
                self.play(min_edge.dehighlight())
        self.play(code_block.highlight(7, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self._remove_edges(graph, mst_edges)
        self.play(code_block.highlight(8, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        return mst_edges


    def mst_kruskal_union_find(self, graph, graph_position=(3.5, 0), graph_scale=1, create_graph=True, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, add_sound=False, union_find_object=None):
        speed = 1 / speed
        if animate_code_block:
            code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
            self.play(code_block.create(-3.3))
        if create_graph:
            x_offset, y_offset = graph_position
            self.play(graph.fade_in(scale=graph_scale, x_offset=x_offset, y_offset=y_offset))
        if create_legend:
            l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", ('LINE', GREEN, GREEN): "curr min edge"}, is_horizontal=show_horizontal_legend)
            # l.mobjects.move_to(2.1*UP+1.8*RIGHT)
            l.mobjects.next_to(graph.mobject, UP, buff=0.3)
            self.play(l.animation)
            self.wait()
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(3, 2, wait_time_after=WAIT_TIME_AFTER, character_object=union_find_object, company='MST')) if animate_code_block else None
        mst_edges = []
        all_edges = graph.edges
        all_edges.sort(key=lambda edge: edge.weight)
        all_nodes = graph.get_nodes()
        union_find = UnionFind(all_nodes)
        self.play(union_find.show_set())
        self.play(code_block.dehighlight_character(union_find_object)) if union_find_object else None
        for i in range(0, graph.n_edges()):
            self.play(code_block.highlight(5, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            min_edge = all_edges[i]
            # self.play(min_edge.highlight(color=GREEN), run_time=0.6*speed)
            # self.play(min_edge.dehighlight(), run_time=0.6*speed)
            self.play(min_edge.highlight(color=GREEN))
            self.wait(speed)
            start_node = min_edge.start_node
            end_node = min_edge.end_node
            parent_of_start = union_find.find(start_node)
            parent_of_end = union_find.find(end_node)
            remain_nodes = list(union_find.all_descendants(parent_of_start)) + list(union_find.all_descendants(parent_of_end))
            remain_edges = list(union_find.all_edges_under_root(parent_of_start)) + list(union_find.all_edges_under_root(parent_of_end))
            disappear_edges = [e for e in graph.get_edges() if not (e == min_edge or e in remain_edges)]
            disappear_nodes = [n for n in all_nodes if n not in remain_nodes]
            disappear_edges_group = GraphEdgesGroup(disappear_edges)
            disappear_nodes_group = GraphNodesGroup(disappear_nodes)
            self.play(code_block.highlight(7, wait_time_after=WAIT_TIME_AFTER, character_object=union_find_object, company='MST')) if animate_code_block else None
            if parent_of_start != parent_of_end:
                # self.play(disappear_edges_group.disappear(include_label=True), disappear_nodes_group.disappear(), run_time=0.8*speed)
                # self.add_sound("correct.wav") if add_sound else None
                # self.wait(speed)
                # self.play(disappear_edges_group.appear(include_label=True), disappear_nodes_group.appear(), run_time=0.8*speed)
                self.play(code_block.if_true(wait_time=2))
                self.play(code_block.highlight(8, 2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
                # self.wait(speed)
                self.play(union_find.union(start_node, end_node, min_edge), run_time=1.2)
                mst_edges.append(min_edge)
            else:
                # everything except current edge and start node and end node should disappear
                # self.play(disappear_edges_group.disappear(include_label=True), disappear_nodes_group.disappear(), run_time=0.8*speed)
                # self.add_sound("wrong.wav") if add_sound else None
                # self.wait(speed)
                # self.play(disappear_edges_group.appear(include_label=True), disappear_nodes_group.appear(), run_time=0.8*speed)
                self.play(code_block.if_true(is_true=False, wait_time=2))
                self.play(min_edge.dehighlight())
            self.wait()
            self.play(code_block.dehighlight_character(union_find_object)) if union_find_object else None
        self.play(code_block.highlight(10, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self._remove_edges(graph, mst_edges, speed=0.5)
        self.play(code_block.highlight(11, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        union_find.destroy()
        return mst_edges       

    ##################################
    # Shortest-paths problem: Dijkstra
    ##################################

    # Initialize
    def initialize(self, graph, speed=1):
        transforms = []
        for node in graph.value2node.values():
            node.initialize_key(float('inf'), show_value=False)
            transforms += node.animations
        self.play(*transforms, run_time=1.5*speed)

    # the new version
    def shortest_paths_dijkstra(self, graph, source=None, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False, language='EN', legend_graph_buff=0.5, subtitle_alignment=None, subtitle_position='TOP'):
        speed = 1 / speed
        def extract_min_node(list):
            min_so_far = float('inf')
            min_node = None
            for n in list:
                if n.key < min_so_far:
                    min_so_far = n.key
                    min_node = n
            list.remove(min_node)
            return min_node
        if create_legend:
            l = Legend({(PINK4, PINK4): "shortest paths", (PINK4, PINK5): "min node v"}, is_horizontal=show_horizontal_legend)
            l.mobjects.next_to(graph.mobject, UP, buff=0.3)
            # l.mobjects.move_to(1.8*UP+1.5*RIGHT)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
            self.play(Create(code_block.code))
        subtitle_mobject = get_subtitle_mobject(graph, english_string='Initialize', chinese_string='初始化', language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        if animate_code_block:
            self.play(code_block.highlight(1), run_time=speed)
            self.wait()
            self.play(code_block.highlight(2), run_time=speed)
            self.wait()
            self.play(code_block.highlight(3), run_time=speed)
            self.wait()
        else:
            self.wait()
            self.play(FadeIn(subtitle_mobject))
            self.wait()
        # Accumulate animations for all nodes and show them at once
        self.initialize(graph, speed)
        if animate_code_block:
            self.play(code_block.highlight(4), run_time=speed)
            self.wait()
            self.play(code_block.highlight(5), run_time=speed)
            self.wait()
        else:
            self.wait()
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0), run_time=1.5*speed)
        if not animate_code_block:
            self.play(FadeOut(subtitle_mobject))
            self.wait()
        prev_v = None
        while unreach:
            # Show group of unreached nodes
            if animate_code_block:
                self.wait()
                self.play(code_block.highlight(6), run_time=speed)
                self.wait()
                self.play(code_block.highlight(7), run_time=speed)
            else:
                english_string = 'Find the nearest node'
                chinese_string = """找到最近的点, 放松由此点出发的边"""
                subtitle_mobject = get_subtitle_mobject(graph, english_string=english_string, chinese_string=chinese_string, language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
                self.play(FadeIn(subtitle_mobject))
                self.wait()
            # Color the min node
            v = extract_min_node(unreach)
            self.wait()
            if not hide_details:
                if prev_v:
                    self.wait(speed)
                    self.play(prev_v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True), v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=WIDTH+2, has_key=True))
                    edges.append(min_edge[v])
                    self.play(min_edge[v].highlight(color=PINK4), run_time=0.5*speed)
                    self.play(min_edge[v].dehighlight(), run_time=0.5*speed)
                    self.play(min_edge[v].highlight(color=PINK4), run_time=0.5*speed)
                else:
                    self.wait(speed)
                    self.play(v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, has_key=True))
                self.wait(1.5*speed)
                prev_v = v
            else:
                if prev_v:
                    edges.append(min_edge[v])
                    self.play(min_edge[v].highlight(color=PINK4, width=EDGE_HIGHLIGHT_STROKE_WIDTH), prev_v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True), v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=WIDTH+2, has_key=True))
                else:
                    self.wait()
                    self.play(v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, has_key=True))
                self.wait(1.5*speed)
                prev_v = v
            # Decrease key and save the min edge
            # Full version - playing each for loop one by one
            if not hide_details:
                nodes_to_keep = [u for u in v.neighbors]
                nodes_to_keep.append(v)
                edges_to_keep = list(v.neighbor2edge.values())
                nodes_to_disappear = [n for n in graph.get_nodes() if n not in nodes_to_keep]
                edges_to_disappear = [e for e in graph.get_edges() if e not in edges_to_keep]
                nodes_to_disappear_group = GraphNodesGroup(nodes_to_disappear)
                edges_to_disappear_group = GraphEdgesGroup(edges_to_disappear)
                self.play(edges_to_disappear_group.disappear(include_label=True), nodes_to_disappear_group.disappear(), run_time=0.8*speed)
                prev_u = None
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    self.play(code_block.highlight(8), run_time=speed) if animate_code_block else None
                    if prev_u:
                        self.play(prev_u.dehighlight(), u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
                    else:
                        self.wait(1)
                        self.play(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
                    prev_u = u
                    self.wait(0.5)
                    # self.play(code_block.highlight(9), run_time=speed) if animate_code_block else None
                    # self.wait()
                    self.play(code_block.highlight(9), run_time=speed) if animate_code_block else None
                    self.wait(1.7)
                    if edge_v_u.weight + v.key < u.key:
                        self.play(code_block.highlight(10), run_time=1.5*speed) if animate_code_block else None
                        self.wait()
                        u.key = edge_v_u.weight + v.key
                        update_key_color = GRAY
                        if u not in unreach:
                            update_key_color = BACKGROUND
                        self.play(u.update_key(u.key, color=update_key_color), run_time=1.5*speed)
                        min_edge[u] = edge_v_u
                        self.wait(1)
                        self.play(code_block.highlight(11), run_time=speed) if animate_code_block else None
                        self.wait(1)
                self.play(prev_u.dehighlight())
                self.play(edges_to_disappear_group.appear(include_label=True), nodes_to_disappear_group.appear(), run_time=0.8*speed)

            # Shortened version - playing all for loops at the same time
            else:
                # Accumulate animations for all qualified nodes and show them at once
                if animate_code_block:
                    self.play(code_block.highlight(8, 4), run_time=speed)
                    self.wait(2)
                nodes_to_keep = [u for u in v.neighbors]
                nodes_to_keep.append(v)
                edges_to_keep = list(v.neighbor2edge.values())
                nodes_to_disappear = [n for n in graph.get_nodes() if n not in nodes_to_keep]
                edges_to_disappear = [e for e in graph.get_edges() if e not in edges_to_keep]
                nodes_to_disappear_group = GraphNodesGroup(nodes_to_disappear)
                edges_to_disappear_group = GraphEdgesGroup(edges_to_disappear)
                self.play(edges_to_disappear_group.disappear(include_label=True), nodes_to_disappear_group.disappear())
                highlight_animations = []
                relax_animations = []
                dehighlight_animations = []
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    if edge_v_u.weight + v.key < u.key:
                        highlight_animations.append(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
                        u.key = edge_v_u.weight + v.key
                        update_key_color = GRAY
                        if u not in unreach:
                            update_key_color = BACKGROUND
                        relax_animations.append(u.update_key(u.key, color=update_key_color))
                        min_edge[u] = edge_v_u
                        dehighlight_animations.append(u.dehighlight())
                if highlight_animations:
                    self.wait(speed)
                    self.play(*highlight_animations)
                if relax_animations:
                    self.wait(speed)
                    self.play(*relax_animations)
                if dehighlight_animations:
                    self.wait(speed)
                    self.play(*dehighlight_animations)
                if not highlight_animations and not relax_animations and not dehighlight_animations:
                    self.wait(1.5*speed)
                self.wait(1.2*speed)
                self.play(edges_to_disappear_group.appear(include_label=True), nodes_to_disappear_group.appear())
            if not animate_code_block:
                self.play(FadeOut(subtitle_mobject))
                self.wait()

        self.play(prev_v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True))
        if animate_code_block:
            self.play(code_block.highlight(6), run_time=speed)
            self.wait()
            self.play(code_block.highlight(12), run_time=speed)
            self.wait()
        else:
            subtitle_mobject = get_subtitle_mobject(graph, english_string='Get shortest paths', chinese_string='生成最短路径', language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
            self.play(FadeIn(subtitle_mobject))
            self.wait()
        self._remove_edges(graph, edges, speed=0.5)
        return edges


    ##################################
    # Relaxation
    ##################################


    def relax(self, graph, source, dest, source_key, dest_key, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
        source_node = graph.value2node[source]
        dest_node = graph.value2node[dest]
        edge = graph.get_edge_from_value(source, dest)
        self.play(source_node.initialize_key(source_key, show_value='TOP'), dest_node.initialize_key(dest_key, show_value='TOP'))
        if not code_block:
            code_block = CodeBlock(CODE_FOR_RELAX)
            self.play(Create(code_block.code))
            self.wait()
        if create_legend:
            l = Legend({(BACKGROUND, GREEN): "需要放松的点"}, is_horizontal=True)
            l.mobjects.next_to(graph.mobject, UP, buff=0.8)
            self.play(l.animation)
        self.play(code_block.highlight(1), run_time=speed) if animate_code_block else None
        self.wait() if animate_code_block else None
        self.play(code_block.highlight(2), run_time=speed) if animate_code_block else None
        self.wait() if animate_code_block else None
        if dest_node.key > source_node.key + edge.weight:
            self.play(dest_node.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
            self.wait() if animate_code_block else None
            self.play(code_block.highlight(3), run_time=speed) if animate_code_block else None
            self.wait() if animate_code_block else None
            new_key = source_node.key + edge.weight
            self.play(dest_node.update_key(new_key))
            self.wait() if animate_code_block else None
            self.play(code_block.highlight(4), run_time=speed) if animate_code_block else None
            self.wait() if animate_code_block else None
            dest_node.min_edge = edge
            string = 'prev: '
            string += source
            new_text = Text(string, color=GRAY, font=FONT, weight=BOLD, font_size=32).scale(0.5).next_to(dest_node.circle_mobject, DOWN, buff=0.18)
            self.play(FadeIn(new_text))
            self.wait() if animate_code_block else None
        self.play(code_block.highlight(5), run_time=speed) if animate_code_block else None



    def relax_for_video_only(self, graph_1, graph_2, source, dest, first, second, texts, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
        graph = graph_1
        source_node = graph.value2node[source]
        dest_node = graph.value2node[dest]
        edge = graph.get_edge_from_value(source, dest)
        source_key, dest_key = first
        graph.mobject.shift(3.5*RIGHT)
        title1, title2, legend = texts
        title = Text(title1, color=GRAY, font=FONT, weight=BOLD, font_size=SMALL_FONT_SIZE).next_to(graph.mobject, DOWN, buff=1)
        if not code_block:
            code_block = CodeBlock(CODE_FOR_RELAX)
            self.play(Create(code_block.code))
            self.wait(2)
        self.play(graph.fade_in(), FadeIn(title))
        self.wait(3)
        self.play(source_node.initialize_key(source_key, show_value='TOP'), dest_node.initialize_key(dest_key, show_value='TOP'))
        self.wait(3)
        if create_legend:
            l = Legend({(BACKGROUND, GREEN): legend}, is_horizontal=True)
            l.mobjects.next_to(graph.mobject, UP, buff=0.8)
            self.play(l.animation)
            self.wait(2)
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        if dest_node.key > source_node.key + edge.weight:
            self.play(code_block.if_true(wait_time=4)) if animate_code_block else None
            self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            self.play(dest_node.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
            self.wait(2) if animate_code_block else None
            new_key = source_node.key + edge.weight
            self.play(dest_node.update_key(new_key), run_time=2)
            self.wait(2) if animate_code_block else None
            self.play(code_block.highlight(4, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            dest_node.min_edge = edge
            string = 'prev: '
            string += source
            new_text = Text(string, color=GRAY, font=FONT, weight=BOLD, font_size=32).scale(0.5).next_to(dest_node.circle_mobject, DOWN, buff=0.18)
            self.play(FadeIn(new_text))
            self.wait(2) if animate_code_block else None 
        else:
            self.play(code_block.if_true(is_true=False, wait_time=4))
        self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(graph.fade_out(), FadeOut(new_text), FadeOut(title))
        self.wait()
        
        graph = graph_2
        source_node = graph.value2node[source]
        dest_node = graph.value2node[dest]
        edge = graph.get_edge_from_value(source, dest)
        source_key, dest_key = second
        graph.mobject.shift(3.5*RIGHT)
        title = Text(title2, color=GRAY, font=FONT, weight=BOLD, font_size=SMALL_FONT_SIZE).next_to(graph.mobject, DOWN, buff=1)
        self.play(FadeIn(graph.mobject), FadeIn(title))
        self.wait(3)
        self.play(source_node.initialize_key(source_key, show_value='TOP'), dest_node.initialize_key(dest_key, show_value='TOP'))
        self.wait(3)
        self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
        if dest_node.key > source_node.key + edge.weight:
            self.play(code_block.if_true(wait_time=3)) if animate_code_block else None
            self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            self.play(dest_node.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
            self.wait(2) if animate_code_block else None
            new_key = source_node.key + edge.weight
            self.play(dest_node.update_key(new_key), run_time=2)
            self.wait(2) if animate_code_block else None
            self.play(code_block.highlight(4, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
            dest_node.min_edge = edge
            string = 'prev: '
            string += source
            new_text = Text(string, color=GRAY, font=FONT, weight=BOLD, font_size=32).scale(0.5).next_to(dest_node.circle_mobject, DOWN, buff=0.18)
            self.play(Write(new_text))
            self.wait(2) if animate_code_block else None
            self.play(dest_node.dehighlight())
        else:
            self.play(code_block.if_true(is_true=False, wait_time=3))
        self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None


    ##################################
    # Shortest paths: Bellman-Ford
    ##################################

    def relax_helper(self, source_node, dest_node, edge, speed, animate_code_block=True):
        edge_relaxed = False
        if dest_node.key > source_node.key + edge.weight:
            edge_relaxed = True
            self.play(dest_node.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
            self.wait(speed)
            new_key = source_node.key + edge.weight
            self.play(dest_node.update_key(new_key))
            self.wait(speed) if animate_code_block else None               
            if dest_node.min_edge and dest_node.min_edge != edge:
                if animate_code_block:
                    self.play(dest_node.min_edge.highlight(color=GRAY, width=WIDTH), edge.highlight(color=PINK4), dest_node.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
                else:
                    self.play(dest_node.min_edge.highlight(color=GRAY, width=WIDTH), edge.highlight(color=PINK4), dest_node.dehighlight())
            else:
                if animate_code_block:
                    self.play(edge.highlight(color=PINK4), dest_node.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
                else:
                    self.play(edge.highlight(color=PINK4), dest_node.dehighlight())
            dest_node.min_edge = edge
        else:
            if animate_code_block:
                self.play(edge.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
            else:
                self.play(edge.dehighlight())
        return edge_relaxed


    def bellman_ford(self, graph, graph_position=(3.5, 0), graph_scale=1, source=None, create_graph=True, create_legend=True, show_horizontal_legend=False, animate_code_block=True, subtitle_alignment=None, subtitle_position='TOP', code_block=None, speed=1, hide_details=False, language='EN', music=None, show_graph_only=False, legend_graph_buff=0.5):
        speed = 1 / speed
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_BELLMAN_FORD_WITH_RELAX)
            self.play(Create(code_block.code))
        if create_graph:
            x_offset, y_offset = graph_position
            self.play(graph.fade_in(scale=graph_scale, x_offset=x_offset, y_offset=y_offset))
        if create_legend:
            l = None
            if language == 'CH':
                l = Legend({('LINE', PINK4, PINK4): "最短路径", ('LINE', GREEN, GREEN): "当前边", (BACKGROUND, GREEN): "键值降低的点"}, is_horizontal=show_horizontal_legend)
            elif language == 'EN':
                l = Legend({('LINE', PINK4, PINK4): "shortest paths", ('LINE', GREEN, GREEN): "current edge", (BACKGROUND, GREEN): "node needs decrease-key"}, is_horizontal=show_horizontal_legend)
            l.mobjects.next_to(graph.mobject, UP, buff=legend_graph_buff).align_to(graph.mobject, RIGHT)
            self.play(l.animation)
        if not show_graph_only:
            if music:
                self.add_sound(music)
            subtitle_mobject = get_subtitle_mobject(graph, english_string='Initialize keys', chinese_string='初始化', language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
            if animate_code_block:
                self.wait()
                self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER))
                self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER))
            else:
                self.wait()
                self.play(FadeIn(subtitle_mobject))
                self.wait()
            self.initialize(graph)
            if animate_code_block:
                self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER))
                self.play(code_block.highlight(4, wait_time_after=WAIT_TIME_AFTER))
            else:
                self.wait()
            if not source:
                source_node = graph.value2node.values()[0]
            else:
                source_node = graph.value2node[source]
            self.play(source_node.update_key(0), run_time=1.5)
            if not animate_code_block:
                self.play(FadeOut(subtitle_mobject))
                self.wait()
            is_converged = False
            for i in range(graph.n_nodes()-1):
                # For no code version
                if animate_code_block:
                    self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER))
                else:
                    # if is_converged:
                    #     # Don't have to animate more if all edges remain unchanged
                    #     english_string = 'Relax all edges (' + str(i+1) + 'time)'
                    #     chinese_string = '放松所有的边（第V - 1次）'
                    #     subtitle_mobject = get_subtitle_mobject(graph, english_string=english_string, chinese_string=chinese_string, language=language)
                    #     self.play(FadeIn(subtitle_mobject))
                    # else:
                    english_string = 'Relax all edges (' + str(i+1) + ' / ' + str(graph.n_nodes()-1) + ')'
                    chinese_string = '放松每条边 ~ 第' + str(i+1) + '/' + str(graph.n_nodes()-1) + '次'
                    subtitle_mobject = get_subtitle_mobject(graph, english_string=english_string, chinese_string=chinese_string, language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
                    self.play(FadeIn(subtitle_mobject))
                    self.wait()                
                key_decreased = []
                edges = graph.get_edges_duplicate()
                for edge in edges:
                    source_node = edge.start_node
                    dest_node = edge.end_node
                    if animate_code_block:
                        self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER))
                        self.play(edge.highlight(color=GREEN), source_node.fade_in_label('u', direction='DOWN'), dest_node.fade_in_label('v', direction='DOWN'))
                        self.play(code_block.highlight(7, wait_time_after=WAIT_TIME_AFTER))
                    else:
                        self.play(edge.highlight(color=GREEN))
                    ### RELAX
                    key_decreased.append(self.relax_helper(source_node, dest_node, edge, speed, animate_code_block))
                    self.wait(speed/2)
                if not animate_code_block:
                    self.wait()
                    self.play(FadeOut(subtitle_mobject))
                    self.wait()
                if not animate_code_block and is_converged:
                    break
                if not any(key_decreased):
                    is_converged = True # If no edge decreased the key, it will break in the next round to save time
            ### Check for negative cycle
            if animate_code_block:
                self.play(code_block.highlight(8, wait_time_after=WAIT_TIME_AFTER))
            else:
                subtitle_mobject = get_subtitle_mobject(graph, english_string='Check for any negative cycles', chinese_string='检查每条边, 看是否存在负环', language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
                self.play(FadeIn(subtitle_mobject))
                self.wait()
            for edge in edges:
                source_node = edge.start_node
                dest_node = edge.end_node
                if animate_code_block:
                    self.play(code_block.highlight(9, wait_time_after=WAIT_TIME_AFTER)) 
                    self.play(edge.highlight(color=GREEN), source_node.fade_in_label('u', direction='DOWN'), dest_node.fade_in_label('v', direction='DOWN'))
                    self.wait(speed)
                    self.play(code_block.highlight(10, wait_time_after=WAIT_TIME_AFTER))
                else:
                    self.play(edge.highlight(color=GREEN))
                if dest_node.key > source_node.key + edge.weight:
                    all_edges = GraphEdgesGroup(graph.get_edges())
                    if animate_code_block:
                        self.play(code_block.if_true(wait_time=3))
                        self.play(code_block.highlight(11, wait_time_after=WAIT_TIME_AFTER))
                        self.play(all_edges.highlight(color=RED), source_node.fade_out_label(), dest_node.fade_out_label())
                        self.play(code_block.highlight(13, wait_time_after=WAIT_TIME_AFTER))
                    else:
                        self.play(all_edges.highlight(color=RED))
                    return False
                else:
                    self.play(code_block.if_true(is_true=False, wait_time=3)) if animate_code_block else None
                if animate_code_block:
                    self.play(edge.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
                else:
                    self.play(edge.dehighlight())
            if animate_code_block:
                self.play(code_block.highlight(12, wait_time_after=WAIT_TIME_AFTER))
                self.play(code_block.highlight(13, wait_time_after=WAIT_TIME_AFTER))
            else:
                self.wait()
                self.play(FadeOut(subtitle_mobject))
                self.wait()
                subtitle_mobject = get_subtitle_mobject(graph, english_string='Return shortest paths', chinese_string='生成最短路径', language=language, legend_graph_buff=legend_graph_buff, subtitle_alignment=subtitle_alignment, subtitle_position=subtitle_position)
                self.play(FadeIn(subtitle_mobject))
                self.wait()
            path_edges = graph.get_shortest_paths()
            self._remove_edges(graph, path_edges, speed=0.5)
            return True


    # Comment out an old code for videos generation only
    # def bellman_ford(self, graph, graph_position=(3.5, 0), graph_scale=1, source=None, create_graph=True, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False, language='EN'):
    #     speed = 1 / speed
    #     if animate_code_block and not code_block:
    #         code_block = CodeBlock(CODE_FOR_BELLMAN_FORD_WITH_RELAX)
    #         self.play(Create(code_block.code))
    #     if create_graph:
    #         x_offset, y_offset = graph_position
    #         # self.play(FadeIn(graph.mobject.scale(graph_scale).shift(x_offset*RIGHT+y_offset*UP)))
    #         self.play(graph.fade_in(scale=graph_scale, x_offset=x_offset, y_offset=y_offset))
    #     if create_legend:
    #         l = None
    #         if language == 'CH':
    #             l = Legend({('LINE', PINK4, PINK4): "最短路径", ('LINE', GREEN, GREEN): "当前边", (BACKGROUND, GREEN): "键值降低的点"}, is_horizontal=show_horizontal_legend)
    #         elif language == 'EN':
    #             l = Legend({('LINE', PINK4, PINK4): "shortest paths", ('LINE', GREEN, GREEN): "current edge", (BACKGROUND, GREEN): "node needs decrease-key"}, is_horizontal=show_horizontal_legend)
    #         l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
    #         self.play(l.animation)
    #     self.add_sound('Lifting Dreams - Aakash Gandhi.mp3')
    #     self.play(code_block.highlight(1, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     self.play(code_block.highlight(2, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     self.initialize(graph, speed)
    #     self.play(code_block.highlight(3, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     self.play(code_block.highlight(4, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     if not source:
    #         source_node = graph.value2node.values()[0]
    #     else:
    #         source_node = graph.value2node[source]
    #     self.play(source_node.update_key(0), run_time=1.5*speed)
    #     edges = graph.get_edges()
    #     for i in range(graph.n_nodes()-1):
    #         self.play(code_block.highlight(5, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #         for edge in edges:
    #             source_node = edge.start_node
    #             dest_node = edge.end_node
    #             self.play(code_block.highlight(6, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #             self.play(edge.highlight(color=GREEN), source_node.fade_in_label('u', direction='DOWN'), dest_node.fade_in_label('v', direction='DOWN'))
    #             self.play(code_block.highlight(7, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #             ### RELAX
    #             if dest_node.key > source_node.key + edge.weight:
    #                 self.play(dest_node.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
    #                 self.wait(2)
    #                 new_key = source_node.key + edge.weight
    #                 self.play(dest_node.update_key(new_key))
    #                 self.wait(2)                        
    #                 if dest_node.min_edge and dest_node.min_edge != edge:
    #                     self.play(dest_node.min_edge.highlight(color=GRAY, width=WIDTH), edge.highlight(color=PINK4), dest_node.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
    #                 else:
    #                     self.play(edge.highlight(color=PINK4), dest_node.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
    #                 dest_node.min_edge = edge
    #             else:
    #                 self.play(edge.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
    #             self.wait(2)
    #     ### Check for negative cycle
    #     self.play(code_block.highlight(8, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     for edge in edges:
    #         source_node = edge.start_node
    #         dest_node = edge.end_node
    #         self.play(code_block.highlight(9, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #         self.play(edge.highlight(color=GREEN), source_node.fade_in_label('u', direction='DOWN'), dest_node.fade_in_label('v', direction='DOWN'))
    #         self.wait()
    #         self.play(code_block.highlight(10, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #         if dest_node.key > source_node.key + edge.weight:
    #             self.play(code_block.if_true(wait_time=3)) if animate_code_block else None
    #             self.play(code_block.highlight(11, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #             all_edges = GraphEdgesGroup(graph.get_edges())
    #             if animate_code_block:
    #                 self.play(all_edges.highlight(color=RED), source_node.fade_out_label(), dest_node.fade_out_label())
    #             else:
    #                 self.play(all_edges.highlight(color=RED))
    #             self.play(code_block.highlight(13, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #             return False
    #         else:
    #             self.play(code_block.if_true(is_true=False, wait_time=3)) if animate_code_block else None
    #         self.play(edge.dehighlight(), source_node.fade_out_label(), dest_node.fade_out_label())
    #     self.play(code_block.highlight(12, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     self.play(code_block.highlight(13, wait_time_after=WAIT_TIME_AFTER)) if animate_code_block else None
    #     path_edges = graph.get_shortest_paths()
    #     self._remove_edges(graph, path_edges, speed=1)
    #     return True


    ##################################
    # Construct - with input commands
    ##################################

    # Comment out for easy testing
    # def construct(self, command):
    #     self.camera.background_color = BACKGROUND
    #     w = watermark()
    #     self.add(w)
        
    #     graph = GraphObject(self.adjacency_list, self.position)
    #     if command == "prim":
    #         print("Generating animations for Prim...")
    #         self.add(show_title_for_demo("PRIM'S ALGO FOR MST"))
    #         graph = GraphObject(self.adjacency_list, self.position)
    #         self.mst_prim_queue(graph, graph_position=(3.5, -0.5), source='A')
    #         self.wait(2)
    #     elif command == "kruskal":
    #         print("Generating animations for Kruskal...")
    #         self.add(show_title_for_demo("KRUSKAL'S ALGO FOR MST"))
    #         graph = GraphObject(self.adjacency_list, self.position)
    #         self.mst_kruskal_union_find(graph, graph_position=(3.5, -0.5))
    #         self.wait(2)

    ##################################
    # Construct - without input commands (for developer easy testing)
    # To test, enter the command: `manim graph_algorithm.py GraphAlgorithm -ql`
    ##################################

    def construct(self):
        self.camera.background_color = BACKGROUND
        watermark_ch = watermark(is_chinese=True)
        watermark_en = watermark(is_chinese=False)

        # Comment out BFS code  
        new_position = scale_position(BFS_POSITION, 2, 1.5)
        graph = GraphObject(MAP_DIRECTED, new_position)
        self.add(graph.mobject.shift(3.2 * RIGHT))
        # code_block = CodeBlock(CODE2_FOR_BFS)
        # self.add(code_block.code)
        # self.bfs(graph, 'A')

        # Comment out DFS code
        # graph = Graph(MAP_DIRECTED, POSITION2)
        # self.add(graph.mobject.shift(3.2 * RIGHT))
        # self.dfs(graph, True)
        
        ### Prim-basic
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # l = Legend({PINK1: "MST so far"})
        # l.mobjects.move_to(2.7*UP + 5*RIGHT)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.3*DOWN)))
        # self.play(l.animation)
        # self.mst_prim_basic(graph, create_legend=False, animate_code_block=False, code_block=None, speed=2)
        # self.wait(10)


        ### Prim-basic create thumbnail
        # l = Legend({PINK1: "MST so far"})
        # l.mobjects.move_to(1.6*UP+1.7*RIGHT)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # graph.mobject.scale(0.9).shift(3.7*RIGHT)
        # self.add(l.mobjects, code_block.code, graph.mobject)


        ### Prim-queue
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.3*RIGHT)))
        # self.mst_prim_queue(graph, source='A', code_block=code_block, hide_details=True)
        # self.wait(10)


        ### Prim-queue-no-code
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.mobject.shift(0.3*DOWN)
        # l = Legend({(PINK4, PINK4): "MST so far", (PINK4, PINK5): "vertex with min edge"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(FadeIn(graph.mobject))
        # self.play(l.animation)
        # self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=2)
        # self.wait(10)


        ### Prim-queue-no-code-Chinese
        # title_mobject = show_title_for_demo("PRIM 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.mobject.shift(0.3*DOWN)
        # l = Legend({(PINK4, PINK4): "最小生成树", (PINK4, PINK5): "与最短边相连的点"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(FadeIn(graph.mobject))
        # self.play(l.animation)
        # self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=2)
        # self.wait(10)


        ### Kruskal-basic
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({(PINK2, PINK2): "MST so far", (GREEN, GREEN): "curr min edge"})
        # l.mobjects.move_to(2*UP+1.6*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, code_block=code_block, create_legend=False)
        # self.wait(10)


        ### Kruskal-basic-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({(PINK2, PINK2): "最小生成树", (GREEN, GREEN): "当前最小边"})
        # l.mobjects.move_to(2*UP+1.6*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, code_block=code_block, create_legend=False)
        # self.wait(10)


        ### Kruskal-basic-no-code
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.mobject.shift(0.3*DOWN)
        # l = Legend({(PINK2, PINK2): "MST so far", (GREEN, GREEN): "curr min edge"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(FadeIn(graph.mobject))
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(10)


        ### Kruskal-basic-no-code-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.mobject.shift(0.3*DOWN)
        # l = Legend({(PINK2, PINK2): "最小生成树", (GREEN, GREEN): "当前最小边"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(FadeIn(graph.mobject))
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(10)


        ### Kruskal-union-find
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.2*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", (GREEN, GREEN): "curr min edge"})
        # l.mobjects.move_to(2.1*UP+1.9*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_union_find(graph, code_block=code_block, create_legend=False)
        # self.wait(15)


        ### Kruskal-union-find-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "最小生成树", (GREEN, GREEN): "当前最小边"})
        # l.mobjects.move_to(2.2*UP+1.9*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_union_find(graph, code_block=code_block, create_legend=False)
        # self.wait(15)


        ### Kruskal-union-find-no-code
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.3*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", (GREEN, GREEN): "curr min edge"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.mst_kruskal_union_find(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(15)


        ### Kruskal-union-find-no-code-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.3*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "最小生成树", (GREEN, GREEN): "当前最小边"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.mst_kruskal_union_find(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(15)


        ### Dijkastra
        # title_mobject = show_title_for_demo("DIJKSTRA'S ALGO FOR SINGLE-SOURCE SHORTEST PATHS")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # new_position = scale_position(DIPOSITION_DIJKASTRA_CLRS, 1.8, 2)
        # graph = GraphObject(DIMAP_DIJKASTRA_CLRS, new_position)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.4*DOWN)))
        # l = Legend({(PINK4, PINK4): "shortest paths", (PINK4, PINK5): "v", (BACKGROUND, GREEN): "u"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5)
        # self.play(l.animation)
        # self.shortest_paths_dijkstra(graph, source='A', code_block=code_block, create_legend=False, hide_details=False)
        # self.wait(15)


        ### Dijkastra-Chinese
        # title_mobject = show_title_for_demo("DIJKSTRA 算法  ·  单源最短路径")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # new_position = scale_position(DIPOSITION_DIJKASTRA_CLRS, 1.8, 2)
        # graph = GraphObject(DIMAP_DIJKASTRA_CLRS, new_position)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.5*RIGHT+0.4*DOWN)))
        # l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "v", (BACKGROUND, GREEN): "u"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5)
        # self.play(l.animation)
        # self.shortest_paths_dijkstra(graph, source='A', code_block=code_block, create_legend=False, hide_details=False)
        # self.wait(15)


        ### Dijkastra-no-code
        # title_mobject = show_title_for_demo("DIJKSTRA'S ALGO")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD_DIJKSTRA, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD_DIJKSTRA, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.5*DOWN)))
        # self.add_sound('Anton - Dan Bodan.mp3')
        # l = Legend({(PINK4, PINK4): "shortest paths", (PINK4, PINK5): "nearest node", (BACKGROUND, GREEN): "node needs relaxation"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.shortest_paths_dijkstra(graph, source='Src', create_legend=False, animate_code_block=False, speed=2, hide_details=True)
        # self.wait(15)


        ### Dijkastra-no-code-Chinese
        # title_mobject = show_title_for_demo("DIJKSTRA 算法  ·  单源最短路径")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.3*DOWN)))
        # l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "当前最近的点", (BACKGROUND, GREEN): "需要放松的点"}, is_horizontal=True)
        # l.mobjects.next_to(graph.mobject, UP, buff=0.5).align_to(graph.mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.shortest_paths_dijkstra(graph, source='A', create_legend=False, animate_code_block=False, speed=2, hide_details=True)
        # self.wait(15)


        ### Dijkastra-negative-edge-Chinese
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("DIJKSTRA 算法  ·  单源最短路径")
        # self.add(title_mobject)
        # self.wait()
        # new_position = scale_position(POSITION_DIJKSTRA_NEGATIVE_CH, 1.3, 1.3)
        # graph_correct = GraphObject(MAP_DIJKSTRA_NEGATIVE_CH, new_position)
        # self.play(FadeIn(graph_correct.graph_mobject))
        # self.add_sound('Firefly - Chris Haugen.mp3')
        # shortest_paths = []
        # shortest_paths.append(graph_correct.get_edge_from_value('始', 'B'))
        # shortest_paths.append(graph_correct.get_edge_from_value('B', 'C'))
        # shortest_paths_group = GraphEdgesGroup(shortest_paths)
        # nodes = graph_correct.get_nodes()
        # nodes_group = GraphNodesGroup(nodes)
        # hiden_edge = graph_correct.get_edge_from_value('始', 'C')
        # text_correct_answer = get_text('正确的最短路径', font_size=31).shift(DOWN*2.2)
        # self.wait(2)
        # self.play(FadeIn(text_correct_answer), shortest_paths_group.highlight(width=WIDTH+4), nodes_group.color(text_color=BACKGROUND, fill_color=PINK4, stroke_color=PINK3), Uncreate(hiden_edge.mobject), run_time=1)
        # self.wait(2)
        # correct_group = VGroup(text_correct_answer, graph_correct.graph_mobject)
        # self.play(correct_group.animate.scale(0.5).to_edge(UR, buff=0.6))
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_DIJKSTRA_NEGATIVE_CH, new_position)
        # self.play(FadeIn(graph.mobject.shift(3.7*RIGHT+0.7*DOWN)))
        # l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "当前最近的点 v", (BACKGROUND, GREEN): "需要放松的点 u"}, is_horizontal=False)
        # l.mobjects.move_to(graph.mobject.get_center()).shift(UP*2.9 + LEFT*1.7)
        # self.play(l.animation)
        # self.wait()
        # self.shortest_paths_dijkstra(graph, source='始', code_block=code_block, create_legend=False, hide_details=True)
        # self.wait(15)


        ### Dijkastra-negative-edge
        # self.add(watermark_en)
        # title_mobject = show_title_for_demo("DIJKSTRA'S ALGO")
        # self.add(title_mobject)
        # self.wait()
        # new_position = scale_position(POSITION_DIJKSTRA_NEGATIVE_EN, 1.3, 1.3)
        # graph_correct = GraphObject(MAP_DIJKSTRA_NEGATIVE_EN, new_position)
        # self.play(FadeIn(graph_correct.graph_mobject))
        # self.add_sound('Firefly - Chris Haugen.mp3')
        # shortest_paths = []
        # shortest_paths.append(graph_correct.get_edge_from_value('Src', 'B'))
        # shortest_paths.append(graph_correct.get_edge_from_value('B', 'C'))
        # shortest_paths_group = GraphEdgesGroup(shortest_paths)
        # nodes = graph_correct.get_nodes()
        # nodes_group = GraphNodesGroup(nodes)
        # hiden_edge = graph_correct.get_edge_from_value('Src', 'C')
        # text_correct_answer = get_text('Correct Shortest Paths', font_size=31).shift(DOWN*2.2)
        # self.wait(2)
        # self.play(FadeIn(text_correct_answer), shortest_paths_group.highlight(width=WIDTH+4), nodes_group.color(text_color=BACKGROUND, fill_color=PINK4, stroke_color=PINK3), Uncreate(hiden_edge.mobject), run_time=1)
        # self.wait(2)
        # correct_group = VGroup(text_correct_answer, graph_correct.graph_mobject)
        # self.play(correct_group.animate.scale(0.5).to_edge(UR, buff=0.6))
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_DIJKSTRA_NEGATIVE_EN, new_position)
        # self.play(FadeIn(graph.mobject.shift(3.7*RIGHT+0.7*DOWN)))
        # l = Legend({(PINK4, PINK4): "shortest paths", (PINK4, PINK5): "v: nearest node", (BACKGROUND, GREEN): "u: node needs relaxation"}, is_horizontal=False)
        # l.mobjects.move_to(graph.mobject.get_center()).shift(UP*2.9 + LEFT*1.6)
        # self.play(l.animation)
        # self.wait()
        # self.shortest_paths_dijkstra(graph, source='Src', code_block=code_block, create_legend=False, hide_details=True)
        # self.wait(15)


        ### Compare Prim vs. Dijkstra (CH)
        # def title_group(title_text, legend_text):
        #     name = Text(title_text, color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5)
        #     l = Legend({(PINK4, PINK4): legend_text}, is_horizontal=True)
        #     l.mobjects.next_to(name, RIGHT, buff=0.3)
        #     return VGroup(name, l.mobjects)
        # title_mobject = show_title_for_demo("PRIM'S VS. DIJKSTRA'S")
        # self.add(title_mobject)  
        # top_l = Legend({(PINK4, PINK5): "当前最近的点", (BACKGROUND, GREEN): "需要放松的点"}, is_horizontal=True)
        # top_l.mobjects.move_to(ORIGIN).to_edge(UP, buff=0.6)
        # self.play(top_l.animation)
        # prim_title = title_group("Prim's", "最小生成树")
        # prim_title.shift(LEFT * 4.1 + UP * 1.9)
        # dij_title = title_group("Dijkstra's", "最短路径")
        # dij_title.shift(RIGHT * 1.9 + UP * 1.9)
        # self.play(FadeIn(prim_title))
        # self.play(FadeIn(dij_title))
        # self.wait()
        ## Prim
        # self.wait()
        # new_position = scale_position(POSITION_SQUARE, 1.8, 1.8)
        # # graph = GraphObject(MAP_SQUARE_1, new_position)
        # # graph = GraphObject(MAP_SQUARE_2, new_position)
        # graph = GraphObject(MAP_SQUARE_3, new_position)
        # graph.mobject.scale(0.9).next_to(prim_title, DOWN, buff=0.5)
        # self.play(FadeIn(graph.mobject))
        # self.wait(3)
        # edges = self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=1)
        # self.wait(5)
        # nodes = graph.get_nodes()
        # fadeout_remain = [ e.fade_out() for e in nodes + edges]
        # self.play(*fadeout_remain)
        # self.wait()
        ## Dijkstra
        # self.wait()
        # new_position = scale_position(POSITION_SQUARE_SRC, 1.8, 1.8)
        # # graph = GraphObject(MAP_SQUARE_SRC_1, new_position)
        # # graph = GraphObject(MAP_SQUARE_SRC_2, new_position)
        # graph = GraphObject(MAP_SQUARE_SRC_3, new_position)
        # graph.mobject.scale(0.9).next_to(dij_title, DOWN, buff=0.5)
        # self.play(FadeIn(graph.mobject))
        # self.wait(3)
        # edges = self.shortest_paths_dijkstra(graph, source='Src', create_legend=False, animate_code_block=False, hide_details=True, speed=1)
        # self.wait(5)
        # nodes = graph.get_nodes()
        # fadeout_remain = [ e.fade_out() for e in nodes + edges]
        # self.play(*fadeout_remain)
        # self.wait()


        ### Compare Prim vs. Dijkstra (EN)
        # def title_group(title_text, legend_text):
        #     name = Text(title_text, color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5)
        #     l = Legend({(PINK4, PINK4): legend_text}, is_horizontal=True)
        #     l.mobjects.next_to(name, RIGHT, buff=0.3)
        #     return VGroup(name, l.mobjects)
        # title_mobject = show_title_for_demo("PRIM'S VS. DIJKSTRA'S")
        # self.add(title_mobject)  
        # top_l = Legend({(PINK4, PINK5): "nearest node", (BACKGROUND, GREEN): "node needs relaxation"}, is_horizontal=True)
        # top_l.mobjects.move_to(ORIGIN).to_edge(UP, buff=0.6)
        # self.play(top_l.animation)
        # prim_title = title_group("Prim's", "MST")
        # prim_title.shift(LEFT * 4.1 + UP * 1.9)
        # dij_title = title_group("Dijkstra's", "shortest paths")
        # dij_title.shift(RIGHT * 1.9 + UP * 1.9)
        # self.play(FadeIn(prim_title))
        # self.play(FadeIn(dij_title))
        # self.wait()
        ## Prim
        # self.wait()
        # new_position = scale_position(POSITION_SQUARE, 1.8, 1.8)
        # graph = GraphObject(MAP_SQUARE_1, new_position)
        # graph = GraphObject(MAP_SQUARE_2, new_position)
        # graph = GraphObject(MAP_SQUARE_3, new_position)
        # graph.mobject.scale(0.9).next_to(prim_title, DOWN, buff=0.5)
        # self.play(FadeIn(graph.mobject))
        # self.wait(3)
        # edges = self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=1)
        # self.wait(5)
        # nodes = graph.get_nodes()
        # fadeout_remain = [ e.fade_out() for e in nodes + edges]
        # self.play(*fadeout_remain)
        # self.wait()
        ## Dijkstra
        # self.wait()
        # new_position = scale_position(POSITION_SQUARE_SRC, 1.8, 1.8)
        # # graph = GraphObject(MAP_SQUARE_SRC_1, new_position)
        # # graph = GraphObject(MAP_SQUARE_SRC_2, new_position)
        # graph = GraphObject(MAP_SQUARE_SRC_3, new_position)
        # graph.mobject.scale(0.9).next_to(dij_title, DOWN, buff=0.5)
        # self.play(FadeIn(graph.mobject))
        # self.wait(3)
        # edges = self.shortest_paths_dijkstra(graph, source='Src', create_legend=False, animate_code_block=False, hide_details=True, speed=1)
        # self.wait(5)
        # nodes = graph.get_nodes()
        # fadeout_remain = [ e.fade_out() for e in nodes + edges]
        # self.play(*fadeout_remain)
        # self.wait()


        ### Relaxation (CH)
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("放松一条边 ")
        # self.add(title_mobject)
        # self.wait()
        # new_position = scale_position(POSITION_RELAX, 2.8, 1)
        # graph_1 = GraphObject(MAP_RELAX, new_position)
        # graph_2 = GraphObject(MAP_RELAX, new_position)
        # self.add_sound('Firefly - Chris Haugen.mp3')
        # self.relax_for_video_only(graph_1, graph_2, source='u', dest='v', first=(1, 100), second=(1, 3), texts=('例子1: v 的键值降低', '例子2: v 的键值不变', '键值降低的点'), create_legend=True)
        # self.wait(4)
        # self.clear()
        # self.play(endding())
        # self.wait(15)


        ### Relaxation (EN)
        # self.add(watermark_en)
        # title_mobject = show_title_for_demo("Relaxation")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_RELAX, 2.8, 1)
        # graph_1 = GraphObject(MAP_RELAX, new_position)
        # graph_2 = GraphObject(MAP_RELAX, new_position)
        # self.add_sound('Firefly - Chris Haugen.mp3')
        # self.relax_for_video_only(graph_1, graph_2, source='u', dest='v', first=(1, 100), second=(1, 3), texts=('E.g.1: v.key decreased', 'E.g.2: v.key unchanged', 'node needs decrease-key'), create_legend=True)
        # self.wait(2)
        # self.clear()
        # self.play(endding(is_chinese=False))
        # self.wait(15)


        ### Bellman-Ford (CH)
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("BELLMAN-FORD 算法")
        # self.add(title_mobject)
        # self.wait()
        ## Positive cycle
        # new_position = scale_position(POSITION_DIJKSTRA_NEGATIVE_EN, 1.3, 1.3)
        # graph = GraphObject(MAP_DIJKSTRA_NEGATIVE_EN, new_position)
        ## Negative cycle
        # new_position = scale_position(POSITION_TRIANGLE_NEGATIVE_CYCLE, 1.3, 1.3)
        # graph = GraphObject(MAP_TRIANGLE_NEGATIVE_CYCLE, new_position)
        # self.bellman_ford(graph, graph_position=(3.5, -0.5), source='Src', create_graph=True, hide_details=False)
        # self.wait(4)
        # self.clear()
        # self.play(endding(language='CH'))
        # self.wait(15)


        ### Bellman-Ford (EN)
        # self.add(watermark_en)
        # title_mobject = show_title_for_demo("BELLMAN-FORD ALGO")
        # self.add(title_mobject)
        # self.wait()
        ## Positive cycle
        # new_position = scale_position(POSITION_DIJKSTRA_NEGATIVE_EN, 1.3, 1.3)
        # graph = GraphObject(MAP_DIJKSTRA_NEGATIVE_EN, new_position)
        ## Negative cycle
        # new_position = scale_position(POSITION_TRIANGLE_NEGATIVE_CYCLE, 1.3, 1.3)
        # graph = GraphObject(MAP_TRIANGLE_NEGATIVE_CYCLE, new_position)
        # self.bellman_ford(graph, graph_position=(3.5, -0.8), source='Src', create_graph=True, hide_details=False, show_horizontal_legend=False, language='EN')
        # self.wait(4)
        # self.clear()
        # self.play(endding(language='EN'))
        # self.wait(15)


        ### Bellman-Ford-no-code (CH)
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("BELLMAN-FORD 算法")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_DOUBLE_SQUARE, 4.8, 3)
        # graph = GraphObject(MAP_DOUBLE_SQUARE, new_position)
        # self.bellman_ford(graph, music='Facile - Kevin MacLeod.mp3', source='Src', graph_position=(0, -0.5), create_legend=True, animate_code_block=False, show_horizontal_legend=True, speed=2, hide_details=True, language='CH')
        # self.wait(5)
        # self.clear()
        # self.play(endding(language='CH'))
        # self.wait(10)

    
        ### Bellman-Ford-no-code (EN)
        # self.add(watermark_en)
        # title_mobject = show_title_for_demo("BELLMAN-FORD ALGO")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_DOUBLE_SQUARE, 4.8, 3)
        # graph = GraphObject(MAP_DOUBLE_SQUARE, new_position)
        # self.bellman_ford(graph, music='Facile - Kevin MacLeod.mp3', source='Src', graph_position=(0, 0), create_legend=True, animate_code_block=False, show_horizontal_legend=True, speed=2, hide_details=True, language='EN', subtitle_position='DOWN')
        # self.wait(5)
        # self.clear()
        # self.play(endding(language='EN'))
        # self.wait(10)


        ### Bellman-Ford-why-n-1-iteration (CH)
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("BELLMAN-FORD 算法")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_6_NODES_HORIZONTAL, 2, 1)
        # graph = GraphObject(MAP_6_NODES_HORIZONTAL, new_position)
        # self.bellman_ford(graph, music='人海如潮.mp3', source='Src', graph_position=(0, -0.3), create_legend=True, animate_code_block=False, show_horizontal_legend=True, speed=2, hide_details=True, language='CH', show_graph_only=False, legend_graph_buff=1)
        # self.wait(5)
        # self.clear()
        # self.play(endding(language='CH'))
        # self.wait(10)


        ### Bellman-Ford-why-n-1-iteration (EN)
        # self.add(watermark_en)
        # title_mobject = show_title_for_demo("BELLMAN-FORD ALGO")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_6_NODES_HORIZONTAL, 2, 1)
        # graph = GraphObject(MAP_6_NODES_HORIZONTAL, new_position)
        # self.bellman_ford(graph, music='人海如潮.mp3', source='Src', graph_position=(0, -0.3), create_legend=True, animate_code_block=False, show_horizontal_legend=True, speed=2, hide_details=True, language='EN', show_graph_only=False, legend_graph_buff=1, subtitle_position='DOWN')
        # self.wait(5)
        # self.clear()
        # self.play(endding(language='EN'))
        # self.wait(10)


        ### Compare Bellman-ford vs. Dijkstra (CH)
        # self.add(watermark_ch)
        # title_mobject = show_title_for_demo("DIJKSTRA'S VS. BELLMAN-FORD")
        # self.add(title_mobject)  
        # top_l = Legend({('LINE', PINK4, PINK4): "最短路径", (BACKGROUND, GREEN): "键值降低的点"}, is_horizontal=True)
        # top_l.mobjects.move_to(ORIGIN).to_edge(UP, buff=1)
        # self.play(top_l.animation)
        # dij_title = Text("Dijkstra's 迪杰斯特拉算法", color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5)
        # dij_title.next_to(top_l.mobjects, DOWN, buff=0.5).shift(LEFT * 3.2)
        # bell_title = Text("Bellman-Ford 贝尔曼福特算法", color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5)
        # bell_title.next_to(top_l.mobjects, DOWN, buff=0.5).shift(RIGHT * 3.1)
        # self.play(FadeIn(dij_title))
        # self.play(FadeIn(bell_title))
        # self.wait(240)
        # new_position = scale_position(POSITION_DOUBLE_SQUARE, 2, 3)
        # graph_left = GraphObject(MAP_DOUBLE_SQUARE, new_position)
        # graph_left.graph_mobject.scale(0.9).shift(LEFT * 3.2 + DOWN * 0.4)
        # graph_right = GraphObject(MAP_DOUBLE_SQUARE, new_position)
        # graph_right.graph_mobject.scale(0.9).shift(RIGHT * 3.1 + DOWN * 0.4)
        # ## Dijkstra
        # self.play(FadeIn(graph_left.graph_mobject))
        # self.wait(3)
        # self.shortest_paths_dijkstra(graph_left, source='Src', create_legend=False, animate_code_block=False, subtitle_position='DOWN', hide_details=True, speed=1, language='CH')
        # ## Bellman-Ford
        # self.play(FadeIn(graph_right.graph_mobject))
        # self.wait(3)
        # self.bellman_ford(graph_right, create_graph=False, source='Src', create_legend=False, animate_code_block=False, subtitle_position='DOWN', hide_details=True, speed=1, language='CH')
        # self.wait(5)
        ## Generate dialogues
        # le = Ellipse(width=1.5, height=0.8)
        # ll = Line((0,0.15,0), (0.15,0,0)).shift(0.4*UP+0.6*LEFT)
        # ldialogue = VGroup(le, ll).set_stroke(color=PINK5)
        # ltext1 = get_text('我好了', color=PINK5, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(le)
        # ldialogue += ltext1
        # self.play(Write(ldialogue.shift(0.2*LEFT+0.1*UP)))
        # self.wait(4)
        # ltext2 = get_text('等你', color=PINK5, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(le)
        # self.play(Unwrite(ltext1))
        # ldialogue += ltext2
        # self.play(Write(ltext2))
        # self.wait(4)
        # re = Ellipse(width=1.5, height=0.8)
        # rl = Line((0,0,0), (0.15,0.15,0)).shift(0.35*UP+0.6*RIGHT)
        # rdialogue = VGroup(re, rl).set_stroke(color=BLUE1).shift(1.3*DOWN)
        # rtext1 = get_text('来了', color=BLUE1, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(re)
        # rdialogue += rtext1
        # self.play(Write(rdialogue.shift(0)))
        # self.wait(4)
        # self.play(Unwrite(ldialogue))
        # self.play(Unwrite(rdialogue))
        # self.wait(1)
        # re = Ellipse(width=1.5, height=0.8)
        # rl = Line((0,0,0), (0.15,0.15,0)).shift(0.35*UP+0.55*RIGHT)
        # rtext1 = get_text('我也好了', color=BLUE1, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(re)
        # rdialogue = VGroup(re, rl).set_stroke(color=BLUE1)
        # rdialogue += rtext1
        # rdialogue.shift(1.3*DOWN)
        # self.play(Write(rdialogue))
        # self.wait(4)
        # rtext2 = get_text('在擦汗呢', color=BLUE1, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(re)
        # self.play(Unwrite(rtext1))
        # self.play(Write(rtext2))
        # self.wait()
        ## Generate endding
        # self.wait(0.3)
        # self.play(endding(language='CH'))
        # self.wait(10)


        ### 算法童话系列 ###
        def fairytale_algorithm_en():
            ##################################
            # English
            ##################################
            def get_text_below(string, graph):
                return get_text(string, weight=NORMAL).next_to(graph.mobject, DOWN, buff=0.5)
            def get_text_left(string):
                return get_text(string, weight=BOLD, font_size=20).to_edge(LEFT, buff=1)
            def get_text_left_next(string, mobject_above):
                return get_text_left(string, graph).next_to(mobject_above, DOWN, buff=0.3).align_to(mobject_above, LEFT)
            title_mobject = show_title_for_demo("The Fairy Tale of Algorithms")
            self.add(title_mobject)
            
            ### Animation 1 MST ###
            kruskal = Character("Kruskal", "kruskal.png")
            concepts_map = ConceptsMap([kruskal])
            self.play(kruskal.fade_in())
            self.wait()
            self.play(concepts_map.add_company("MST ®", kruskal, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.wait()
            # self.play(concepts_map.show_only([kruskal.company]))
            # self.wait()
            # self.play(kruskal.company.move_to_top_right())
            # self.wait()
            new_position = scale_position(FAIRYTALE_POSITION, 2, 2)
            graph = GraphObject(FAIRYTALE_MAP, new_position)
            # self.play(graph.fade_in())
            # self.wait()
            # mst_edges_group = graph.get_mst_edges('A')
            # mst_nodes_group = graph.get_mst_nodes()
            # self.play(mst_edges_group.highlight(width=EDGE_HIGHLIGHT_STROKE_WIDTH), mst_nodes_group.fill())
            # formula = get_text_below("4 + 7 + 2 + 1 + 5 + 3 = 22", graph)
            # self.wait()
            # self.play(Write(formula))
            # self.wait()
            # self._remove_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # mst_title = get_text("Minimum Spanning Tree", weight=BOLD).to_edge(UP, buff=0.9)
            # self.play(Write(mst_title))
            # self.wait()
            # self.play(Unwrite(formula))
            # self.wait()
            # self._restore_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.play(graph.shift(x_offset=3))
            # outline = LeftSideOutline("1. Cover all nodes", buff=2)
            # self.wait()
            # self.play(outline.show("1. Cover all nodes"))
            # self.wait()
            # self.play(mst_edges_group.dehighlight())
            # self.wait()
            # self.play(outline.add("""
            # 2. The sum of edge weights
            # is minimum
            # """))
            # self.play(mst_edges_group.highlight(width=EDGE_HIGHLIGHT_STROKE_WIDTH))
            # self.wait()
            # self.play(outline.add("4 + 7 + 2 + 1 + 5 + 3 = 22", is_secondary=True))
            # self.wait()
            # self._remove_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # self._restore_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # self.play(graph.fade_out(), outline.fade_out(), FadeOut(mst_title))
            # self.wait()
            # self.play(kruskal.company.back_from_top_right())
            # self.wait()
            # self.play(concepts_map.show_all())
            # self.wait()

            ### Animation 2 Kruskal ###
            # self.wait()
            # self.play(concepts_map.show_only([kruskal]))
            # self.play(kruskal.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE*0.8))
            # self.wait()
            kruskal_code_block = CodeBlock(CODE_FOR_KRUSKAL)
            # l = Legend({
            #     (PINK4, PINK4): "MST so far", 
            #     ('LINE', GREEN, GREEN): "curr min edge"
            # }, is_horizontal=True)
            # l.mobjects.next_to(kruskal.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(kruskal_code_block.create(x_offset=-2.6))
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.play(l.fade_in())
            # self.mst_kruskal_basic(graph, code_block=kruskal_code_block, create_legend=False)
            # self.wait()

            ### Animation 3 add same label ###
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.play(l.fade_in())
            # self.wait()
            # self.play(kruskal_code_block.highlight(4, 2))
            # self.wait()
            # green_edge_1 = graph.get_edge_by_name('B', 'C')
            # green_edge_2 = graph.get_edge_by_name('C', 'D')
            # small_group_edges = GraphEdgesGroup([graph.get_edge_by_name(start, end) for start, end in [('B', 'E')]])
            # large_group_edges = GraphEdgesGroup([graph.get_edge_by_name(start, end) for start, end in [('A', 'D'), ('C', 'F'), ('D', 'F'), ('D', 'G')]])
            # small_group_nodes = GraphNodesGroup([graph.get_node_by_name('B'), graph.get_node_by_name('E')])
            # large_group_nodes = GraphNodesGroup([graph.get_node_by_name('A'), graph.get_node_by_name('C'), graph.get_node_by_name('D'), graph.get_node_by_name('F'), graph.get_node_by_name('G')])
            # self.play(green_edge_1.highlight(color=GREEN), small_group_edges.highlight(color=PINK4), large_group_edges.highlight(color=PINK4), small_group_nodes.fill(stroke_color=PINK3), large_group_nodes.fill(stroke_color=PINK3))
            # self.wait()
            ## change name
            # self.play(small_group_edges.highlight(color='#9BA3EC'), small_group_nodes.fill(fill_color='#9BA3EC'), small_group_nodes.initialize_keys("♥", color=BACKGROUND))
            # self.wait()
            # self.play(large_group_edges.highlight(color='#FDF8CA'), large_group_nodes.fill(fill_color='#FDF8CA'), large_group_nodes.initialize_keys("★", color=BACKGROUND))
            # self.wait()
            # self.play(green_edge_1.dehighlight(), green_edge_2.highlight(color=GREEN))
            # self.wait()
            union_find = Character("Union-Find", "union_find.png")
            # self.play(union_find.fade_in_by_position(scale=0.48, x_offset=-5.85, y_offset=0, together=True))
            # self.wait()
            # self.play(union_find.next_to(kruskal.mobject, DOWN))
            # self.wait()
            # self.play(graph.restore_graph(), kruskal_code_block.fade_out(), l.fade_out(), small_group_nodes.delete_keys(), large_group_nodes.delete_keys())

            ### Animation 4 kruskal 2 ###
            # self.wait()
            # kruskal_uf_code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
            # self.play(kruskal_uf_code_block.create(x_offset=-2.7), graph.shift(x_offset=-0.2))
            # l = Legend({
            #     ("MULTICOLORS", "CIRCLE"): "MST so far", 
            #     ('LINE', GREEN, GREEN): "curr min edge"
            # }, is_horizontal=True)
            # l.mobjects.next_to(kruskal.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(l.fade_in())
            # self.mst_kruskal_union_find(graph, code_block=kruskal_uf_code_block, create_legend=False, union_find_object=union_find)
            # self.play(kruskal_uf_code_block.fade_out(), l.fade_out(), graph.fade_out())

            ### Animation 5 map kruskal, union find, prim ###
            # self.play(concepts_map.show_only([kruskal]))
            # self.play(kruskal.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE*0.8))
            # self.play(union_find.fade_in_by_position(scale=CHARACTER_TO_EDGE_SCALE*0.8, x_offset=0.7, y_offset=0))
            # self.play(union_find.next_to(kruskal.mobject, DOWN))
            # self.wait()
            # kruskal_and_uf = ObjectGroup([kruskal, union_find])
            # self.play(kruskal_and_uf.next_to_company(kruskal.company, scale=1/0.48))
            # self.play(concepts_map.show_all())
            # concepts_map.add(union_find)
            # self.play(union_find.shift(y_offset=-1.2))
            # self.play(concepts_map.center(scale=0.8))
            # self.wait()
            # self.play(concepts_map.add_edge(kruskal, union_find, weight='Help'))
            # self.wait()
            # self.play(kruskal.add_time_complexity('O(E·lgV)'))
            # self.wait()
            # self.play(concepts_map.shift(x_offset=-2.5))
            # self.wait()
            # prim = Character('Prim', 'prim.png')
            # self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            # concepts_map.add(prim)
            # self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.wait()
            # self.play(concepts_map.add_edge(kruskal, prim, weight='Colleague'))
            # self.wait()
            # self.play(concepts_map.center())
            # self.wait()
            # self.play(concepts_map.show_only([prim]))
            # self.wait()
            # self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            # self.wait()

            ### Animation 6 prim and heap ###
            # self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            # self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.play(concepts_map.show_only([prim]))
            # self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            # self.wait()
            # prim_code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
            # l = Legend({
            #     (PINK4, PINK4): "MST so far", 
            #     ('LINE', GREEN, GREEN): "curr min edge"
            # }, is_horizontal=True)
            # l.mobjects.next_to(prim.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(prim_code_block.create(x_offset=-2.7))
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # graph.save_state()
            # self.play(l.fade_in())
            # self.wait()
            # self.mst_prim_basic(graph, code_block=prim_code_block, create_legend=False)
            # self.wait()
            # self.play(prim_code_block.highlight(7, 2))  # Go to the code to show where to get the min edge
            # min_heap = Character("Min Heap", "min_heap.png")
            # current_scale = prim.scale
            # self.wait()
            # self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-5.86, y_offset=-0.2, together=True))
            # self.wait()
            # self.play(min_heap.next_to(prim.mobject, DOWN))
            # self.wait()
            # self.play(prim_code_block.fade_out(), l.fade_out(), graph.restore())
            

            ### Animation 7 prim 2 ###
            # self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            # self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.play(concepts_map.show_only([prim]))
            # self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            # current_scale = prim.scale
            # self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-6, y_offset=-0.2))
            # self.play(min_heap.next_to(prim.mobject, DOWN))
            # prim_heap_code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            # l = Legend({
            #     (PINK4, PINK4): "MST so far", 
            #     (PINK4, PINK5): "curr min node",
            #     (BACKGROUND, GREEN): "decrease key"
            # }, is_horizontal=True)
            # l.mobjects.next_to(prim.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.wait()
            # self.play(prim_heap_code_block.create(x_offset=-2.8, y_offset=-0.4), graph.shift(x_offset=-0.6))
            # self.play(l.fade_in())
            # self.mst_prim_queue(graph, source='A', code_block=prim_heap_code_block, create_legend=False, hide_details=True, character_object=min_heap)
            # self.wait()
            # self.play(prim_heap_code_block.fade_out(), l.fade_out(), graph.fade_out())
            

            ### Animation 8 back to map (need uncomment Animation 5) ###
            # current_scale = prim.scale
            # self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-6, y_offset=-0.2))
            # self.wait()
            # self.play(min_heap.next_to(prim.mobject, DOWN))
            # self.wait()
            # prim_and_mh = ObjectGroup([prim, min_heap])
            # self.play(prim_and_mh.next_to_company(prim.company, scale=1/0.6))
            # self.wait()
            # self.play(concepts_map.show_all())
            # concepts_map.add(min_heap)
            # self.play(min_heap.align_to(union_find.mobject, UP))
            # self.wait()
            # self.play(concepts_map.add_edge(prim, min_heap, weight='Help'))
            # self.wait()
            # self.play(prim.add_time_complexity('O(E+V·lgV)'))
            # self.wait()
            # self.clear()
            # self.wait()


        def fairytale_algorithm_ch():
            ##################################
            # Chinese
            ##################################
            def get_text_below(string, graph):
                return get_text(string, weight=NORMAL).next_to(graph.mobject, DOWN, buff=0.5)
            def get_text_left(string):
                return get_text(string, weight=BOLD, font_size=20).to_edge(LEFT, buff=1)
            def get_text_left_next(string, mobject_above):
                return get_text_left(string, graph).next_to(mobject_above, DOWN, buff=0.3).align_to(mobject_above, LEFT)
            title_mobject = show_title_for_demo("算法童话")
            self.add(title_mobject)

            ### Animation 1 MST ###
            kruskal = Character("Kruskal", "kruskal.png")
            concepts_map = ConceptsMap([kruskal])
            self.play(kruskal.fade_in())
            self.wait()
            self.play(concepts_map.add_company("MST ®", kruskal, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.wait()
            # self.play(concepts_map.show_only([kruskal.company]))
            # self.play(kruskal.company.move_to_top_right())
            # self.wait()
            # new_position = scale_position(FAIRYTALE_POSITION, 2, 2)
            # graph = GraphObject(FAIRYTALE_MAP, new_position)
            # self.play(graph.fade_in())
            # self.wait()
            # mst_edges_group = graph.get_mst_edges('A')
            # mst_nodes_group = graph.get_mst_nodes()
            # self.play(mst_edges_group.highlight(width=EDGE_HIGHLIGHT_STROKE_WIDTH), mst_nodes_group.fill())
            # formula = get_text_below("4 + 7 + 2 + 1 + 5 + 3 = 22", graph)
            # self.wait()
            # self.play(Write(formula))
            # self.wait()
            # self._remove_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # mst_title = get_text("最小生成树 (Minimum Spanning Tree)", weight=BOLD).to_edge(UP, buff=0.9)
            # self.play(Write(mst_title))
            # self.wait()
            # self.play(Unwrite(formula))
            # self.wait()
            # self._restore_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.play(graph.shift(x_offset=3))
            # outline = LeftSideOutline("1. 覆盖所有的点", buff=2)
            # self.wait()
            # self.play(outline.show("1. 覆盖所有的点"))
            # self.wait()
            # self.play(mst_edges_group.dehighlight())
            # self.wait()
            # self.play(outline.add("2. 边的权重之和越小越好"))
            # self.play(mst_edges_group.highlight(width=EDGE_HIGHLIGHT_STROKE_WIDTH))
            # self.wait()
            # self.play(outline.add("4 + 7 + 2 + 1 + 5 + 3 = 22", is_secondary=True))
            # self.wait()
            # self._remove_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # self._restore_edges(graph, mst_edges_group.edges_array, is_sync=True)
            # self.wait()
            # self.play(graph.fade_out(), outline.fade_out(), FadeOut(mst_title))
            # self.wait()
            # self.play(kruskal.company.back_from_top_right())
            # self.play(concepts_map.show_all())
            # self.wait()

            ### Animation 2 Kruskal ###
            # self.wait()
            # self.play(concepts_map.show_only([kruskal]))
            # self.play(kruskal.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE*0.8))
            # self.wait()
            # kruskal_code_block = CodeBlock(CODE_FOR_KRUSKAL)
            # l = Legend({
            #     (PINK4, PINK4): "最小生成树", 
            #     ('LINE', GREEN, GREEN): "当前最小边"
            # }, is_horizontal=True)
            # l.mobjects.next_to(kruskal.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(kruskal_code_block.create(x_offset=-2.6))
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.play(l.fade_in())
            # self.mst_kruskal_basic(graph, code_block=kruskal_code_block, create_legend=False)
            # self.wait()

            ### Animation 3 add same label ###
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.play(l.fade_in())
            # self.wait()
            # self.play(kruskal_code_block.highlight(4, 2))
            # self.wait()
            # green_edge_1 = graph.get_edge_by_name('B', 'C')
            # green_edge_2 = graph.get_edge_by_name('C', 'D')
            # small_group_edges = GraphEdgesGroup([graph.get_edge_by_name(start, end) for start, end in [('B', 'E')]])
            # large_group_edges = GraphEdgesGroup([graph.get_edge_by_name(start, end) for start, end in [('A', 'D'), ('C', 'F'), ('D', 'F'), ('D', 'G')]])
            # small_group_nodes = GraphNodesGroup([graph.get_node_by_name('B'), graph.get_node_by_name('E')])
            # large_group_nodes = GraphNodesGroup([graph.get_node_by_name('A'), graph.get_node_by_name('C'), graph.get_node_by_name('D'), graph.get_node_by_name('F'), graph.get_node_by_name('G')])
            # self.play(green_edge_1.highlight(color=GREEN), small_group_edges.highlight(color=PINK4), large_group_edges.highlight(color=PINK4), small_group_nodes.fill(stroke_color=PINK3), large_group_nodes.fill(stroke_color=PINK3))
            # self.wait()
            # change name
            # self.play(small_group_edges.highlight(color='#9BA3EC'), small_group_nodes.fill(fill_color='#9BA3EC'), small_group_nodes.initialize_keys("♥", color=BACKGROUND))
            # self.wait()
            # self.play(large_group_edges.highlight(color='#FDF8CA'), large_group_nodes.fill(fill_color='#FDF8CA'), large_group_nodes.initialize_keys("★", color=BACKGROUND))
            # self.wait()
            # self.play(green_edge_1.dehighlight(), green_edge_2.highlight(color=GREEN))
            # self.wait()
            union_find = Character("Union-Find", "union_find.png")
            # self.play(union_find.fade_in_by_position(scale=0.48, x_offset=-5.85, y_offset=0, together=True))
            # self.wait()
            # self.play(union_find.next_to(kruskal.mobject, DOWN))
            # self.wait()
            # self.play(graph.restore_graph(), kruskal_code_block.fade_out(), l.fade_out(), small_group_nodes.delete_keys(), large_group_nodes.delete_keys())

            ### Animation 4 kruskal 2 ###
            # self.wait()
            # kruskal_uf_code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
            # self.play(kruskal_uf_code_block.create(x_offset=-2.7), graph.shift(x_offset=-0.2))
            # l = Legend({
            #     ("MULTICOLORS", "CIRCLE"): "最小生成树", 
            #     ('LINE', GREEN, GREEN): "当前最小边"
            # }, is_horizontal=True)
            # l.mobjects.next_to(kruskal.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(l.fade_in())
            # self.mst_kruskal_union_find(graph, code_block=kruskal_uf_code_block, create_legend=False, union_find_object=union_find)
            # self.play(kruskal_uf_code_block.fade_out(), l.fade_out(), graph.fade_out())

            ### Animation 5 map kruskal, union find, prim ###
            self.play(concepts_map.show_only([kruskal]))
            self.play(kruskal.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE*0.8))
            self.play(union_find.fade_in_by_position(scale=CHARACTER_TO_EDGE_SCALE*0.8, x_offset=0.7, y_offset=0))
            self.play(union_find.next_to(kruskal.mobject, DOWN))
            # self.wait()
            kruskal_and_uf = ObjectGroup([kruskal, union_find])
            self.play(kruskal_and_uf.next_to_company(kruskal.company, scale=1/0.48))
            # self.play(concepts_map.show_all())
            concepts_map.add(union_find)
            self.play(union_find.shift(y_offset=-1.2))
            self.play(concepts_map.center(scale=0.8))
            # self.wait()
            self.play(concepts_map.add_edge(kruskal, union_find, weight='帮助'))
            # self.wait()
            self.play(kruskal.add_time_complexity('O(E·lgV)'))
            # self.wait()
            self.play(concepts_map.shift(x_offset=-2.5))
            # self.wait()
            prim = Character('Prim', 'prim.png')
            self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            concepts_map.add(prim)
            self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            self.wait()
            self.play(concepts_map.add_edge(kruskal, prim, weight='同事'))
            self.wait()
            self.play(concepts_map.center())
            self.wait()
            self.play(concepts_map.show_only([prim]))
            self.wait()
            self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            self.wait()

            ### Animation 6 prim and heap ###
            # self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            # self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.play(concepts_map.show_only([prim]))
            # self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            # self.wait()
            # prim_code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
            # l = Legend({
            #     (PINK4, PINK4): "最小生成树", 
            #     ('LINE', GREEN, GREEN): "当前边"
            # }, is_horizontal=True)
            # l.mobjects.next_to(prim.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(prim_code_block.create(x_offset=-2.7))
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # graph.save_state()
            # self.play(l.fade_in())
            # self.wait()
            # self.mst_prim_basic(graph, code_block=prim_code_block, create_legend=False)
            # self.wait()
            # self.play(prim_code_block.highlight(7, 2))  # Go to the code to show where to get the min edge
            min_heap = Character("Min Heap", "min_heap.png")
            # current_scale = prim.scale
            # self.wait()
            # self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-5.86, y_offset=-0.2, together=True))
            # self.wait()
            # self.play(min_heap.next_to(prim.mobject, DOWN))
            # self.wait()
            # self.play(prim_code_block.fade_out(), l.fade_out(), graph.restore())
            

            ### Animation 7 prim 2 ###
            # self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            # self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            # self.play(concepts_map.show_only([prim]))
            # self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            # current_scale = prim.scale
            # self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-6, y_offset=-0.2))
            # self.play(min_heap.next_to(prim.mobject, DOWN))
            # prim_heap_code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            # l = Legend({
            #     (PINK4, PINK4): "最小生成树", 
            #     (PINK4, PINK5): "当前最小的点",
            #     (BACKGROUND, GREEN): "键值降低的点"
            # }, is_horizontal=True)
            # l.mobjects.next_to(prim.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            # self.play(graph.fade_in(scale=0.9, x_offset=3.7, y_offset=-0.3))
            # self.wait()
            # self.play(prim_heap_code_block.create(x_offset=-2.8, y_offset=-0.4), graph.shift(x_offset=-0.6))
            # self.play(l.fade_in())
            # self.mst_prim_queue(graph, source='A', code_block=prim_heap_code_block, create_legend=False, hide_details=True, character_object=min_heap)
            # self.wait()
            # self.play(prim_heap_code_block.fade_out(), l.fade_out(), graph.fade_out())
            

            ### Animation 8 back to map (need uncomment Animation 5) ###
            current_scale = prim.scale
            self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-6, y_offset=-0.2))
            self.wait()
            self.play(min_heap.next_to(prim.mobject, DOWN))
            self.wait()
            prim_and_mh = ObjectGroup([prim, min_heap])
            self.play(prim_and_mh.next_to_company(prim.company, scale=1/0.6))
            self.wait()
            self.play(concepts_map.show_all())
            concepts_map.add(min_heap)
            self.play(min_heap.align_to(union_find.mobject, UP))
            self.wait()
            self.play(concepts_map.add_edge(prim, min_heap, weight='帮助'))
            self.wait()
            self.play(prim.add_time_complexity('O(E+V·lgV)'))
            self.wait()
            self.play(concepts_map.show_only([kruskal, prim]))
            self.play(kruskal.shift(scale=0.8, x_offset=-3.5, y_offset=0), prim.shift(scale=0.8, x_offset=3.5, y_offset=0))
            self.wait()
            self.play(kruskal.shift(scale=1/0.8, x_offset=3.5, y_offset=0), prim.shift(scale=1/0.8, x_offset=-3.5, y_offset=0))
            self.play(concepts_map.show_all())
            self.wait()
            self.clear()

        def fairytale_algorithm_dijkstra_en():
            title_mobject = show_title_for_demo("算法童话")
            self.add(title_mobject)

            ### Get the recent map ###
            kruskal = Character("Kruskal", "kruskal.png")
            concepts_map = ConceptsMap([kruskal])
            self.play(kruskal.fade_in())
            self.wait()
            self.play(concepts_map.add_company("MST ®", kruskal, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            union_find = Character("Union-Find", "union_find.png")
            self.play(concepts_map.show_only([kruskal]))
            self.play(kruskal.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE*0.8))
            self.play(union_find.fade_in_by_position(scale=CHARACTER_TO_EDGE_SCALE*0.8, x_offset=0.7, y_offset=0))
            self.play(union_find.next_to(kruskal.mobject, DOWN))
            kruskal_and_uf = ObjectGroup([kruskal, union_find])
            self.play(kruskal_and_uf.next_to_company(kruskal.company, scale=1/0.48))
            concepts_map.add(union_find)
            self.play(union_find.shift(y_offset=-1.2))
            self.play(concepts_map.center(scale=0.8))
            self.play(concepts_map.add_edge(kruskal, union_find, weight='帮助'))
            self.play(kruskal.add_time_complexity('O(E·lgV)'))
            self.play(concepts_map.shift(x_offset=-2.5))
            prim = Character('Prim', 'prim.png')
            self.play(prim.fade_in(scale=0.8, object=kruskal, direction=RIGHT, buff=1.5))
            concepts_map.add(prim)
            self.play(concepts_map.add_company("MST ®", prim, stroke_color=MST_COMPANY[0], fill_color=MST_COMPANY[1]))
            self.play(concepts_map.add_edge(kruskal, prim, weight='同事'))
            self.play(concepts_map.center())
            self.play(concepts_map.show_only([prim]))
            self.play(prim.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            min_heap = Character("Min Heap", "min_heap.png")
            current_scale = prim.scale
            self.play(min_heap.fade_in_by_position(scale=current_scale, x_offset=-6, y_offset=-0.2))
            self.play(min_heap.next_to(prim.mobject, DOWN))
            prim_and_mh = ObjectGroup([prim, min_heap])
            self.play(prim_and_mh.next_to_company(prim.company, scale=1/0.6))
            self.play(concepts_map.show_all())
            concepts_map.add(min_heap)
            self.play(min_heap.align_to(union_find.mobject, UP))
            self.play(concepts_map.add_edge(prim, min_heap, weight='帮助'))
            self.play(prim.add_time_complexity('O(E+V·lgV)'))
            self.play(concepts_map.show_only([kruskal, prim]))
            self.play(concepts_map.show_all())

            ### Create Dijkstra and develop the map ###
            dijkstra = Character("Dijkstra", "dijkstra.png")
            self.play(dijkstra.fade_in(scale=0.8, object=prim, direction=RIGHT, buff=1.5))
            concepts_map.add(dijkstra)
            self.play(concepts_map.add_company("短路 ®", dijkstra, stroke_color=SP_COMPANY[0], fill_color=SP_COMPANY[1]))
            self.play(concepts_map.add_edge(prim, dijkstra, weight='兄弟'))
            self.play(concepts_map.center())

            ### 短路 VS MST
            self.play(concepts_map.show_only([dijkstra.company]))
            self.play(dijkstra.company.move_to_top_right())
            print(dijkstra.company.scale)
            new_position = scale_position(FAIRYTALE_POSITION, 2, 2)
            graph = GraphObject(FAIRYTALE_MAP, new_position)
            self.play(graph.fade_in())
            nodes_list = graph.get_nodes()
            edges_list = [graph.get_edge_by_name(start, end) for start, end in [('A', 'B'), ('A', 'C'), ('A', 'D'), ('D', 'F'), ('D', 'G'), ('E', 'F')]]
            subgraph = SubGraph(edges_list, nodes_list)
            self.play(subgraph.highlight(node_stroke_color=PINK3))
            graph_left = GraphObject(FAIRYTALE_MAP, new_position)
            temp_mst_title = get_text('MST ®', weight=ULTRAHEAVY, font_size=COMPANY_FONT_SIZE_TOP_RIGHT, color=MST_COMPANY[0]).move_to(3 * UP + 3 * LEFT)
            self.play(graph.shift(3), dijkstra.company.move_to(3, 3), graph_left.fade_in(-3, 0), graph_left.mst_highlight(), FadeIn(temp_mst_title))
            temp_edges_text = get_text('Edges = {AD, BC, BE, CF, DG, DF}', weight=ULTRAHEAVY, font_size=COMPANY_FONT_SIZE_TOP_RIGHT, color=GRAY).next_to(graph_left.mobject, DOWN, buff=0.5)
            self.play(Write(temp_edges_text))
            node2last = {'B': 'A', 'C': 'A', 'D': 'A', 'E': 'F', 'F': 'D', 'G': 'D'}
            last_names_fadein = []
            for node_name, last_node_name in list(node2last.items()):
                node = graph.get_node_by_name(node_name)
                last_names_fadein.append(node.fade_in_label(last_node_name, font_size=15))
            self.play(*last_names_fadein)
            self.play(FadeOut(temp_edges_text), FadeOut(temp_mst_title), graph_left.fade_out(), graph.fade_out(), dijkstra.company.back_from_top_right())
            
            ### Map
            self.play(concepts_map.show_all())
            self.play(concepts_map.add_edge(min_heap, dijkstra, weight='帮助'))
            self.play(concepts_map.show_only([dijkstra, min_heap]))
            self.play(dijkstra.move_to_top_right(scale=CHARACTER_TO_EDGE_SCALE))
            self.play(min_heap.next_to(dijkstra.mobject, DOWN, scale=CHARACTER_TO_EDGE_SCALE))

            ### Graph
            dijkstra_code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
            self.play(dijkstra_code_block.create(-2.9, -0.2))
            self.play(FadeIn(graph.mobject.scale(0.9).move_to(3.3*RIGHT+0.4*DOWN)))
            l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "当前最小的点", (BACKGROUND, GREEN): "键值降低的点"}, is_horizontal=True)
            l.mobjects.next_to(dijkstra.mobject, LEFT, buff=LEGEND_CHARACTER_BUFF)
            self.play(l.animation)
            # self.shortest_paths_dijkstra(graph, source='A', code_block=dijkstra_code_block, create_legend=False, hide_details=True)
#             self.play(test_code.replace(9, """              RELAX(u, v, weight)
# }
# RELAX(u, v, weight) {
#     if v.key > u.key + weight(u, v)
#         v.key = u.key + weight(u, v)
#         v.previous = u
# }
# """))


        # fairytale_algorithm_en()
        # self.play(endding('EN'))
        # self.play(fairytale_header())

        # self.play(fairytale_header(language='CH'))
        # fairytale_algorithm_ch()
        # self.play(endding('CH'))

        # re = Ellipse(width=1.5, height=0.8)
        # rl = Line((0,0,0), (0.15,0.15,0)).shift(0.52*DOWN+0.75*LEFT)
        # rtext1 = get_text('勿拉踩', color=GRAY, font_size=SMALL_FONT_SIZE, weight=ULTRAHEAVY).move_to(re)
        # rdialogue = VGroup(re, rl).set_stroke(color=GRAY)
        # rdialogue += rtext1
        # self.play(Write(rdialogue))
        # self.wait(3)
        # self.play(Unwrite(rdialogue))


        # fairytale_algorithm_dijkstra_en()
        # new_position = scale_position(FAIRYTALE_POSITION, 2, 2)
        # graph = GraphObject(FAIRYTALE_MAP, new_position)
        # self.play(FadeIn(graph.mobject.shift(0.5*DOWN)))
        # self.shortest_paths_dijkstra(graph, source='A', create_legend=False, animate_code_block=False, speed=1, hide_details=True)


        




        

        

        

