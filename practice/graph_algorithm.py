from manim import *
from style import *
from code_constant import *
from graph import Graph
from code_block import CodeBlock
from legend import Legend
import copy


MAP= {'A': ['B'], 'B': ['D'], 'D': ['C'], 'C': ['A']}

POSITION1 = {'A': (0.675, 2.1569), 'B': (2.4143499999999998, 0.45), 'D': (4.135, 2.181125), 'C': (2.38995, 3.8865000000000003)}
MAP_DIRECTED = {'A': ['B', 'C'], 'B': ['D', 'E'], 'D': ['F'], 'E': ['F']}
MAP_UNDIRECTED = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A'], 'D': ['B', 'F'], 'E': ['B'], 'F': ['D']}
POSITION2 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

POSITION3 = {'A': (0.6042746838748182, 0.7103137006229252), 'B': (1.4402327576560112, 2.1393785668991754), 'H': (2.23008691111194, 0.4028497892498788), 'C': (2.9889216307956286, 3.1086575403782315), 'D': (4.368905964414935, 4.069901898616137), 'I': (3.082024693200045, 1.457062926629117), 'F': (4.744899101048156, 2.5254205677197956), 'G': (4.178671341713604, 0.7153493229885487), 'E': (6.0, 3.649819090603902)}
MAP3 = {'A': ['B', 'H'], 'B': ['A', 'C', 'H'], 'H': ['A', 'B', 'G', 'I'], 'C': ['B', 'D', 'I', 'F'], 'D': ['C', 'F', 'E'], 'I': ['C', 'G', 'H'], 'F': ['C', 'G', 'D', 'E'], 'G': ['I', 'F', 'H'], 'E': ['D', 'F']}
EDGE_VALUE = {'A': {'B': 4, 'H': 8}, 'B': {'A': 4, 'H': 11, 'C': 8}, 'C': {'B': 8, 'I': 2, 'F': 4, 'D': 7}, 'D': {'C': 7, 'F': 14, 'E': 9}, 'E': {'D': 9, 'F': 10}, 'F': {'C': 4, 'D': 14, 'E': 10, 'G': 2}, 'G': {'F': 2, 'H': 1}, 'H': {'A': 8, 'B': 11, 'G': 1, 'I': 7}, 'I': {'C': 2, 'G': 6, 'H': 7}}

MAP_HARD = {'0': ['1', '3', '4', '5', '6', '7', '8', '9'], '1': ['2', '4', '5', '6', '7', '8', '9'], '2': ['3', '5', '6', '7', '8', '9'], '3': ['4', '6', '7', '8', '9'], '4': ['5', '7', '8', '9'], '5': ['6', '8', '9'], '6': ['7', '9'], '7': ['8'], '8': ['9']}
POSITION_HARD = {'0': (0.6620619456158209, 3.900198730066405), '1': (4.853860695070525, 3.5979836168872086), '3': (0.8818040812369734, 0.42969318016576996), '4': (1.8702195724880033, 5.0), '5': (4.774368668508555, 4.896757306965247), '6': (2.542048373806408, 3.626339004410838), '7': (0.8719887547864863, 1.7828995201395959), '8': (4.364790848722795, 2.102951868547332), '9': (2.812757500848238, 1.0603218457660801), '2': (4.762735689011682, 0.4245068101400804)}


class GraphAlgorithm(Scene):
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
        for neighbor in node.neighbor2line:
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
        print("node.value", node.value)
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
        print("post_order", post_order)
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
                print(start_node.value)
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
    #         for neighbor in curr.neighbor2line:
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
                for neighbor in curr.neighbor2line:
                    self.play(code_block.highlight(8))
                    if neighbor not in discovered:
                        self.play(code_block.highlight(9))
                        next_level.append(neighbor)
                        self.play(code_block.highlight(10))
                        discovered.add(curr)
                        self.play(code_block.highlight(11))
                        self.play(neighbor.mark_pink3())
                self.play(curr.mobject.highlight_stroke(PINK1))
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

    CODE_FOR_PRIM = """MST-PRIM(G, w, s) {
        for each vertex v
            v.key = ∞
        s.key = 0
        Q = G.V
        T = Φ
        while Q != Φ
            v = EXTRACT-MIN(Q)
            add edge(v) to T
            for each neighbor u of v
                if u ∈ Q and w(u, v) < u.key
                    edge(u) = uv
                    u.key = w(u, v)
    }
    """

    CODE_FOR_PRIM_BASIC = """MST-PRIM(G) {
        T = ∅;
        add an arbitraty v vertex to U;
        while (U ≠ V)
            for each vertex v in U
                find (u, v) be the min edge
                such that u ∈ V - U
                T = T ∪ {(u, v)}
                U = U ∪ {v}
    }
    """

    def mst_prim_basic(self, graph):
        code_block = CodeBlock(CODE_FOR_PRIM_BASIC)
        self.add(code_block.code)
        selected_edges = set()
        selected = set()
        first_node_key = list(graph.adjacency_list.keys())[0]
        first_node = graph.value2node[first_node_key]
        selected.add(first_node)
        while len(selected) != len(graph.adjacency_list):
            minimum = float("inf")
            minimum_node = None
            for v in selected:
                for u in v.neighbor2line:
                    if u not in selected and graph.adjacency_list[u.value][v.value] < minimum:
                        print("u v", v.value, u.value, graph.adjacency_list[u.value][v.value], minimum)
                        minimum = graph.adjacency_list[u.value][v.value]
                        minimum_node = u
            print(minimum_node.value)
            for e in v.neighbor2line:
                print("- inside v.neighbor2line", v.value, e.value)
            selected_edges.add(v.neighbor2line[minimum_node])
            selected.add(minimum_node)



    def construct(self):
        self.camera.background_color = BACKGROUND
        # Comment out DFS code
        graph = Graph(MAP_DIRECTED, POSITION2, is_directed=True)
        self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        self.dfs(graph, True)

        # Comment out for easy testing
        # graph = Graph(self.adjacency_list, self.position, self.is_directed)
        
        # Prim
        # graph = Graph(MAP3, POSITION3, EDGE_VALUE)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.mst_prim_basic(graph)


        # Comment out BFS code  
        # graph = Graph(MAP_DIRECTED, POSITION2, True)
        # self.add(graph.graph_mobject.shift(3.2 * RIGHT))
        # self.bfs2(graph, 'A')

        
    
        