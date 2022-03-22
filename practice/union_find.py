class UnionFind:
    def __init__(self, array):
        self.parent = {}
        for a in array:
            self.parent[a] = a

    def find(self, element):
        parent = self.parent[element]
        if parent == element:
            return element
        else:
            return self.find(parent)
    
    def union(self, element_a, element_b):
        self.parent[self.find(element_a)] = self.find(element_b)