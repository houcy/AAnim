from manimlib import *
from collections import deque

# try run manimgl tree.py BuildTree

SHORT = [1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3,]
LONG = [1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0, 1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0]

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
    # Turn a list of numbers to a tree, return the root node
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

    # Calculate the correct offset (so that the node in the bottom level doesn’t overlap)
    def get_offset(self, array):
        # Hardcode the offset for different range = (how many nodes in total, corresponding offset value)
        hardcode_standard = [(3, 0.5), (7, 1), (15, 2), (32, 3), (63, 4)]
        if len(array) > 63:
            print("The max length we support is 63. Now the lengh is:", len(array))
            return False
        for cutoff, offset in hardcode_standard:
            if len(array) <= cutoff:
                return offset

    # Convert a TreeNode to an MObject in order to show on the canvas
    def create_node_object(self, node):
        radius = 0.2 # should adjust
        font_size = 0.4 
        circle = Circle(radius=radius).set_stroke(color=WHITE)
        text = Text(str(node.value)).scale(font_size)
        # Place the text at the center of the circle
        text.add_updater(lambda m: m.move_to(circle.get_center()))
        # If the node is on the left side of the root
        if node.position_x < 0:
            return VGroup(circle, text).shift(LEFT * abs(node.position_x) + DOWN * node.position_y)
        # If the node is on the right side of the root
        else:
            return VGroup(circle, text).shift(RIGHT * abs(node.position_x) + DOWN * node.position_y)

    
    # Calculate the position of each treenode and save in the treenode object
    def populate_position(self, node, offset):
        if node.parent is None:
            if node.left:
                node.left.offset = -offset
                self.populate_position(node.left, offset)
            if node.right:
                node.right.offset = offset
                self.populate_position(node.right, offset)
        else:
            parent_x = node.parent.position_x
            parent_y = node.parent.position_y
            node.position_x = parent_x + node.offset
            node.position_y = parent_y + 1 # should adjust
            if node.left:
                node.left.offset = -abs(node.offset) / 2
                self.populate_position(node.left, offset)
            if node.right:
                node.right.offset = abs(node.offset) / 2
                self.populate_position(node.right, offset)
        # Convert node to an MObject so that it can be showed on canvas
        node.object = self.create_node_object(node)

    # Convert the tree to a list of (circle+text) MObject
    def get_all_node_objects(self, node, node_objects):
        node_objects.append(node.object)
        if node.left:
            self.get_all_node_objects(node.left, node_objects)
        if node.right:
            self.get_all_node_objects(node.right, node_objects)

    # Convert the lines to a list of line MObject
    def get_all_line_objects(self, node, line_objects):
        if node.left:
            line_objects.append(Line(node.object, node.left.object))
            self.get_all_line_objects(node.left, line_objects)
        if node.right:
            line_objects.append(Line(node.object, node.right.object))
            self.get_all_line_objects(node.right, line_objects)


    def construct(self):
        # Check the length of the list (should be <=63) and output the offset based on the length
        # offset is the half of the distance between root.left and root.right
        offset = self.get_offset(LONG)
        if not offset:
            return
        # Convert list to a tree
        root = self.deserialize(LONG)
        # Fill in the position of each node, pass the offset to draw nodes
        self.populate_position(root, offset)
        # Convert the tree to a list of (circle+text) MObject
        node_objects = []
        self.get_all_node_objects(root, node_objects)
        # Convert the lines to a list of line MObject
        line_objects = []
        self.get_all_line_objects(root, line_objects)
        # Show (circle+text) MObject and line MObject
        self.add(*node_objects, *line_objects)