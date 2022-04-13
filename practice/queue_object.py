from manim import *
from style import *
from table_line import TableLine

class QueueObject:
    def __init__(self, array):
        self.array = array
        self.table = TableLine(array)
        
    def show(self):
        return self.table.show()

    def append(self, element):
        self.array.append(element)
        return self.table.add(element)

    def pop(self):
        self.array.pop(0)
        return self.table.remove_first()

    def length(self):
        return len(self.array)

    def peek_first(self):
        if self.length() == 0:
            return None
        else:
            return self.array[0]
