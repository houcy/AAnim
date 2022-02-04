from manim import *
from manim.utils.color import Colors
from collections import deque

# run for low quality $ manim -ql -p tree.py BuildHeap
# try for medium quality $ manim -qm -p tree.py BuildHeap
# try for high quality $ manim -qh -p tree.py BuildHeap

MIN = [9, 8, 7, 6, 5, 4, 3, 2, 1]
MAX = [1, 2, 3, 4, 5, 6, 7, 8, 9]
LONG = [1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0, 1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0]

# Styling configs
LINE_COLOR = WHITE
BACKGROUND = BLACK
HIGHLIGHT_COLOR = Colors.yellow_c.value
HIGHLIGHT_TEXT = BLACK
WIDTH = 2
FONT_SIZE = 0.6
RADIUS = 0.3


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
        Unpack the tree to a list of nodes in bfs
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
        circle = Circle(radius=RADIUS).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND, opacity=1.0)
        text = Tex(str(self.value), color=LINE_COLOR).scale(FONT_SIZE)
        text.add_updater(lambda m: m.move_to(circle.get_center())) # Place the text at the center of the circle
        key_mobject_list = [("circle", circle), ("text", text)]
        # If the node is on the left side of the root
        if self.position_x < 0:
            return VDict(key_mobject_list).shift(LEFT * abs(self.position_x) + DOWN * self.position_y)
        # If the node is on the right side of the root
        else:
            return VDict(key_mobject_list).shift(RIGHT * abs(self.position_x) + DOWN * self.position_y)


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
            
    def _get_all_node_objects(self):
        """
        Convert tree nodes to a list of (circle+text) mobject.
        Reutrn the mobject.
        """
        nodes = self.unpack()
        return [node.object for node in nodes]

    def _get_all_line_objects(self):
        """
        Convert the lines to a list of line mobject.
        Reutrn the mobject.
        """
        line_objects = []
        if self.left:
            line_objects.append(Line(self.object.get_center(), self.left.object.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH))
            line_objects += self.left._get_all_line_objects()
        if self.right:
            line_objects.append(Line(self.object.get_center(), self.right.object.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH))
            line_objects += self.right._get_all_line_objects()
        return line_objects

    def create_node_mobjects(self):
        """
        Convert an abstract tree object to its mobject representation.
        Return a list of node object(Mobject), a list of lines(mobject). 
        """
        # Check the length of the list (should be <=63) and output the offset based on the length
        # offset is the half of the distance between root.left and root.right
        offset = self._get_offset()
        if not offset:
            return
        # Fill in the position of each node, pass the offset to draw nodes
        self._populate_position_and_objects(offset)
        # Convert the node tree to a list of (circle+text) MObject
        node_mobjects = self._get_all_node_objects()
        # Convert the lines to a list of line MObject
        line_mobjects = self._get_all_line_objects()
        return [*line_mobjects, *node_mobjects]


class HeapNode(TreeNode):
    """
    Inherit from TreeNode and add more attributes about array representation
    """
    def __init__(self, value):
        super().__init__(value)
        self.text_mobject = None
    
    def _create_text_mobject(self):
        return Tex(str(self.value), color=LINE_COLOR).scale(FONT_SIZE)

    def create_text_mobjects(self):
        """
        Calculate the position of the treenode the its children and save in the treenode object
        and create the node object for each node
        """
        all = self.unpack()
        text_mobjects = []
        for node in all:
            node.text_mobject = node._create_text_mobject()
            text_mobjects.append(node.text_mobject)
        return text_mobjects
            

class BuildHeap(Scene):
    def create_table_mobject(self, root):
        array_node_mobjects = root.create_text_mobjects()
        table = MobjectTable(
            [array_node_mobjects],
            v_buff=0.5, h_buff=0.7,
            include_outer_lines=True).set_stroke(width=WIDTH)
        return table
    
    def color(self, node):
        """
        Color a node to highlight
        """
        # self.play(node.object["circle"].animate.set_color(HIGHLIGHT_COLOR), node.object["text"].animate.set_color(HIGHLIGHT_TEXT))
        node.object["circle"].set_color(HIGHLIGHT_COLOR)        
        node.object["text"].set_color(HIGHLIGHT_TEXT)
        node.text_mobject.set_color(HIGHLIGHT_COLOR)

    def decolor(self, node):
        """
        Deolor a node to de-highlight
        """
        node.object["circle"].set_color(BACKGROUND).set_stroke(LINE_COLOR)
        node.object["text"].set_color(LINE_COLOR)
        node.text_mobject.set_color(LINE_COLOR)

    def swap(self, curr_node, node_to_swap):
        """
        Draw the swap animation and update the tree structure
        """
        self.color(curr_node)
        curr_node.value, node_to_swap.value = node_to_swap.value, curr_node.value
        curr_node.object, node_to_swap.object = node_to_swap.object, curr_node.object
        curr_node.text_mobject, node_to_swap.text_mobject = node_to_swap.text_mobject, curr_node.text_mobject
        self.play(Swap(curr_node.object, node_to_swap.object), Swap(curr_node.text_mobject, node_to_swap.text_mobject))
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
        Main function called by manim
        """
        self.camera.background_color = BACKGROUND
        # Create a tree data structure
        root = HeapNode.from_array(MIN)

        # Create the array mobject
        table_mobject = self.create_table_mobject(root)

        # Create the tree mobject
        tree_mobject_list = root.create_node_mobjects()

        # Draw array and tree
        tree_vgroup = VGroup(*tree_mobject_list)
        table_mobject.next_to(tree_vgroup, direction = DOWN, buff=1)  # Align the tree and the array
        vgroup = VGroup(table_mobject, tree_vgroup)
        vgroup.center() # Position the vgroup of tree and array at the center
        animation = [FadeIn(x) for x in tree_mobject_list]
        self.play(table_mobject.create(), run_time=3)
        self.play(AnimationGroup(*animation, lag_ratio=0.5), run_time=3)

        # To animate build heap (apply heapify)
        self.wait(2)
        self.build_heap(root, is_min_heap=True)




