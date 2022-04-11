from manim import *
from style import *
from graph_edges_group import GraphEdgesGroup

class UnionFind:
    def __init__(self, array):
        self.array = array
        self.color = {}
        self.animation = None
        self.donimant_color = None
        self.root2edges = {}
        for a in array:
            a.parent = a
            self.root2edges[a] = []
        # if len(LIGHT_COLORS) >= len(array):
        color_index = 0
        animations = []
        for node in array:
            if color_index == len(LIGHT_COLORS):
                color_index = 0
            node_color = LIGHT_COLORS[color_index]
            animations.append(node.color(fill_color=node_color))
            self.color[node] = node_color
            color_index += 1
        self.animation = AnimationGroup(*animations, lag_ratio=0.2)
    
    def show_set(self):
        """
        Usually called after initialize an instance (each node is a set)
        """
        return self.animation

    def find(self, element):
        if element.parent == element:
            return element
        else:
            return self.find(element.parent)

    def all_descendants(self, node):
        if not node.children:
            return [node]
        else:
            descendants = [node]
            for child in node.children:
                descendants += self.all_descendants(child)
            return descendants
    
    def union(self, element_b, element_a, edge=None):
        root_of_a = self.find(element_a)
        root_of_b = self.find(element_b)
        a_and_descendants = self.all_descendants(root_of_a)
        b_and_descendants = self.all_descendants(root_of_b)
        # assign the larger tree to b such that the smaller root will be the child of the larger root
        if len(a_and_descendants) > len(b_and_descendants):
            root_of_a, root_of_b = root_of_b, root_of_a
            a_and_descendants, b_and_descendants = b_and_descendants, a_and_descendants
        root_of_a.parent = root_of_b
        root_of_b.children.append(root_of_a)
        # change the color of a and all descendants to the color of group b
        root_of_b_color = self.color[root_of_b]
        animations = []
        for descendant in a_and_descendants:
            animations.append(descendant.color(fill_color=root_of_b_color))
            new_text_mobject = root_of_b.text_mobject.copy().move_to(descendant.text_mobject.get_center())
            animations.append(ReplacementTransform(descendant.text_mobject, new_text_mobject))
            descendant.text_mobject = new_text_mobject
        self.donimant_color = root_of_b_color
        # update b.edges
        self.root2edges[root_of_b] = [edge] + self.root2edges[root_of_b] + self.root2edges[root_of_a]
        if not edge:
            return AnimationGroup(*animations)
        else:
            edge_group = GraphEdgesGroup(self.root2edges[root_of_b])
            animations.append(edge_group.highlight(color=root_of_b_color))
            return AnimationGroup(*animations)

    def destroy(self):
        for n in self.array:
            n.parent = None
            n.children = []

        
        

