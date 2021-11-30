from manim import *
from style import *
from heap_array import HeapArray

# run for low quality $ manim -ql -p heap.py BuildHeap
# try for medium quality $ manim -qm -p heap.py BuildHeap
# try for high quality $ manim -qh -p heap.py BuildHeap

SHORT = [9, 8, 7]
MIN = [9, 8, 7, 6, 5, 4, 3, 2, 1]
MID = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
MAX = [1, 2, 3, 4, 5, 6, 7, 8, 9]
LONG = [1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0, 1, 4, 3, 2, 2, 3, 4, 0, 1, 4, 3, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 1, 2, 3, 4, 0]

# Zindex: line 0, circle 1, description text 2


class BuildHeap(Scene):
    def _color(self, node, is_delete):
        """
        Color a node to highlight
        """
        if is_delete:
            node.mobject["circle"].set_color(DELETE_COLOR)
            node.mobject["text"].set_color(HIGHLIGHT_TEXT)
            node.text_mobject.set_color(DELETE_COLOR)
        else:
            node.mobject["circle"].set_color(HIGHLIGHT_COLOR)  
            node.mobject["text"].set_color(HIGHLIGHT_TEXT)
            node.text_mobject.set_color(HIGHLIGHT_COLOR)

    def _decolor(self, node):
        """
        Deolor a node to de-highlight
        """
        node.mobject["circle"].set_color(BACKGROUND_COLOR).set_stroke(LINE_COLOR)
        node.mobject["text"].set_color(LINE_COLOR)
        node.text_mobject.set_color(LINE_COLOR)

    def swap(self, heap, node, node_to_swap, is_delete=False):
        """
        Draw the swap animation and update the array structure
        """
        self._color(node, is_delete)
        self.wait(1)
        text = None
        if is_delete:
            text = Tex('move {} to the end'.format(node.value), color=LINE_COLOR).scale(FONT_SIZE).set_z_index(2).shift(5*LEFT+1*UP)
        else:
            text = Tex('heapify({})'.format(node.value), color=LINE_COLOR).scale(FONT_SIZE).set_z_index(2).shift(5*LEFT+1*UP)
        node.value, node_to_swap.value = node_to_swap.value, node.value
        node.mobject, node_to_swap.mobject = node_to_swap.mobject, node.mobject
        node.text_mobject, node_to_swap.text_mobject = node_to_swap.text_mobject, node.text_mobject
        self.play(FadeIn(text))
        self.play(Swap(node.mobject, node_to_swap.mobject), heap.table.swap(node.text_mobject, node_to_swap.text_mobject), run_time=1.5)
        self.play(FadeOut(text))
        if not is_delete:
            self._decolor(node_to_swap)
    
    def _heapify(self, heap, node, is_min_heap):
        """
        Heapify the subtree started at curr_node
        """
        if is_min_heap:
            smallest = node
            if node.left < len(heap.array) and smallest.value > heap.array[node.left].value:
                smallest = heap.array[node.left]
            if node.right < len(heap.array) and smallest.value > heap.array[node.right].value:
                smallest = heap.array[node.right]
            if smallest.value != node.value: # Need swap
                self.swap(heap, node, smallest) # Draw the swap animation
                self._heapify(heap, smallest, is_min_heap)
        else:
            largest = node
            if node.left < len(heap.array) and largest.value < heap[node.left].value:
                largest = heap.array[node.left]
            if node.right < len(heap.array) and largest.value < heap[node.right].value:
                largest = heap.array[node.right]
            if largest != node: # Need swap
                self.swap(heap, node, largest) # Draw the swap animation
                self._heapify(heap, largest, is_min_heap)

    def _filterup(self, heap, node, is_min_heap):
        if node.parent < 0:
            return
        parent = heap.array[node.parent]
        if is_min_heap:
            if node.value < parent.value:
                self.swap(heap, node, parent)
                self._filterup(heap, parent, is_min_heap)
        else:
            if node.value > parent.value:
                self.swap(heap, node, parent)
                self._filterup(heap, parent, is_min_heap)
    
    def build_heap(self, heap, is_min_heap=True):
        """
        Build a heap by heapify each node from bottom to up
        """
        text = Tex('Building the heap', color=LINE_COLOR).scale(TITLE_SIZE).set_z_index(2).move_to(TITLE_POSITION)
        self.play(FadeIn(text))
        self.wait(1)
        for i in range(len(heap.array)-1, -1, -1):
            self._heapify(heap, heap.array[i], is_min_heap)
        self.play(FadeOut(text))

    def extract(self, heap):
        if len(heap.array) == 0:
            print("Heap is empty")
            return
        text = Tex('Deletion', color=LINE_COLOR).scale(TITLE_SIZE).set_z_index(2).move_to(TITLE_POSITION)
        self.play(FadeIn(text))
        self.wait(1)
        first = heap.array[0]
        last = heap.array[-1]
        self.swap(heap, first, last, True)
        self.play(FadeOut(last.mobject), FadeOut(last.line_mobject), heap.table.remove())
        heap.remove()
        self._heapify(heap, first, True)
        self.play(FadeOut(text))

    def insert(self, heap, value):
        if len(heap.array) == 0:
            print("Heap is empty")
            return
        text = Tex('Insertion', color=LINE_COLOR).scale(TITLE_SIZE).set_z_index(2).move_to(TITLE_POSITION)
        self.play(FadeIn(text))
        self.wait(1)
        node = heap.add(value)
        self.play(FadeIn(node.line_mobject), FadeIn(node.mobject), heap.table.add(node.text_mobject))
        self._filterup(heap, node, True)
        self.play(FadeOut(text))


    def construct(self):
        """
        Main function called by manim
        """
        self.camera.background_color = BACKGROUND_COLOR
        # Draw an array and a tree
        heap = HeapArray(MIN)        
        self.play(heap.animation, run_time=3)

        # Building the heap
        self.build_heap(heap, is_min_heap=True)

        # Deletion
        self.extract(heap)

        # Insertion
        self.insert(heap, 1)




