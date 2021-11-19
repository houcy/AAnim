from manim import *
from manim.utils.color import Colors
from collections import deque
import math

# run for low quality $ manim -ql -p tree.py BuildHeap
# try for medium quality $ manim -qm -p tree.py BuildHeap
# try for high quality $ manim -qh -p tree.py BuildHeap

MIN = [9, 8, 7, 6, 5, 4, 3, 2, 1]
MAX = [1, 2, 3, 4, 5, 6, 7, 8, 9]
LONG = [1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0, 1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0]

# Styling configs
LINE_COLOR = WHITE
BACKGROUND_COLOR = BLACK
HIGHLIGHT_COLOR = Colors.yellow_c.value
HIGHLIGHT_TEXT = BLACK
DELETE_COLOR = RED
WIDTH = 2
FONT_SIZE = 0.6
RADIUS = 0.3


class HeapNode:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.left = 2 * self.index + 1
        self.right = 2 * self.index + 2
        self.parent = math.floor((index - 1) / 2)
        self.offset = 0
        self.position_x = 0
        self.position_y = 0
        self.mobject = None
        self.text_mobject = None
        self.line_mobject = None
    
    def _create_mobject(self):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        circle = Circle(radius=RADIUS).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND_COLOR, opacity=1.0)
        text = Tex(str(self.value), color=LINE_COLOR).scale(FONT_SIZE)
        text.add_updater(lambda m: m.move_to(circle.get_center())) # Place the text at the center of the circle
        key_mobject_list = [("circle", circle), ("text", text)]
        # If the node is on the left side of the root
        if self.position_x < 0:
            self.mobject = VDict(key_mobject_list).shift(LEFT * abs(self.position_x) + DOWN * self.position_y)
        # If the node is on the right side of the root
        else:
            self.mobject = VDict(key_mobject_list).shift(RIGHT * abs(self.position_x) + DOWN * self.position_y)

    def _create_text_mobject(self):
        return Tex(str(self.value), color=LINE_COLOR).scale(FONT_SIZE)


class HeapArray():
    def __init__(self, array):
        self.length = len(array)
        self.array = []
        for i, value in enumerate(array):
            node = HeapNode(i, value)
            self.array.append(node)
        self._populate_position_and_mobjects()
    
    def _get_offset(self):
        """
        Calculate the correct offset (so that the node in the bottom level doesn’t overlap)
        """
        # Hardcode the offset for different range = (how many nodes in total, corresponding offset value)
        hardcode_standard = [(3, 0.5), (7, 1), (15, 2), (32, 3), (63, 4)]
        if self.length > 63:
            print("The max length we support is 63. Now the lengh is:", self.length)
            return False
        for cutoff, offset in hardcode_standard:
            if self.length <= cutoff:
                return offset

    def _populate_position_and_mobjects(self):
        offset = self._get_offset()
        if not offset:
            return
        for i, node in enumerate(self.array):
            if i == 0:
                if node.left < self.length:
                    self.array[node.left].offset = -offset
                if node.right < self.length:
                    self.array[node.right].offset = offset
            else:
                parent_x = self.array[node.parent].position_x
                parent_y = self.array[node.parent].position_y
                node.position_x = parent_x + node.offset
                node.position_y = parent_y + 1
                if node.left < self.length:
                    self.array[node.left].offset = -abs(node.offset) / 2
                if node.right < self.length:
                    self.array[node.right].offset = abs(node.offset) / 2
            node._create_mobject()
        
    def tree(self):
        line_mobjects = []
        node_mobjects = []
        for node in self.array:
            node_mobjects.append(node.mobject)
            if node.left < self.length:
                line = Line(node.mobject.get_center(), self.array[node.left].mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH)
                line_mobjects.append(line)
                self.array[node.left].line_mobject = line
            if node.right < self.length:
                line = Line(node.mobject.get_center(), self.array[node.right].mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH)
                line_mobjects.append(line)
                self.array[node.right].line_mobject = line
        tree = VGroup(*line_mobjects, *node_mobjects)
        animation = [FadeIn(x) for x in line_mobjects+node_mobjects]
        return tree, animation

    def table(self):
        """
        Calculate the position of the treenode the its children and save in the treenode object
        and create the node object for each node
        """
        text_mobjects = []
        for node in self.array:
            node.text_mobject = node._create_text_mobject()
            text_mobjects.append(node.text_mobject)
        table = MobjectTable(
            [text_mobjects],
            v_buff=0.5, h_buff=0.7,
            include_outer_lines=True).set_stroke(width=WIDTH)
        return table


