from manim import *
from style import *
from heap_array import HeapArray

# create low quality video $ manim -ql -p heap.py BinaryHeap
# create medium quality video $ manim -qm -p heap.py BinaryHeap
# create high quality video $ manim -qh -p heap.py BinaryHeap

# Zindex: line 0, circle 1, description text 2


class BinaryHeap(Scene):
    def __init__(self, array):
        self.heap = HeapArray(array) 
        super().__init__()

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
        node.mobject["circle"].set_color(BACKGROUND).set_stroke(LINE_COLOR)
        node.mobject["text"].set_color(LINE_COLOR)
        node.text_mobject.set_color(LINE_COLOR)

    def _decolor_all(self, heap_array):
        """
        Deolor all nodes to de-highlight
        """
        for node in heap_array:
            node.mobject["circle"].set_color(BACKGROUND).set_stroke(LINE_COLOR)
            node.mobject["text"].set_color(LINE_COLOR)
            node.text_mobject.set_color(LINE_COLOR)

    def swap(self, heap, node, node_to_swap, is_delete=False):
        """
        Draw the swap animation and update the array structure
        """
        node.value, node_to_swap.value = node_to_swap.value, node.value
        node.mobject, node_to_swap.mobject = node_to_swap.mobject, node.mobject
        self.play(Swap(node.mobject, node_to_swap.mobject), heap.table.swap(node.text_mobject, node_to_swap.text_mobject), run_time=1.5)
        node.text_mobject, node_to_swap.text_mobject = node_to_swap.text_mobject, node.text_mobject
        # if not is_delete:
        #     self._decolor(node_to_swap)
    
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
        self.play(FadeIn(heap.code_for_build.code, heap.code_for_build.create_title('Building the heap')))
        self.wait(1)
        for i in range((len(heap.array)-1) // 2, -1, -1):
            node = heap.array[i]
            # Color
            self.play(heap.code_for_build.highlight(2))
            self.wait(0.5)
            self._color(node, False)
            self.wait(0.5)
            # Heapify
            self.play(heap.code_for_build.highlight(3))
            self._heapify(heap, node, is_min_heap)
            self._decolor_all(heap.array)
        self.play(FadeOut(heap.code_for_build.code, heap.code_for_build.highlight_rect, heap.code_for_build.title))


    def extract(self, heap):
        if len(heap.array) == 0:
            print("Heap is empty")
            return
        self.play(FadeIn(heap.code_for_extract.code, heap.code_for_build.create_title('Deletion')))
        self.wait(0.5)
        # Swap
        self.play(heap.code_for_extract.highlight(3))
        first = heap.array[0]
        last = heap.array[-1]
        self._color(first, False)
        self._color(last, False)
        self.swap(heap, first, last, True)
        # Remove last
        self.play(heap.code_for_extract.highlight(4))
        self.wait(1)
        self.play(FadeOut(last.mobject), FadeOut(last.line_mobject), heap.table.remove())
        heap.remove()
        # Heapify
        self.play(heap.code_for_extract.highlight(5))
        self.wait(1)
        self._heapify(heap, first, True)
        self._decolor_all(heap.array)
        # Clean up
        self.play(FadeOut(heap.code_for_extract.code, heap.code_for_extract.highlight_rect, heap.code_for_build.title))


    def insert(self, heap, value):
        if len(heap.array) == 0:
            print("Heap is empty")
            return
        self.play(FadeIn(heap.code_for_insert.code, heap.code_for_build.create_title('Insertion')))
        self.wait(0.5)
        # Insert
        self.play(heap.code_for_insert.highlight(3))
        node = heap.add(value)
        self.play(FadeIn(node.line_mobject), FadeIn(node.mobject), heap.table.add(node.text_mobject))
        # Heapify
        self._color(node, False)
        self.play(heap.code_for_insert.highlight(4))
        self.wait(1)
        self._filterup(heap, node, True)
        self._decolor_all(heap.array)
        # Clean up
        self.play(FadeOut(heap.code_for_insert.code, heap.code_for_insert.highlight_rect, heap.code_for_build.title))


    def construct(self, command):
        """
        Main function called by manim
        command is a list of string
        """
        # print("command", command)
        self.camera.background_color = BACKGROUND
        
        # Draw an array and a tree 
        if command[0].isdigit():   
            print("self.heap.animation", self.heap.animation)  
            self.play(self.heap.animation, run_time=3)
        # Building the heap
        elif command[0] == 'build':
            if command[1] == 'min':
                self.build_heap(self.heap, is_min_heap=True)
            elif command[1] == 'max':
                self.build_heap(self.heap, is_min_heap=False)
            else:
                print('Error: input should be min or max')
        # Deletion
        elif command[0] == 'extract':
            self.extract(self.heap)
        # Insertion
        elif command[0] == 'insert':
            self.insert(self.heap, int(command[1]))






