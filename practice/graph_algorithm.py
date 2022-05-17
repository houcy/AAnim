from manim import *
from style import *
from code_constant import *
from graph import GraphObject
from code_block import CodeBlock
from legend import Legend
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *
from scale_position import *
from union_find import UnionFind
from color_generator import ColorGenerator
import copy

MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
POSITION1 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

MAP_MST = {'A': {'B': 4, 'H': 8}, 'B': {'A': 4, 'C': 8, 'H': 11}, 'H': {'A': 8, 'B': 11, 'G': 1, 'I': 7}, 'C': {'B': 8, 'D': 7, 'I': 2, 'F': 4}, 'D': {'C': 7, 'F': 14, 'E': 9}, 'I': {'C': 2, 'G': 6, 'H': 7}, 'F': {'C': 4, 'G': 2, 'D': 14, 'E': 10}, 'G': {'I': 6, 'F': 2, 'H': 1}, 'E': {'D': 9, 'F': 10}}
POSITION_MST = {'A': (0.7, 0.6), 'B': (1.4402327576560112, 2.1393785668991754), 'H': (2.5, -0.1), 'C': (2.9889216307956286, 3.1086575403782315), 'D': (4.368905964414935, 4.2), 'I': (3.082024693200045, 1.457062926629117), 'F': (4.744899101048156, 2.3), 'G': (4.4, 0.5), 'E': (6.0, 3.649819090603902)}

MAP_HARD = {'A': {'B': 7, 'D': 8, 'G': 8}, 'B': {'A': 7, 'C': 5, 'D': 6}, 'C': {'B': 5, 'D': 5, 'E': 7}, 'D': {'C': 5, 'E': 3, 'A': 8, 'B': 6, 'F': 5, 'G': 9}, 'E': {'D': 3, 'F': 2, 'C': 7, 'N': 8, 'M': 6}, 'F': {'E': 2, 'G': 5, 'D': 5, 'M': 7}, 'G': {'F': 5, 'H': 5, 'A': 8, 'D': 9, 'M': 6}, 'H': {'G': 5, 'I': 5, 'M': 9}, 'P': {'Q': 5, 'O': 5, 'K': 8}, 'Q': {'P': 5, 'R': 5, 'K': 6, 'T': 7}, 'I': {'H': 5, 'J': 3, 'M': 6, 'L': 6, 'K': 9}, 'J': {'I': 3, 'K': 5, 'U': 6, 'T': 6}, 'K': {'J': 5, 'L': 3, 'P': 8, 'O': 5, 'I': 9, 'Q': 6, 'T': 9, 'U': 6}, 'L': {'K': 3, 'M': 3, 'O': 9, 'I': 6}, 'M': {'L': 3, 'N': 3, 'E': 6, 'F': 7, 'G': 6, 'O': 8, 'H': 9, 'I': 6}, 'N': {'M': 3, 'O': 2, 'E': 8}, 'O': {'N': 2, 'P': 5, 'L': 9, 'M': 8, 'K': 5}, 'R': {'Q': 5, 'S': 2, 'T': 5}, 'S': {'R': 2, 'T': 6}, 'T': {'R': 5, 'U': 3, 'K': 9, 'J': 6, 'S': 6, 'Q': 7}, 'U': {'T': 3, 'K': 6, 'J': 6}}
POSITION_HARD = {'A': (-4, -1), 'B': (-4, 0), 'C': (-4, 1), 'D': (-3, 0), 'E': (-2, 1), 'F': (-2, 0), 'G': (-2, -1), 'H': (-1, -1), 'I': (0, -1), 'J': (1, -1), 'K': (1, 0), 'L': (0, 0), 'M': (-1, 0), 'N': (-1, 1), 'O': (0, 1), 'P': (1, 1), 'Q': (2, 1), 'R': (3, 1), 'S': (4, 1), 'T': (3, 0), 'U': (3, -1)}

DIMAP_DIJKASTRA_CLRS = {'A': {'B': 10, 'E': 5}, 'B': {'C': 1, 'E': 2}, 'C': {'D': 4}, 'D': {'C': 6}, 'E': {'C': 9, 'D': 2, 'B': 3}}
DIPOSITION_DIJKASTRA_CLRS = {'A': (1, 2), 'B': (2, 1), 'E': (0, 1), 'C': (2, 0), 'D': (0, 0)}