class BuildHeap(Scene):
    def color(self, node, is_delete):
        """
        Color a node to highlight
        """
        if is_delete:
            node.mobject["circle"].set_color(DELETE_COLOR)        
        else:
            node.mobject["circle"].set_color(HIGHLIGHT_COLOR)        
        node.mobject["text"].set_color(HIGHLIGHT_TEXT)
        node.text_mobject.set_color(HIGHLIGHT_COLOR)

    def decolor(self, node):
        """
        Deolor a node to de-highlight
        """
        node.mobject["circle"].set_color(BACKGROUND_COLOR).set_stroke(LINE_COLOR)
        node.mobject["text"].set_color(LINE_COLOR)
        node.text_mobject.set_color(LINE_COLOR)

    def swap(self, node, node_to_swap, is_delete=False):
        """
        Draw the swap animation and update the array structure
        """
        self.color(node, is_delete)
        node.value, node_to_swap.value = node_to_swap.value, node.value
        node.mobject, node_to_swap.mobject = node_to_swap.mobject, node.mobject
        node.text_mobject, node_to_swap.text_mobject = node_to_swap.text_mobject, node.text_mobject
        self.play(Swap(node.mobject, node_to_swap.mobject), Swap(node.text_mobject, node_to_swap.text_mobject))
        if not is_delete:
            self.decolor(node_to_swap)
    
    def _heapify(self, heap, node, is_min_heap):
        """
        Heapify the subtree started at curr_node
        """
        if is_min_heap:
            smallest = node
            if node.left < heap.length and smallest.value > heap.array[node.left].value:
                smallest = heap.array[node.left]
            if node.right < heap.length and smallest.value > heap.array[node.right].value:
                smallest = heap.array[node.right]
            if smallest.value != node.value: # Need swap
                self.swap(node, smallest) # Draw the swap animation
                self._heapify(heap, smallest, is_min_heap)
        else:
            largest = node
            if node.left < heap.length and largest.value < heap[node.left].value:
                largest = heap.array[node.left]
            if node.right < heap.length and largest.value < heap[node.right].value:
                largest = heap.array[node.right]
            if largest != node: # Need swap
                self.swap(node, largest) # Draw the swap animation
                self.heapify(heap, largest, is_min_heap)
    
    def build_heap(self, heap, is_min_heap=True):
        """
        Build a heap by heapify each node from bottom to up
        """
        for i in range(heap.length-1, -1, -1):
            self._heapify(heap, heap.array[i], is_min_heap)

    def delete(self, heap):
        if heap.length == 0:
            print("Heap is empty")
            return
        first = heap.array[0]
        last = heap.array[-1]
        self.swap(first, last, True)
        self.play(FadeOut(last.mobject), FadeOut(last.line_mobject))
        heap.array.pop()
        heap.length -= 1
        self._heapify(heap, first, True)

    def construct(self):
        """
        Main function called by manim
        """
        self.camera.background_color = BACKGROUND_COLOR
        # Draw an array and a tree
        heap = HeapArray(MIN)
        tree, animation = heap.tree()
        table = heap.table()
        table.next_to(tree, direction = DOWN, buff=1)  # Align the tree and the array
        vgroup = VGroup(table, tree)
        vgroup.center() # Position the vgroup of tree and array at the center
        self.play(table.create(), run_time=3)
        self.play(AnimationGroup(*animation, lag_ratio=0.5), run_time=3)

        # Build heap
        # self.wait(2)
        self.build_heap(heap, is_min_heap=True)

        # Delete
        self.wait(2)
        self.delete(heap)
        self.delete(heap)
        self.delete(heap)



