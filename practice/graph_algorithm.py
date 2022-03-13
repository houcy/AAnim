from manim import *
from style import *
from code_constant import *
from graph import Graph1
from code_block import CodeBlock
from legend import Legend
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *
import copy

MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
POSITION1 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

MAP_MST = {'A': {'B': 4, 'H': 8}, 'B': {'A': 4, 'C': 8, 'H': 11}, 'H': {'A': 8, 'B': 11, 'G': 1, 'I': 7}, 'C': {'B': 8, 'D': 7, 'I': 2, 'F': 4}, 'D': {'C': 7, 'F': 14, 'E': 9}, 'I': {'C': 2, 'G': 6, 'H': 7}, 'F': {'C': 4, 'G': 2, 'D': 14, 'E': 10}, 'G': {'I': 6, 'F': 2, 'H': 1}, 'E': {'D': 9, 'F': 10}}
POSITION_MST = {'A': (0.6042746838748182, 0.7103137006229252), 'B': (1.4402327576560112, 2.1393785668991754), 'H': (2.23008691111194, 0.4028497892498788), 'C': (2.9889216307956286, 3.1086575403782315), 'D': (4.368905964414935, 4.069901898616137), 'I': (3.082024693200045, 1.457062926629117), 'F': (4.744899101048156, 2.5254205677197956), 'G': (4.178671341713604, 0.7153493229885487), 'E': (6.0, 3.649819090603902)}

MAP_HARD = {'0': ['1', '3', '4', '5', '6', '7', '8', '9'], '1': ['2', '4', '5', '6', '7', '8', '9'], '2': ['3', '5', '6', '7', '8', '9'], '3': ['4', '6', '7', '8', '9'], '4': ['5', '7', '8', '9'], '5': ['6', '8', '9'], '6': ['7', '9'], '7': ['8'], '8': ['9']}
POSITION_HARD = {'0': (0.6620619456158209, 3.900198730066405), '1': (4.853860695070525, 3.5979836168872086), '3': (0.8818040812369734, 0.42969318016576996), '4': (1.8702195724880033, 5.0), '5': (4.774368668508555, 4.896757306965247), '6': (2.542048373806408, 3.626339004410838), '7': (0.8719887547864863, 1.7828995201395959), '8': (4.364790848722795, 2.102951868547332), '9': (2.812757500848238, 1.0603218457660801), '2': (4.762735689011682, 0.4245068101400804)}


