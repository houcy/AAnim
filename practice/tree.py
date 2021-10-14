from manimlib import *
from collections import deque

# try run $ manimgl tree.py BuildTree

MIN = [9, 8, 7, 6, 5, 4, 3, 2, 1]
MAX = [1, 2, 3, 4, 5, 6, 7, 8, 9]
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

    @classmethod
    def from_array(cls, array):
        """
        Turn a list of numbers to a tree, return the root node
        """
        if not array:
            return None
        root = cls(array[0])
        queue = deque()
        queue.append(root)
        i = 1
        while queue and i < len(array):
            node = queue.popleft()
            if array[i] != None:
                left = cls(array[i])
                left.parent = node
                node.left = left
                queue.append(left)
            i += 1
            if i < len(array) and array[i] != None:
                right = cls(array[i])
                right.parent = node
                node.right = right
                queue.append(right)
            i += 1
        return root


class HeapNode(TreeNode):
    """
    Inherit from TreeNode and add more attributes about array representation
    """
    def __init__(self, value):
        self.array_position_x = 0
        self.array_position_y = 0
        self.array_object = None
        TreeNode.__init__(self, value)


class BuildTree(Scene):
    ###################################################
    # Methods that convert a list to tree and mobjects #
    ###################################################

    def get_offset(self, array):
        """
        Calculate the correct offset (so that the node in the bottom level doesn’t overlap)
        """
        # Hardcode the offset for different range = (how many nodes in total, corresponding offset value)
        hardcode_standard = [(3, 0.5), (7, 1), (15, 2), (32, 3), (63, 4)]
        if len(array) > 63:
            print("The max length we support is 63. Now the lengh is:", len(array))
            return False
        for cutoff, offset in hardcode_standard:
            if len(array) <= cutoff:
                return offset


    def create_node_object(self, node):
        """
        Convert a TreeNode to an MObject so that it shows on the canvas
        """
        radius = 0.3
        font_size = 0.5 
        circle = Circle(radius=radius).set_stroke(color=WHITE, width=1).set_fill(WHITE, opacity=1.0)
        text = Text(str(node.value), font="Open Sans", weight="THIN", color=BLACK).scale(font_size)
        text.add_updater(lambda m: m.move_to(circle.get_center())) # Place the text at the center of the circle
        # If the node is on the left side of the root
        if node.position_x < 0:
            return VGroup(circle, text).shift(LEFT * abs(node.position_x) + DOWN * node.position_y)
        # If the node is on the right side of the root
        else:
            return VGroup(circle, text).shift(RIGHT * abs(node.position_x) + DOWN * node.position_y)


    def populate_position(self, node, offset):
        """
        Calculate the position of each treenode and save in the treenode object
        """
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


    def get_all_node_objects(self, node, node_objects):
        """
        Convert tree nodes to a list of (circle+text) MObject
        """
        node_objects.append(node.object)
        if node.left:
            self.get_all_node_objects(node.left, node_objects)
        if node.right:
            self.get_all_node_objects(node.right, node_objects)


    def get_all_line_objects(self, node, line_objects):
        """
        Convert the lines to a list of line MObject
        """
        if node.left:
            line_objects.append(Line(node.object.get_center(), node.left.object.get_center()).set_stroke(color=WHITE, width=1))
            self.get_all_line_objects(node.left, line_objects)
        if node.right:
            line_objects.append(Line(node.object.get_center(), node.right.object.get_center()).set_stroke(color=WHITE, width=1))
            self.get_all_line_objects(node.right, line_objects)


    def _list_to_tree_mobjects(self, node_cls, array):
        """
        Return a root node, a list of node object(Mobject), a list of lines(Mobject).
        Not user-facing. This function is called by user-facing functions list_to_tree_mobjects() 
        or list_to_heap_mobjects().
        """
        # Check the length of the list (should be <=63) and output the offset based on the length
        # offset is the half of the distance between root.left and root.right
        offset = self.get_offset(array)
        if not offset:
            return
        # Convert list to a tree
        root = node_cls.from_array(array)
        # Fill in the position of each node, pass the offset to draw nodes
        self.populate_position(root, offset)
        # Convert the tree to a list of (circle+text) MObject
        node_objects = []
        self.get_all_node_objects(root, node_objects)
        # Convert the lines to a list of line MObject
        line_objects = []
        self.get_all_line_objects(root, line_objects)
        return (root, node_objects, line_objects)

    def list_to_tree_mobjects(self, array):
        return self._list_to_tree_mobjects(TreeNode, array)

    def list_to_heap_mobjects(self, array):
        return self._list_to_tree_mobjects(HeapNode, array)

    def draw_tree(self, node_objects, line_objects):
        """
        Show (circle+text) MObject and line MObject
        """
        self.add(*line_objects, *node_objects)

    ###################################################
    # BUILD HEAP #
    ###################################################

    def color(self, node):
        """
        Color a node to highlight
        """
        node.object.set_stroke(RED, opacity=1.0, width=2)


    def decolor(self, node):
        """
        Deolor a node to de-highlight
        """
        node.object.set_stroke(BLACK, opacity=1.0, width=1)


    def swap(self, curr_node, node_to_swap):
        """
        Draw the swap animation and update the tree structure
        """
        self.color(curr_node)
        curr_node.value, node_to_swap.value = node_to_swap.value, curr_node.value
        curr_node.object, node_to_swap.object = node_to_swap.object, curr_node.object
        self.play(Swap(curr_node.object, node_to_swap.object))
        self.decolor(node_to_swap)
    

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
            if smallest.value != curr_node.value: # Need swap
                self.swap(curr_node, smallest) # Draw the swap animation
                self.heapify(smallest, is_min_heap)
        else:
            largest = curr_node
            if curr_node.left and largest.value < curr_node.left.value:
                largest = curr_node.left
            if curr_node.right and largest.value < curr_node.right.value:
                largest = curr_node.right 
            if largest.value != curr_node.value: # Need swap
                self.swap(curr_node, largest) # Draw the swap animation
                self.heapify(largest, is_min_heap)


    def build_heap(self, root, is_min_heap=True):
        """
        Build a heap started at root
        """
        stack = [root]
        all = [root]
        # Unpack the tree to a list of nodes in level order
        while stack:
            node = stack.pop()
            if node.left:
                stack.append(node.left)
                all.append(node.left)
            if node.right:
                stack.append(node.right)
                all.append(node.right)
        # Iterate all nodes from bottom to top and heapify each node
        while all:
            curr_node = all.pop()
            if not curr_node.left and not curr_node.right:
                continue
            self.heapify(curr_node, is_min_heap)


    def construct(self):
        """
        This is the main function called by manim
        """
        # To build a heap tree
        root, node_objects, line_objects = self.list_to_heap_mobjects(MAX)
        self.draw_tree(node_objects, line_objects)

        # To build a heap by the tree 
        self.build_heap(root, is_min_heap=False)


