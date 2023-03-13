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


MAP_6_NODES_HORIZONTAL = {'E': {'F': 1}, 'D': {'E': 1}, 'C': {'D': 1}, 'B': {'C': 1}, 'Src': {'B': 1}, }
POSITION_6_NODES_HORIZONTAL = {'Src': (0, 0), 'B': (1, 0), 'C': (2, 0), 'D': (3, 0), 'E': (4, 0), 'F': (5, 0)}



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
        code_block = CodeBlock(CODE2_FOR_BFS)
        self.add(code_block.code)
        self.bfs(graph, 'A')

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


        ### Prim-queue
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.mobject.scale(0.9).shift(3.3*RIGHT)))
        # self.mst_prim_queue(graph, source='A', code_block=code_block, hide_details=True)
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


        

        

        

