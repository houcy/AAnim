from manimlib import *
from collections import deque

# try run $ manimgl tree.py BuildHeap

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

    def size(self):
        """
        Get the size of the tree
        """
        size = 1
        if self.left:
            size += self.left.size()
        if self.right:
            size += self.right.size()
        return size

    def unpack(self):
        """
        Unpack the tree to a list of nodes in level order
        """
        queue = deque([self])
        all = [self]
        while queue:
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
                all.append(node.left)
            if node.right:
                queue.append(node.right)
                all.append(node.right)
        return all
        
    def _get_offset(self):
        """
        Calculate the correct offset (so that the node in the bottom level doesn’t overlap)
        """
        # Hardcode the offset for different range = (how many nodes in total, corresponding offset value)
        size = self.size()
        hardcode_standard = [(3, 0.5), (7, 1), (15, 2), (32, 3), (63, 4)]
        if size > 63:
            print("The max length we support is 63. Now the lengh is:", size)
            return False
        for cutoff, offset in hardcode_standard:
            if size <= cutoff:
                return offset

    def _create_node_object(self):
        """
        Convert a TreeNode to an MObject so that it shows on the canvas
        """
        radius = 0.3
        font_size = 0.5 
        circle = Circle(radius=radius).set_stroke(color=WHITE, width=1).set_fill(WHITE, opacity=1.0)
        text = Text(str(self.value), font="Open Sans", weight="THIN", color=BLACK).scale(font_size)
        text.add_updater(lambda m: m.move_to(circle.get_center())) # Place the text at the center of the circle
        # If the node is on the left side of the root
        if self.position_x < 0:
            return VGroup(circle, text).shift(LEFT * abs(self.position_x) + DOWN * self.position_y)
        # If the node is on the right side of the root
        else:
            return VGroup(circle, text).shift(RIGHT * abs(self.position_x) + DOWN * self.position_y)

    def _populate_position_and_objects(self, offset):
        """
        Calculate the position of the treenode the its children and save in the treenode object
        and create the node object for each node
        """
        if self.parent is None:
            if self.left:
                self.left.offset = -offset
                self.left._populate_position_and_objects(offset)
            if self.right:
                self.right.offset = offset
                self.right._populate_position_and_objects(offset)
        else:
            parent_x = self.parent.position_x
            parent_y = self.parent.position_y
            self.position_x = parent_x + self.offset
            self.position_y = parent_y + 1
            if self.left:
                self.left.offset = -abs(self.offset) / 2
                self.left._populate_position_and_objects(offset)
            if self.right:
                self.right.offset = abs(self.offset) / 2
                self.right._populate_position_and_objects(offset)
        # Convert node to an MObject so that it can be showed on canvas
        self.object = self._create_node_object()
            

    def _get_all_node_objects(self, node_objects):
        """
        Convert tree nodes to a list of (circle+text) MObject
        """
        node_objects.append(self.object)
        if self.left:
            self.left._get_all_node_objects(node_objects)
        if self.right:
            self.right._get_all_node_objects(node_objects)

    def _get_all_line_objects(self, line_objects):
        """
        Convert the lines to a list of line MObject
        """
        if self.left:
            line_objects.append(Line(self.object.get_center(), self.left.object.get_center()).set_stroke(color=WHITE, width=1))
            self.left._get_all_line_objects(line_objects)
        if self.right:
            line_objects.append(Line(self.object.get_center(), self.right.object.get_center()).set_stroke(color=WHITE, width=1))
            self.right._get_all_line_objects(line_objects)

    def tree_to_mobjects(self):
        """
        Convert an abstract tree object to its mobject representation.
        Return a list of node object(Mobject), a list of lines(Mobject). 
        """
        # Check the length of the list (should be <=63) and output the offset based on the length
        # offset is the half of the distance between root.left and root.right
        offset = self._get_offset()
        if not offset:
            return
        # Fill in the position of each node, pass the offset to draw nodes
        self._populate_position_and_objects(offset)
        # Convert the tree to a list of (circle+text) MObject
        node_objects = []
        self._get_all_node_objects(node_objects)
        # Convert the lines to a list of line MObject
        line_objects = []
        self._get_all_line_objects(line_objects)
        return node_objects, line_objects


class HeapNode(TreeNode):
    """
    Inherit from TreeNode and add more attributes about array representation
    """
    def __init__(self, value):
        super().__init__(value)
        self.array_position_x = 0
        self.array_position_y = 1
        self.array_object = None


    # def _populate_array_objects(self):
    #     """
    #     Calculate the position of the treenode the its children and save in the treenode object
    #     and create the node object for each node
    #     """
    #     all = self.unpack()
        
    
    # def draw_array(self):
    #     """
    #     Create an a copy of all node objects and save in an array
    #     """
    #     self._populate_array_objects()

class BuildHeap(Scene):
    ###################################################
    # DRAW A TREE #
    ###################################################

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
        all = root.unpack()
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
        # To build a tree (initial heap that hasn't been heapified)
        root = HeapNode.from_array(MAX)
        node_objects, line_objects = root.tree_to_mobjects()
        root.draw_array()

        # To draw the tree (initial heap that hasn't been heapified)
        self.draw_tree(node_objects, line_objects)

        # To animate build heap (apply heapify)
        self.build_heap(root, is_min_heap=False)



