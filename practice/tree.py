from manimlib import *
from collections import deque

# try run manimgl tree.py BuildTree

ARRAY = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, None, 4]

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.offset = 0
        self.position_x = 0
        self.position_y = 0
        self.object = None

class BuildTree(Scene):
    def deserialize(self, array):
        if not array:
            return None
        root = TreeNode(array[0])
        queue = deque()
        queue.append(root)
        i = 1
        while queue and i < len(array):
            node = queue.popleft()
            if array[i] != None:
                left = TreeNode(array[i])
                left.parent = node
                node.left = left
                queue.append(left)
            i += 1
            if i < len(array) and array[i] != None:
                right = TreeNode(array[i])
                right.parent = node
                node.right = right
                queue.append(right)
            i += 1
        return root

    def create_node_object(self, node):
        radius = 0.2 # should adjust
        font_size = 0.4 
        circle = Circle(radius=radius).set_stroke(color=WHITE)
        text = Text(str(node.value)).scale(font_size)
        text.add_updater(lambda m: m.move_to(circle.get_center()))
        if node.position_x < 0:
            return VGroup(circle, text).shift(LEFT * abs(node.position_x) + DOWN * node.position_y)
        else:
            return VGroup(circle, text).shift(RIGHT * abs(node.position_x) + DOWN * node.position_y)

    def populate_position(self, node):
        if node.parent is None:
            if node.left:
                node.left.offset = -2
                self.populate_position(node.left)
            if node.right:
                node.right.offset = 2
                self.populate_position(node.right)
        else:
            parent_x = node.parent.position_x
            parent_y = node.parent.position_y
            node.position_x = parent_x + node.offset
            node.position_y = parent_y + 1 # should adjust
            if node.left:
                node.left.offset = -abs(node.offset) / 2
                self.populate_position(node.left)
            if node.right:
                node.right.offset = abs(node.offset) / 2
                self.populate_position(node.right)
        node.object = self.create_node_object(node)


    def get_all_node_objects(self, node, node_objects):
        node_objects.append(node.object)
        if node.left:
            self.get_all_node_objects(node.left, node_objects)
        if node.right:
            self.get_all_node_objects(node.right, node_objects)


    def get_all_line_objects(self, node, line_objects):
        if node.left:
            line_objects.append(Line(node.object, node.left.object))
            self.get_all_line_objects(node.left, line_objects)
        if node.right:
            line_objects.append(Line(node.object, node.right.object))
            self.get_all_line_objects(node.right, line_objects)


    def construct(self):
        root = self.deserialize(ARRAY)
        self.populate_position(root)
        node_objects = []
        self.get_all_node_objects(root, node_objects)
        line_objects = []
        self.get_all_line_objects(root, line_objects)
        self.add(*node_objects, *line_objects)