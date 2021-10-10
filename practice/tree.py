from manimlib import *
from collections import deque

# try run $ manimgl tree.py BuildTree

SHORT = [9, 8, 7, 6, 5, 4, 3, 2, 1]
SHORT2 = [1, 4, 3, 2, 2, 3, 4]
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
    ###################################################
    # Methods that convert a list to tree and mobjects #
    ###################################################
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
        radius = 0.3 # should adjust
        font_size = 0.5 
        circle = Circle(radius=radius).set_stroke(color=WHITE, width=1)
        text = Text(str(node.value), font="Open Sans", weight="THIN").scale(font_size)
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
            node.position_y = parent_y + 1
            if node.left:
                node.left.offset = -abs(node.offset) / 2
                self.populate_position(node.left, offset)
            if node.right:
                node.right.offset = abs(node.offset) / 2
                self.populate_position(node.right, offset)
        # Convert node to an MObject so that it can be showed on canvas
        node.object = self.create_node_object(node)

    # Convert tree nodes to a list of (circle+text) MObject
    def get_all_node_objects(self, node, node_objects):
        node_objects.append(node.object)
        if node.left:
            self.get_all_node_objects(node.left, node_objects)
        if node.right:
            self.get_all_node_objects(node.right, node_objects)

    # Convert the lines to a list of line MObject
    def get_all_line_objects(self, node, line_objects):
        if node.left:
            line_objects.append(Line(node.object, node.left.object).set_stroke(color=WHITE, width=1))
            self.get_all_line_objects(node.left, line_objects)
        if node.right:
            line_objects.append(Line(node.object, node.right.object).set_stroke(color=WHITE, width=1))
            self.get_all_line_objects(node.right, line_objects)

    def list_to_tree_mobjects(self, array):
        """
        Return a root node, a list of node object(Mobject), a list of lines(Mobject)
        """
        # Check the length of the list (should be <=63) and output the offset based on the length
        # offset is the half of the distance between root.left and root.right
        offset = self.get_offset(array)
        if not offset:
            return
        # Convert list to a tree
        root = self.deserialize(array)
        # Fill in the position of each node, pass the offset to draw nodes
        self.populate_position(root, offset)
        # Convert the tree to a list of (circle+text) MObject
        node_objects = []
        self.get_all_node_objects(root, node_objects)
        # Convert the lines to a list of line MObject
        line_objects = []
        self.get_all_line_objects(root, line_objects)
        return (root, node_objects, line_objects)

    def draw_tree(self, node_objects, line_objects):
        """
        Show (circle+text) MObject and line MObject
        """
        self.add(*node_objects, *line_objects)

    ###################################################
    # BUILD HEAP #
    ###################################################

    def swap(self, node1, node2):
        """
        Draw the swap animation and update the tree structure
        """
        node1.value, node2.value = node2.value, node1.value
        node1.object, node2.object = node2.object, node1.object
        self.play(Swap(node1.object, node2.object))

    def heapify(self, curr_node, is_min_heap):
        """
        Heapify the subtree started at curr_node
        """
        if is_min_heap:
            smallest = curr_node
            if curr_node.left and smallest.value > curr_node.left.value:
                smallest = curr_node.left
            if curr_node.right and smallest.value > curr_node.right.value:
                smallest = curr_node.right 
            if smallest.value != curr_node.value:
                self.swap(curr_node, smallest) # Draw the swap animation
                self.heapify(smallest, is_min_heap=True)
        else:
            largest = curr_node
            if curr_node.left and largest.value < curr_node.left.value:
                largest = curr_node.left
            if curr_node.right and largest.value < curr_node.right.value:
                largest = curr_node.right 
            if largest.value != curr_node.value:
                self.swap(curr_node, largest) # Draw the swap animation
                self.heapify(largest, is_min_heap=True)

    def build_heap(self, root, is_min_heap=True):
        """
        Build a heap started at root
        """
        stack = [root]
        all = [root]
        while stack:
            node = stack.pop()
            if node.left:
                stack.append(node.left)
                all.append(node.left)
            if node.right:
                stack.append(node.right)
                all.append(node.right)
        
        while all:
            curr_node = all.pop()
            if not curr_node.left and not curr_node.right:
                continue
            self.heapify(curr_node, is_min_heap=True)


    # Main
    def construct(self):
        """
        To build a tree:
        1. Call list_to_tree_mobjects() which takes a list and returns a list of tree nodes and a list of lines
        2. Add all nodes and all lines in self.add()
        """
        root, node_objects, line_objects = self.list_to_tree_mobjects(SHORT)
        self.draw_tree(node_objects, line_objects)
        self.build_heap(root, is_min_heap=True)


