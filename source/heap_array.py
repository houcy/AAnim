from manim import *
from style import *
from heap_node import HeapNode
from table import Table
from code_block import CodeBlock
from code_constant import *


class HeapArray():
    def __init__(self, array):
        self.array = []
        for i, value in enumerate(array):
            node = HeapNode(i, value)
            self.array.append(node)
        self.table = self._table()
        self._populate_position_and_mobjects()  
        self.code_for_build = CodeBlock(CODE_FOR_BUILD)
        self.code_for_extract = CodeBlock(CODE_FOR_EXTRACT)
        self.code_for_insert = CodeBlock(CODE_FOR_INSERT)
        self.x_offset = 0
        self.y_offset = 0

    def show(self, x_offset=0, y_offset=0):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.tree = self._tree()
        self.animation = [FadeIn(x.shift(x_offset * RIGHT + y_offset * UP)) for x in self.tree]
        self.table.first_line.next_to(self.tree, direction = DOWN, buff=1)  # Align the tree and the table
        self.animation = AnimationGroup(*self.animation, *self.table.animation, lag_ratio=0.5)
        return self.animation
    
    def _get_offset(self):
        """
        Calculate the correct offset (so that the node in the bottom level doesn’t overlap)
        """
        # Hardcode the offset for different range = (how many nodes in total, corresponding offset value)
        hardcode_standard = [(3, 0.5, -1), (7, 1, -1.5), (15, 2, -2), (32, 3, -2.5), (63, 4, 4, -3)]
        if len(self.array) > 63:
            print("The max length we support is 63. Now the lengh is:", len(self.array))
            return False
        for cutoff, offset, start_y in hardcode_standard:
            if len(self.array) <= cutoff:
                return offset, start_y

    def _populate_position_and_mobjects(self):
        offset, start_y = self._get_offset()
        if not offset:
            return
        for i, node in enumerate(self.array):
            if i == 0:
                node.position_y = start_y
                if node.left < len(self.array):
                    self.array[node.left].offset = -offset
                if node.right < len(self.array):
                    self.array[node.right].offset = offset
            else:
                parent_x = self.array[node.parent].position_x
                parent_y = self.array[node.parent].position_y
                node.position_x = parent_x + node.offset
                node.position_y = parent_y + 1
                if node.left < len(self.array):
                    self.array[node.left].offset = -abs(node.offset) / 2
                if node.right < len(self.array):
                    self.array[node.right].offset = abs(node.offset) / 2
            node._create_mobject()
        
    def _tree(self):
        mobjects = []
        for node in self.array:
            mobjects.append(node.mobject)
            if node.left < len(self.array):
                line = Line(node.mobject.get_center(), self.array[node.left].mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
                mobjects.append(line)
                self.array[node.left].line_mobject = line
            if node.right < len(self.array):
                line = Line(node.mobject.get_center(), self.array[node.right].mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
                mobjects.append(line)
                self.array[node.right].line_mobject = line
        return VGroup(*mobjects)
        

    def _table(self):
        text_mobjects = [node.text_mobject for node in self.array]
        return Table(text_mobjects, is_mobject=True)
    
    def remove(self):
        """
        Remove the last node
        """
        if not self.array:
            print("Error: the array is empty")
            return
        last = self.array[-1]
        self.array.pop()
        return AnimationGroup(FadeOut(last.mobject), FadeOut(last.line_mobject), self.table.remove(x_offset=self.x_offset))

    def add(self, value):
        """
        Add a node in the end, create a mobject and update the array
        """
        node = HeapNode(len(self.array), value)
        parent_x = self.array[node.parent].position_x
        parent_y = self.array[node.parent].position_y
        if self.array[node.parent].left >= len(self.array):
            node.offset = -abs(self.array[node.parent].offset) / 2
        else:
            node.offset = abs(self.array[node.parent].offset) / 2
        node.position_x = parent_x + node.offset
        node.position_y = parent_y + 1
        node._create_mobject()
        node.mobject = node.mobject.shift(3 * RIGHT)
        node.line_mobject = Line(node.mobject.get_center(), self.array[node.parent].mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        self.array.append(node)
        return node
    
    def _create_text_mobject(self, value):
        return Text(str(value), color=LINE_COLOR, font=FONT, weight="BOLD", font_size=VALUE_SIZE)