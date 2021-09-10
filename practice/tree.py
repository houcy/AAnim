from manimlib import *
from collections import deque


ARRAY = [0, 1, 2, 3, 4]

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.offset = 0
        self.position_x = 0
        self.position_y = 0

class BuildTree(Scene):

    def deserialize(self):
        if not ARRAY:
            return None
        root = TreeNode(ARRAY[0])
        queue = deque()
        queue.append(root)
        i = 1
        while queue and i < len(ARRAY):
            node = queue.popleft()
            if ARRAY[i] != "None":
                left = TreeNode(ARRAY[i])
                left.parent = node
                node.left = left
                queue.append(left)
            i += 1
            if ARRAY[i] != "None":
                right = TreeNode(ARRAY[i])
                right.parent = node
                node.right = right
                queue.append(right)
            i += 1
        return root

    def create_node_object(self, node):
        radius = 0.25 # should adjust
        font_size = 0.4 
        circle = Circle(radius=radius).set_stroke(color=WHITE)
        text = Text(str(node.value)).scale(font_size)
        text.add_updater(lambda m: m.move_to(circle.get_center()))
        if node.position_x < 0:
            return VGroup(circle, text).shift(LEFT * abs(node.position_x) + DOWN * node.position_y)
        else:
            return VGroup(circle, text).shift(RIGHT * abs(node.position_x) + DOWN * node.position_y)

    def traverse(self, node, nodes):
        if node.parent is None:
            node.left.offset = -2
            node.right.offset = 2
        else:
            parent_x = node.parent.position_x
            parent_y = node.parent.position_y
            node.position_x = parent_x + node.offset
            node.position_y = parent_y - 1 # should adjust
            if node.left:
                node.left.offset = - node.offset / 2
                node.right.offset = node.offset / 2
        nodes.append(self.create_node_object(node))

    def construct(self):
        root = self.deserialize()
        nodes = []
        self.traverse(root, nodes)
        self.add(*nodes)