class Show(Scene):
    # def __init__(self, adjacency_list, position, is_directed):
    #     self.adjacency_list = adjacency_list
    #     self.position = position
    #     self.is_directed = is_directed
    #     super().__init__()

    def _remove_edges(self, graph, selected_edges, speed=1):
        for edge in graph.edges:
            if edge not in selected_edges:
                self.play(edge.fade_out(), run_time=0.3*speed)

    def flash(self, temp_group):
        self.play(*[m.animate.set_color(BACKGROUND) for m in temp_group])
        self.play(*[m.animate.set_color(GRAY) for m in temp_group])
    
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
                self.play(l.mobjects.animate.shift(UP), graph.graph_mobject.animate.shift(1 * UP))
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
        l.mobjects.next_to(graph.graph_mobject, RIGHT, buff=0.5)
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
            _, graph_y, _ = graph.graph_mobject.get_center()
            topo_vgroup = VGroup()
            for node in post_order:
                topo_vgroup += node.mobject
            _, topo_y, _ = topo_vgroup.get_center()
            self.play(graph.graph_mobject.animate.move_to(graph_y * UP), topo_vgroup.animate.move_to(topo_y * UP))
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
        self.play(FadeOut(topo_vgroup, graph.graph_mobject))

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
    
    def bfs(self, graph, s):
        """
        BFS: traverse the tree starting from source s. 
        Mark 3 colors for curr level, next level, and finished
        """
        l = Legend({PINK1: "curr level", PINK3: "next level", BLUE1: "finished"})
        l.mobjects.next_to(graph.graph_mobject, RIGHT, buff=0.5)
        self.play(l.animation)
        code_block = CodeBlock(CODE2_FOR_BFS)
        self.add(code_block.code)
        self.play(code_block.highlight(1))
        discovered = set()
        s_node = graph.value2node[s]
        curr_level = []
        self.play(code_block.highlight(2))
        next_level = []
        self.play(code_block.highlight(3))
        curr_level.append(s_node)
        self.play(code_block.highlight(4))
        discovered.add(s_node)
        self.play(code_block.highlight(5))
        self.play(s_node.mark_pink1())
        while curr_level:
            self.play(code_block.highlight(6))
            for curr in curr_level:
                self.play(code_block.highlight(7))
                self.play(curr.highlight_stroke())
                for neighbor in curr.neighbor2edge:
                    self.play(code_block.highlight(8))
                    if neighbor not in discovered:
                        self.play(code_block.highlight(9))
                        next_level.append(neighbor)
                        self.play(code_block.highlight(10))
                        discovered.add(curr)
                        self.play(code_block.highlight(11))
                        self.play(neighbor.mark_pink3())
                self.play(curr.highlight_stroke(PINK1))
                self.wait(1)
                self.play(code_block.highlight(12))
                self.play(curr.mark_blue1())
            self.play(code_block.highlight(13))
            # self.play(self.mark_levels(curr_level, BLUE1))
            curr_level = next_level
            self.play(code_block.highlight(14))
            self.play(self.mark_levels(curr_level, PINK1))
            next_level = []
            self.play(code_block.highlight(15))
        self.play(code_block.highlight(16))

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
        # l.mobjects.next_to(graph.graph_mobject, DOWN, buff=0.3)
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
            self.play(Create(code_block.code))
        # self.play(code_block.highlight(1)) if animate_code_block else None
        selected_edges = set()
        selected = set()
        first_node_key = list(graph.adjacency_list.keys())[0]
        first_node = graph.value2node[first_node_key]
        # self.play(code_block.highlight(2, 3), run_time=speed) if animate_code_block else None
        # self.play(code_block.highlight(5), run_time=speed) if animate_code_block else None
        selected.add(first_node)
        self.play(first_node.color(fill_color=PINK4), run_time=speed)
        while len(selected) != len(graph.adjacency_list):
            # self.play(code_block.highlight(6), run_time=speed) if animate_code_block else None
            # self.wait(0.8)
            minimum = float("inf")
            minimum_node = None
            minimum_edge = None
            neighbor_edges = GraphEdgesGroup()
            for v in selected:
                for e in v.edges:
                    u = e.get_the_other_end(v)
                    if u not in selected:
                        neighbor_edges.add(e)
                        if graph.adjacency_list[u.value][v.value] < minimum:
                            minimum = graph.adjacency_list[u.value][v.value]
                            minimum_node = u
                            minimum_edge = e
            selected_edges.add(minimum_edge)
            # show all available edges
            # self.play(code_block.highlight(7, 2), run_time=speed) if animate_code_block else None
            self.play(neighbor_edges.highlight(BACKGROUND), run_time=1.3*speed)
            self.wait(speed)
            self.play(neighbor_edges.dehighlight(), run_time=1.3*speed)
            # self.play(minimum_edge.highlight(), run_time=0.5*speed)
            # self.play(minimum_edge.dehighlight(), run_time=0.5*speed)
            self.play(minimum_edge.highlight(color=PINK4), run_time=0.5*speed)
            self.wait()
            # show the shortest edge - the next edge to add
            # self.play(code_block.highlight(9, 3), run_time=speed) if animate_code_block else None
            selected.add(minimum_node)
            self.play(minimum_node.color(fill_color=PINK4), run_time=speed)
        # self.play(code_block.highlight(12), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, selected_edges)
        # self.play(code_block.highlight(13), run_time=speed) if animate_code_block else None
        

    def mst_prim_queue(self, graph, source=None, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
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
            l = Legend({(PINK4, PINK4): "MST so far", (PINK4, PINK5): "v"}, is_horizontal=show_horizontal_legend)
            l.mobjects.next_to(graph.graph_mobject, UP, buff=0.3)
            # l.mobjects.move_to(2*UP+1.5*RIGHT)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            self.play(Create(code_block.code))
        self.play(code_block.highlight(1), run_time=2*speed) if animate_code_block else None
        self.play(code_block.highlight(2), run_time=2*speed) if animate_code_block else None
        self.play(code_block.highlight(3), run_time=2*speed) if animate_code_block else None
        self.play(code_block.highlight(4), run_time=2*speed) if animate_code_block else None
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        self.play(code_block.highlight(5), run_time=speed) if animate_code_block else None
        # Accumulate animations for all nodes and show them at once
        transforms = []
        for node in graph.value2node.values():
            node.initialize_key(float('inf'), show_value=False)
            transforms += node.animations
        unreach_nodes_group = GraphNodesGroup(unreach)
        self.play(*transforms)
        self.play(code_block.highlight(6), run_time=speed) if animate_code_block else None
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0), run_time=1.5*speed)
        while unreach:
            # Show group of unreached nodes
            self.play(code_block.highlight(7), run_time=speed) if animate_code_block else None
            self.play(code_block.highlight(8), run_time=speed) if animate_code_block else None
            # Flash candidates
            self.wait()
            self.play(unreach_nodes_group.color(stroke_color=GRAY, key_color=BACKGROUND), run_time=1.2*speed)
            self.play(unreach_nodes_group.color(stroke_color=GRAY, key_color=GRAY), run_time=1.2*speed)
            # Color the min node
            v = extract_min_node(unreach)
            self.play(v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, has_key=True))
            # Get the min edge
            self.play(code_block.highlight(9), run_time=speed) if animate_code_block else None
            if v in min_edge:
                edges.append(min_edge[v])
                self.play(code_block.highlight(10), run_time=speed) if animate_code_block else None
                self.wait(speed)
                self.play(min_edge[v].highlight(color=PINK4), run_time=0.5*speed)
                self.play(min_edge[v].dehighlight(), run_time=0.5*speed)
                self.play(min_edge[v].highlight(color=PINK4), run_time=0.5*speed)
                self.wait(speed)
            # Decrease key and save the min edge
            # Full version - playing each for loop one by one
            if not hide_details:
                for u in v.neighbors:
                    if u in unreach:
                        self.play(code_block.highlight(11), run_time=speed) if animate_code_block else None
                        self.play(code_block.highlight(12, 2), run_time=speed) if animate_code_block else None
                        edge_v_u = v.neighbor2edge[u]
                        # Flash edge_v_u.weight and u.key
                        temp_group = [edge_v_u.mobject, u.key_mobject]
                        self.play(*[m.animate.set_color(BACKGROUND) for m in temp_group], run_time=speed)
                        self.play(*[m.animate.set_color(GRAY) for m in temp_group], run_time=speed)
                        if edge_v_u.weight < u.key:
                            self.play(code_block.highlight(14), run_time=speed) if animate_code_block else None
                            self.play(u.update_key(edge_v_u.weight), run_time=speed)
                            u.key = edge_v_u.weight
                            min_edge[u] = edge_v_u
                            self.play(code_block.highlight(15), run_time=speed) if animate_code_block else None
            # Shortened version - playing all for loops at the same time
            else:
                self.play(code_block.highlight(11, 3)) if animate_code_block else None
                # Accumulate animations for all qualified mobjects and show them at once
                mobject_to_flash = []
                animations_update_key = []
                for u in v.neighbors:
                    if u in unreach:
                        edge_v_u = v.neighbor2edge[u]
                        if edge_v_u.weight < u.key:
                            mobject_to_flash += [edge_v_u.mobject["text"]["text"], edge_v_u.mobject["line"], u.key_mobject]
                            animations_update_key.append(u.update_key(edge_v_u.weight))
                            u.key = edge_v_u.weight
                            min_edge[u] = edge_v_u
                if mobject_to_flash:
                    self.play(*[m.animate.set_color(BACKGROUND) for m in mobject_to_flash], run_time=speed)
                    self.play(*[m.animate.set_color(GRAY) for m in mobject_to_flash], run_time=speed)
                if animations_update_key:
                    self.play(code_block.highlight(14), run_time=speed) if animate_code_block else None
                    self.play(*animations_update_key, run_time=1.5*speed)
                    self.play(code_block.highlight(15), run_time=speed) if animate_code_block else None
            self.play(v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True))

        self.play(code_block.highlight(16), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, edges, speed=speed)
        self.play(code_block.highlight(17), run_time=speed) if animate_code_block else None
        return edges

    ##################################
    # MST: Kruskal
    ##################################

    def mst_kruskal_basic(self, graph, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, add_sound=False):
        speed = 1 / speed
        if create_legend:
            l = Legend({(PINK2, PINK2): "MST so far", (PURPLE, PURPLE): "curr min edge"}, show_horizontal_legend=show_horizontal_legend)
            l.mobjects.next_to(graph.graph_mobject, UP, buff=0.3)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_KRUSKAL)
            self.play(Create(code_block.code))
        self.play(code_block.highlight(1), run_time=speed) if animate_code_block else None
        self.play(code_block.highlight(2), run_time=speed) if animate_code_block else None
        mst_edges = []
        mst_nodes = []
        all_edges = graph.edges
        all_edges.sort(key=lambda edge: edge.weight)
        union_find = UnionFind(graph.get_nodes())
        for i in range(0, graph.n_edges()):
            # self.wait(speed)
            self.play(code_block.highlight(3), run_time=speed) if animate_code_block else None
            min_edge = all_edges[i]
            self.wait(speed)
            self.play(min_edge.highlight(color=GREEN), run_time=0.6*speed)
            self.play(min_edge.dehighlight(), run_time=0.6*speed)
            self.play(min_edge.highlight(color=GREEN), run_time=0.6*speed)
            start_node = min_edge.start_node
            end_node = min_edge.end_node
            parent_of_start = union_find.find(start_node)
            parent_of_end = union_find.find(end_node)
            self.play(code_block.highlight(4, 2), run_time=speed) if animate_code_block else None
            # self.wait(1.5*speed)
            if parent_of_start != parent_of_end:
                self.play(code_block.highlight(6), run_time=speed) if animate_code_block else None
                animations = []
                if start_node not in mst_nodes:
                    mst_nodes.append(start_node)
                    animations.append(start_node.color(fill_color=PINK4, stroke_color=PINK3))
                if end_node not in mst_nodes:
                    mst_nodes.append(end_node)
                    animations.append(end_node.color(fill_color=PINK4, stroke_color=PINK3))
                if animations:
                    self.play(min_edge.highlight(color=PINK4), *animations, run_time=speed)
                else:
                    self.play(min_edge.highlight(color=PINK4), run_time=speed)
                union_find.union(start_node, end_node)
                mst_edges.append(min_edge)
            else:
                cycle_array = graph.get_path(start_node, end_node, mst_edges)
                # edges which are not part of the cycle will disappear, to make the cycle prominent
                non_cycle_array = [e for e in graph.edges if (e not in cycle_array and e != min_edge)]
                non_cycle_group = GraphEdgesGroup(non_cycle_array)
                self.play(non_cycle_group.disappear(include_label=True), run_time=0.8*speed)
                self.add_sound("wrong.wav") if add_sound else None
                self.wait(0.8*speed)
                self.play(non_cycle_group.appear(include_label=True), run_time=0.8*speed)
                self.play(min_edge.dehighlight(), run_time=0.8*speed)
            # self.wait(0.5*speed)
        self.play(code_block.highlight(7), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, mst_edges)
        self.play(code_block.highlight(8), run_time=speed) if animate_code_block else None
        return mst_edges


    def mst_kruskal_union_find(self, graph, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, add_sound=False):
        speed = 1 / speed
        if create_legend:
            l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", (GREEN, GREEN): "curr min edge"}, is_horizontal=show_horizontal_legend)
            # l.mobjects.move_to(2.1*UP+1.8*RIGHT)
            l.mobjects.next_to(graph.graph_mobject, UP, buff=0.3)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
            self.play(Create(code_block.code))
        # self.play(code_block.highlight(1), run_time=speed) if animate_code_block else None
        # self.wait()
        # self.play(code_block.highlight(2), run_time=speed) if animate_code_block else None
        # self.wait()
        # self.play(code_block.highlight(3, 2), run_time=speed) if animate_code_block else None
        # self.wait()
        mst_edges = []
        all_edges = graph.edges
        all_edges.sort(key=lambda edge: edge.weight)
        all_nodes = graph.get_nodes()
        union_find = UnionFind(all_nodes)
        self.play(union_find.show_set())
        for i in range(0, graph.n_edges()):
            # self.play(code_block.highlight(5, 2), run_time=speed) if animate_code_block else None
            # self.wait(1.5*speed)
            min_edge = all_edges[i]
            self.play(min_edge.highlight(color=GREEN), run_time=0.6*speed)
            self.play(min_edge.dehighlight(), run_time=0.6*speed)
            self.play(min_edge.highlight(color=GREEN), run_time=0.6*speed)
            self.wait(1*speed)
            self.play(code_block.highlight(7), run_time=speed) if animate_code_block else None
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
            if parent_of_start != parent_of_end:
                # self.play(disappear_edges_group.disappear(include_label=True), disappear_nodes_group.disappear(), run_time=0.8*speed)
                # self.add_sound("correct.wav") if add_sound else None
                # self.wait(speed)
                # self.play(disappear_edges_group.appear(include_label=True), disappear_nodes_group.appear(), run_time=0.8*speed)
                # self.play(code_block.highlight(8, 2), run_time=speed) if animate_code_block else None
                # self.wait(speed)
                self.play(union_find.union(start_node, end_node, min_edge), run_time=1.2)
                mst_edges.append(min_edge)
            else:
                # everything except current edge and start node and end node should disappear
                # self.play(disappear_edges_group.disappear(include_label=True), disappear_nodes_group.disappear(), run_time=0.8*speed)
                # self.add_sound("wrong.wav") if add_sound else None
                # self.wait(speed)
                # self.play(disappear_edges_group.appear(include_label=True), disappear_nodes_group.appear(), run_time=0.8*speed)
                self.play(min_edge.dehighlight())
            self.wait()
        self.play(code_block.highlight(10), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, mst_edges)
        self.play(code_block.highlight(11), run_time=speed) if animate_code_block else None
        union_find.destroy()
        return mst_edges       

    ##################################
    # Shortest-paths problem: Dijkstra
    ##################################

    # the version without disappearing, save in case for AB TESTING
    def shortest_paths_dijkstra_1(self, graph, source=None, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
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
            l.mobjects.next_to(graph.graph_mobject, UP, buff=0.3)
            # l.mobjects.move_to(1.8*UP+1.5*RIGHT)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
            self.play(Create(code_block.code))
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        self.play(code_block.highlight(1), run_time=speed) if animate_code_block else None
        self.wait()
        self.play(code_block.highlight(2), run_time=speed) if animate_code_block else None
        self.wait()
        self.play(code_block.highlight(3), run_time=speed) if animate_code_block else None
        self.wait()
        # Accumulate animations for all nodes and show them at once
        transforms = []
        for node in graph.value2node.values():
            node.initialize_key(float('inf'), show_value=False)
            transforms += node.animations
        unreach_nodes_group = GraphNodesGroup(unreach)
        self.play(*transforms)
        self.wait()
        self.play(code_block.highlight(4), run_time=speed) if animate_code_block else None
        self.wait()
        self.play(code_block.highlight(5), run_time=speed) if animate_code_block else None
        self.wait()
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0), run_time=1.5*speed)
        while unreach:
            # # Show group of unreached nodes
            self.play(code_block.highlight(6), run_time=speed) if animate_code_block else None
            self.wait()
            self.play(code_block.highlight(7), run_time=speed) if animate_code_block else None
            self.wait()
            # Color the min node
            v = extract_min_node(unreach)
            self.play(v.color(fill_color=PINK4, stroke_color=PINK5, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH, has_key=True))
            # Get the min edge
            if v in min_edge:
                edges.append(min_edge[v])
                self.wait(speed)
                self.play(min_edge[v].highlight(color=PINK4), width=EDGE_HIGHLIGHT_STROKE_WIDTH_FOR_DIGRAPH, run_time=0.5)
                self.play(min_edge[v].dehighlight(), run_time=0.5)
                self.play(min_edge[v].highlight(color=PINK4), width=EDGE_HIGHLIGHT_STROKE_WIDTH_FOR_DIGRAPH, run_time=0.5)
                self.wait(speed)
            # Decrease key and save the min edge
            # Full version - playing each for loop one by one
            if not hide_details:
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    self.play(code_block.highlight(8), run_time=speed) if animate_code_block else None
                    self.wait()
                    self.play(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH), edge_v_u.mobject["line"].animate.set_color(GREEN))
                    # Flash edge_v_u.weight and u.key
                    self.play(code_block.highlight(10), run_time=speed) if animate_code_block else None
                    self.wait()
                    temp_group = [edge_v_u.mobject["text"]["text"], v.key_mobject, u.key_mobject]
                    if u in unreach:
                        # if the neighbor is not a visited node
                        self.play(*[temp_group[0].animate.set_color(BACKGROUND), temp_group[1].animate.set_color(PINK4), temp_group[2].animate.set_color(BACKGROUND)], run_time=speed)
                        self.play(*[temp_group[0].animate.set_color(PINK3), temp_group[1].animate.set_color(BACKGROUND), temp_group[2].animate.set_color(GRAY)], run_time=speed)
                    else:
                        # if the neighbor is a visited node, key color should be different
                        self.play(*[temp_group[0].animate.set_color(BACKGROUND), temp_group[1].animate.set_color(PINK4), temp_group[2].animate.set_color(PINK4)], run_time=speed)
                        self.play(*[temp_group[0].animate.set_color(PINK3), temp_group[1].animate.set_color(BACKGROUND), temp_group[2].animate.set_color(BACKGROUND)], run_time=speed)
                    if edge_v_u.weight + v.key < u.key:
                        self.play(code_block.highlight(11), run_time=speed) if animate_code_block else None
                        self.wait()
                        u.key = edge_v_u.weight + v.key
                        self.play(u.update_key(u.key), run_time=speed)
                        min_edge[u] = edge_v_u
                        self.play(code_block.highlight(12), run_time=speed) if animate_code_block else None
                    self.play(u.dehighlight(), edge_v_u.mobject["line"].animate.set_color(GRAY))

            # Shortened version - playing all for loops at the same time
            else:
                self.play(code_block.highlight(8, 5), run_time=speed) if animate_code_block else None
                # Accumulate animations for all qualified mobjects and show them at once
                mobject_to_flash = []
                v_mobject_to_flash = []
                animations_update_key = []
                for u in v.neighbors:
                    if u in unreach:
                        edge_v_u = v.neighbor2edge[u]
                        new_key = edge_v_u.weight + v.key
                        if new_key < u.key:
                            mobject_to_flash += [edge_v_u.mobject["text"]["text"], edge_v_u.mobject["line"], u.key_mobject]
                            v_mobject_to_flash.append(v.key_mobject)
                            animations_update_key.append(u.update_key(new_key))
                            u.key = new_key
                            min_edge[u] = edge_v_u
                if mobject_to_flash:
                    self.play(*[m.animate.set_color(BACKGROUND) for m in mobject_to_flash], *[m.animate.set_color(PINK4) for m in v_mobject_to_flash], run_time=speed)
                    self.play(*[m.animate.set_color(GRAY) for m in mobject_to_flash], *[m.animate.set_color(BACKGROUND) for m in v_mobject_to_flash], run_time=speed)
                if animations_update_key:
                    self.play(*animations_update_key, run_time=1.5*speed)
            self.play(v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True))

        self.play(code_block.highlight(13), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, edges, speed=speed)
        return edges


    # the new version
    def shortest_paths_dijkstra(self, graph, source=None, create_legend=True, show_horizontal_legend=False, animate_code_block=True, code_block=None, speed=1, hide_details=False):
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
            l.mobjects.next_to(graph.graph_mobject, UP, buff=0.3)
            # l.mobjects.move_to(1.8*UP+1.5*RIGHT)
            self.play(l.animation)
            self.wait()
        if animate_code_block and not code_block:
            code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
            self.play(Create(code_block.code))
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        self.play(code_block.highlight(1), run_time=speed) if animate_code_block else None
        self.wait() if animate_code_block else None
        self.play(code_block.highlight(2), run_time=speed) if animate_code_block else None
        self.wait() if animate_code_block else None
        self.play(code_block.highlight(3), run_time=speed) if animate_code_block else None
        self.wait() if animate_code_block else None
        self.play(code_block.highlight(4), run_time=speed) if animate_code_block else None
        self.wait()
        # Accumulate animations for all nodes and show them at once
        transforms = []
        for node in graph.value2node.values():
            node.initialize_key(float('inf'), show_value=False)
            transforms += node.animations
        unreach_nodes_group = GraphNodesGroup(unreach)
        self.play(*transforms, run_time=1.5*speed)
        self.play(code_block.highlight(5), run_time=speed) if animate_code_block else None
        self.wait()
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0), run_time=1.5*speed)
        prev_v = None
        while unreach:
            # Show group of unreached nodes
            self.play(code_block.highlight(6), run_time=speed) if animate_code_block else None
            self.wait() if animate_code_block else None
            self.play(code_block.highlight(7), run_time=speed) if animate_code_block else None
            # Color the min node
            v = extract_min_node(unreach)
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
                    self.play(code_block.highlight(9), run_time=speed) if animate_code_block else None
                    self.wait()
                    self.play(code_block.highlight(10), run_time=speed) if animate_code_block else None
                    self.wait(1.7)
                    if edge_v_u.weight + v.key < u.key:
                        self.play(code_block.highlight(11), run_time=1.5*speed) if animate_code_block else None
                        self.wait()
                        u.key = edge_v_u.weight + v.key
                        self.play(u.update_key(u.key), run_time=1.5*speed)
                        min_edge[u] = edge_v_u
                        self.wait(1)
                        self.play(code_block.highlight(12), run_time=speed) if animate_code_block else None
                        self.wait(1)
                self.play(prev_u.dehighlight())
                self.play(edges_to_disappear_group.appear(include_label=True), nodes_to_disappear_group.appear(), run_time=0.8*speed)

            # Shortened version - playing all for loops at the same time
            else:
                # self.play(code_block.highlight(8, 5), run_time=speed) if animate_code_block else None
                # Accumulate animations for all qualified nodes and show them at once
                nodes_to_keep = [u for u in v.neighbors]
                nodes_to_keep.append(v)
                edges_to_keep = list(v.neighbor2edge.values())
                nodes_to_disappear = [n for n in graph.get_nodes() if n not in nodes_to_keep]
                edges_to_disappear = [e for e in graph.get_edges() if e not in edges_to_keep]
                nodes_to_disappear_group = GraphNodesGroup(nodes_to_disappear)
                edges_to_disappear_group = GraphEdgesGroup(edges_to_disappear)
                self.play(edges_to_disappear_group.disappear(include_label=True), nodes_to_disappear_group.disappear(), run_time=0.8*speed)
                highlight_animations = []
                relax_animations = []
                dehighlight_animations = []
                for u in v.neighbors:
                    edge_v_u = v.neighbor2edge[u]
                    if edge_v_u.weight + v.key < u.key:
                        highlight_animations.append(u.highlight(stroke_color=GREEN, stroke_width=NODE_HIGHLIGHT_STROKE_WIDTH))
                        u.key = edge_v_u.weight + v.key
                        relax_animations.append(u.update_key(u.key))
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
                self.play(edges_to_disappear_group.appear(include_label=True), nodes_to_disappear_group.appear(), run_time=0.8*speed)
        self.play(prev_v.color(fill_color=PINK4, stroke_color=PINK3, stroke_width=WIDTH, has_key=True))
        self.play(code_block.highlight(13), run_time=speed) if animate_code_block else None
        self._remove_edges(graph, edges, speed=speed)
        return edges

    ##################################
    # Construct
    ##################################

    # Comment out for easy testing
    # def construct(self, command):
    #     self.camera.background_color = BACKGROUND
    #     w = watermark()
    #     self.add(w)
        
    #     graph = GraphObject(self.adjacency_list, self.position, self.is_directed)
    #     if command == "prim":
    #         title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
    #         self.add(title_mobject)
    #         code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
    #         self.play(Create(code_block.code))
    #         graph = GraphObject(self.adjacency_list, self.position)
    #         self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.3*RIGHT)))
    #         self.mst_prim_queue(graph, source='A', code_block=code_block, hide_details=True)
    #         self.wait(2)
    #     elif command == "kruskal":
    #         title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
    #         self.add(title_mobject)
    #         code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
    #         self.play(Create(code_block.code))
    #         graph = GraphObject(self.adjacency_list, self.position)
    #         self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.2*DOWN)))
    #         self.mst_kruskal_union_find(graph, code_block=code_block)
    #         self.wait(2)


    def construct(self):
        self.camera.background_color = BACKGROUND
        w = watermark()
        self.add(w)

        # Comment out BFS code  
        # graph = Graph(MAP_UNDIRECTED, POSITION2, is_directed=False)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.bfs2(graph, 'A')

        # Comment out DFS code
        # graph = Graph(MAP_DIRECTED, POSITION2, is_directed=True)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.dfs(graph, True)
        
        # Prim-basic
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # l = Legend({PINK1: "MST so far"})
        # l.mobjects.move_to(2.7*UP + 5*RIGHT)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.graph_mobject.shift(0.3*DOWN)))
        # self.play(l.animation)
        # self.mst_prim_basic(graph, create_legend=False, animate_code_block=False, code_block=None, speed=2)
        # self.wait(10)

        # Prim-basic create thumbnail
        # l = Legend({PINK1: "MST so far"})
        # l.mobjects.move_to(1.6*UP+1.7*RIGHT)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # graph.graph_mobject.scale(0.9).shift(3.7*RIGHT)
        # self.add(l.mobjects, code_block.code, graph.graph_mobject)

        # Prim-queue
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.3*RIGHT)))
        # self.mst_prim_queue(graph, source='A', code_block=code_block, hide_details=True)
        # self.wait(10)

        # Prim-queue-no-code
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.graph_mobject.shift(0.3*DOWN)
        # l = Legend({(PINK4, PINK4): "MST so far", (PINK4, PINK5): "vertex with min edge"}, show_horizontal_legend=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(FadeIn(graph.graph_mobject))
        # self.play(l.animation)
        # self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=2)
        # self.wait(10)

        # Prim-queue-no-code-Chinese
        # title_mobject = show_title_for_demo("PRIM 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.graph_mobject.shift(0.3*DOWN)
        # l = Legend({(PINK4, PINK4): "最小生成树", (PINK4, PINK5): "与最短边相连的点"}, show_horizontal_legend=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(FadeIn(graph.graph_mobject))
        # self.play(l.animation)
        # self.mst_prim_queue(graph, source='A', create_legend=False, animate_code_block=False, hide_details=True, speed=2)
        # self.wait(10)

        # Kruskal-basic
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({(PINK2, PINK2): "MST so far", (GREEN, GREEN): "curr min edge"})
        # l.mobjects.move_to(2*UP+1.6*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, code_block=code_block, create_legend=False)
        # self.wait(10)

        # Kruskal-basic-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({(PINK2, PINK2): "最小生成树", (GREEN, GREEN): "当前最小边"})
        # l.mobjects.move_to(2*UP+1.6*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, code_block=code_block, create_legend=False)
        # self.wait(10)

        # Kruskal-basic-no-code
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.graph_mobject.shift(0.3*DOWN)
        # l = Legend({(PINK2, PINK2): "MST so far", (GREEN, GREEN): "curr min edge"}, show_horizontal_legend=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(FadeIn(graph.graph_mobject))
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(10)

        # Kruskal-basic-no-code-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # graph.graph_mobject.shift(0.3*DOWN)
        # l = Legend({(PINK2, PINK2): "最小生成树", (GREEN, GREEN): "当前最小边"}, show_horizontal_legend=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(FadeIn(graph.graph_mobject))
        # self.play(l.animation)
        # self.mst_kruskal_basic(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(10)

        # Kruskal-union-find
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.2*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", (GREEN, GREEN): "curr min edge"})
        # l.mobjects.move_to(2.1*UP+1.9*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_union_find(graph, code_block=code_block, create_legend=False)
        # self.wait(15)

        # Kruskal-union-find-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_KRUSKAL_UNION_FIND)
        # self.play(Create(code_block.code))
        # graph = GraphObject(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.1*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "最小生成树", (GREEN, GREEN): "当前最小边"})
        # l.mobjects.move_to(2.2*UP+1.9*RIGHT)
        # self.play(l.animation)
        # self.mst_kruskal_union_find(graph, code_block=code_block, create_legend=False)
        # self.wait(15)

        # Kruskal-union-find-no-code
        # title_mobject = show_title_for_demo("KRUSKAL'S ALGO FOR MST")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.graph_mobject.shift(0.3*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "MST so far", (GREEN, GREEN): "curr min edge"}, is_horizontal=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.mst_kruskal_union_find(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(15)

        # Kruskal-union-find-no-code-Chinese
        # title_mobject = show_title_for_demo("KRUSKAL 算法  ·  最小生成树")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.graph_mobject.shift(0.3*DOWN)))
        # l = Legend({("MULTICOLORS", "CIRCLE"): "最小生成树", (GREEN, GREEN): "当前最小边"}, is_horizontal=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.mst_kruskal_union_find(graph, create_legend=False, animate_code_block=False, speed=2)
        # self.wait(15)

        # Dijkastra
        # title_mobject = show_title_for_demo("DIJKSTRA'S ALGO FOR SINGLE-SOURCE SHORTEST PATHS")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # new_position = scale_position(DIPOSITION_DIJKASTRA_CLRS, 1.8, 2)
        # graph = GraphObject(DIMAP_DIJKASTRA_CLRS, new_position, is_directed=True)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.4*DOWN)))
        # l = Legend({(PINK4, PINK4): "shortest paths", (PINK4, PINK5): "v", (BACKGROUND, GREEN): "u"}, is_horizontal=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5)
        # self.play(l.animation)
        # self.shortest_paths_dijkstra(graph, source='A', code_block=code_block, create_legend=False, hide_details=False)
        # self.wait(15)

        # Dijkastra-Chinese
        # title_mobject = show_title_for_demo("DIJKSTRA 算法  ·  单源最短路径")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        # self.play(Create(code_block.code))
        # new_position = scale_position(DIPOSITION_DIJKASTRA_CLRS, 1.8, 2)
        # graph = GraphObject(DIMAP_DIJKASTRA_CLRS, new_position, is_directed=True)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.5*RIGHT+0.4*DOWN)))
        # l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "v", (BACKGROUND, GREEN): "u"}, is_horizontal=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5)
        # self.play(l.animation)
        # self.shortest_paths_dijkstra(graph, source='A', code_block=code_block, create_legend=False, hide_details=False)
        # self.wait(15)

        # Dijkastra-no-code-Chinese
        title_mobject = show_title_for_demo("DIJKSTRA'S ALGO FOR SHORTEST PATHS")
        self.add(title_mobject)
        new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        graph = GraphObject(MAP_HARD, new_position)
        self.play(FadeIn(graph.graph_mobject.shift(0.5*DOWN)))
        l = Legend({(PINK4, PINK4): "s h o r t e s t  p a t h s", (PINK4, PINK5): "n e a r e s t  n o d e", (BACKGROUND, GREEN): "n o d e  n e e d s  r e l a x a t i o n"}, is_horizontal=True)
        l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        self.play(l.animation)
        self.wait()
        self.shortest_paths_dijkstra(graph, source='A', create_legend=False, animate_code_block=False, speed=2, hide_details=True)
        self.wait(15)

        # Dijkastra-no-code-Chinese
        # title_mobject = show_title_for_demo("DIJKSTRA 算法  ·  单源最短路径")
        # self.add(title_mobject)
        # new_position = scale_position(POSITION_HARD, 1.4, 1.8)
        # graph = GraphObject(MAP_HARD, new_position)
        # self.play(FadeIn(graph.graph_mobject.shift(0.3*DOWN)))
        # l = Legend({(PINK4, PINK4): "最短路径", (PINK4, PINK5): "当前最近的点", (BACKGROUND, GREEN): "需要放松的点"}, is_horizontal=True)
        # l.mobjects.next_to(graph.graph_mobject, UP, buff=0.5).align_to(graph.graph_mobject, RIGHT)
        # self.play(l.animation)
        # self.wait()
        # self.shortest_paths_dijkstra(graph, source='A', create_legend=False, animate_code_block=False, speed=2, hide_details=True)
        # self.wait(15)