class Show(Scene):
    # def __init__(self, adjacency_list, position, is_directed):
    #     self.adjacency_list = adjacency_list
    #     self.position = position
    #     self.is_directed = is_directed
    #     super().__init__()

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
    
    def bfs2(self, graph, s):
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

    def mst_prim_basic(self, graph, speed=1, code_block=None):
        l = Legend({PINK1: "MST so far"})
        l.mobjects.move_to(1.6*UP+1.7*RIGHT)
        self.play(l.animation)
        self.wait()
        # l.mobjects.next_to(graph.graph_mobject, DOWN, buff=0.3)
        if not code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
            self.play(Create(code_block.code))
        self.play(code_block.highlight(1))
        selected_edges = set()
        selected = set()
        first_node_key = list(graph.adjacency_list.keys())[0]
        first_node = graph.value2node[first_node_key]
        self.play(code_block.highlight(2, 3), run_time=speed)
        self.play(code_block.highlight(5), run_time=speed)
        selected.add(first_node)
        self.play(first_node.color(), run_time=speed)
        while len(selected) != len(graph.adjacency_list):
            self.play(code_block.highlight(6), run_time=speed)
            self.wait(0.8)
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
            self.play(code_block.highlight(7, 2), run_time=speed)
            self.play(neighbor_edges.highlight(BACKGROUND), run_time=1.3*speed)
            self.wait(speed)
            self.play(neighbor_edges.dehighlight(), run_time=1.3*speed)
            self.play(minimum_edge.highlight(PINK1), run_time=0.5*speed)
            self.play(minimum_edge.dehighlight(), run_time=0.5*speed)
            self.play(minimum_edge.highlight(PINK1), run_time=0.5*speed)
            self.wait()
            # show the shortest edge - the next edge to add
            self.play(code_block.highlight(9, 3), run_time=speed)
            selected.add(minimum_node)
            self.play(minimum_node.color(), run_time=speed)
        self.play(code_block.highlight(12), run_time=speed)
        edge_to_remove = set()
        for edge in graph.edges:
            if edge not in selected_edges:
                edge_to_remove.add(edge)
                self.play(edge.fade_out(), run_time=0.4*speed)
        self.play(code_block.highlight(13), run_time=speed)
        

    def mst_prim_queue(self, graph, source=None, speed=1, code_block=None):
        def extract_min_node(list, unreach_nodes_group):
            min_so_far = float('inf')
            min_node = None
            for n in list:
                if n.key < min_so_far:
                    min_so_far = n.key
                    min_node = n
            list.remove(min_node)
            return min_node

        l = Legend({PINK1: "MST so far", ("HIGHLIGHT_ROUNDED_RECTANGLE", PINK1, HIGHLIGHT_STROKE): "v"})
        l.mobjects.next_to(graph.graph_mobject, DOWN, buff=0.3)
        l.mobjects.move_to(1.8*UP+1.5*RIGHT)
        self.play(l.animation)
        self.wait()
        if not code_block:
            code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
            self.play(Create(code_block.code))
        # self.play(code_block.highlight(1), run_time=speed)
        # self.play(code_block.highlight(2, 3), run_time=speed)
        edges = []
        unreach = list(graph.value2node.values())
        min_edge = {}
        # self.play(code_block.highlight(5), run_time=speed)
        transforms = []
        fadeins = []
        for node in graph.value2node.values():
            node.initialize_key(float('inf'), show_value=False)
            transform, fadein = node.animations
            transforms.append(transform)
            fadeins.append(fadein)
        unreach_nodes_group = GraphNodesGroup(unreach)
        self.play(*transforms)
        # self.wait()
        self.play(*fadeins)
        # self.play(code_block.highlight(6), run_time=speed)
        if not source:
            source_node = graph.value2node.values()[0]
        else:
            source_node = graph.value2node[source]
        self.play(source_node.update_key(0))
        while unreach:
            self.play(unreach_nodes_group.color(PINK1, width=1), run_time=0.5*speed)
            self.play(unreach_nodes_group.color(GRAY, width=0), run_time=0.5*speed)
            self.play(unreach_nodes_group.color(PINK1, width=1), run_time=0.5*speed)
            self.wait()
            self.play(unreach_nodes_group.color(GRAY, width=0), run_time=0.5*speed)
            v = extract_min_node(unreach, unreach_nodes_group)
            self.play(v.color(has_key=True))
            # self.play(v.highlight_stroke())
            self.play(v.highlight_stroke_and_change_shape())
            # Get the min edge
            if v in min_edge:
                edges.append(min_edge[v])
                # self.play(min_edge[v].highlight(PINK1), run_time=0.5*speed)
                # self.play(min_edge[v].dehighlight(), run_time=0.5*speed)
                self.play(min_edge[v].highlight(PINK1), run_time=0.5*speed)
                # self.wait()
            # Decrease key and save the min edge
            for u in v.neighbors:
                if u in unreach:
                    edge_v_u = v.neighbor2edge[u]
                    if edge_v_u.weight < u.key:
                        self.play(u.update_key(edge_v_u.weight))
                        u.key = edge_v_u.weight
                        min_edge[u] = edge_v_u
            # self.play(v.highlight_stroke(PINK2))
            self.play(v.dehighlight_stroke_and_change_shape())
        return edges


    def construct(self):
        self.camera.background_color = BACKGROUND
        w = watermark()
        self.add(w)
        # Comment out for easy testing
        # graph = Graph(self.adjacency_list, self.position, self.is_directed)

        # Comment out DFS code
        # graph = Graph(MAP_DIRECTED, POSITION2, is_directed=True)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.dfs(graph, True)
        
        # Prim-basic
        # title_mobject = show_title_for_demo("PRIM'S ALGO FOR MST")
        # self.add(title_mobject)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # self.play(Create(code_block.code))
        # graph = Graph1(MAP_MST, POSITION_MST)
        # self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.7*RIGHT)))
        # self.mst_prim_basic(graph, code_block=code_block)
        # self.wait(5)

        # Prim-basic create thumbnail
        # l = Legend({PINK1: "MST so far"})
        # l.mobjects.move_to(1.6*UP+1.7*RIGHT)
        # code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        # graph = Graph1(MAP_MST, POSITION_MST)
        # graph.graph_mobject.scale(0.9).shift(3.7*RIGHT)
        # self.add(l.mobjects, code_block.code, graph.graph_mobject)

        # Prim-queue
        # title_mobject = show_title_for_demo("PRIM'S ALGO (USING QUEUE) FOR MST")
        # self.add(title_mobject)
        code_block = CodeBlock(CODE_FOR_PRIM_QUEUE)
        self.play(Create(code_block.code.shift(0.2*RIGHT)))
        graph = Graph1(MAP_MST, POSITION_MST)
        self.play(FadeIn(graph.graph_mobject.scale(0.9).shift(3.3*RIGHT)))
        self.mst_prim_queue(graph, source='A', code_block=code_block)
        # self.wait(5)

        # Comment out BFS code  
        # graph = Graph(MAP_UNDIRECTED, POSITION2, is_directed=False)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.bfs2(graph, 'A')

        
    
        