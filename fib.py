# explanations for member functions are provided in requirements.py
from __future__ import annotations
import math

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min_node = None
        self.count_nodes = 0
        self.PHI = 1.618

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        new_node = FibNode(val)

        # Add new node to the list of roots.
        self.roots.append(new_node)

        # Update the min pointer.
        if self.min_node is None or val < self.min_node.val:
            self.min_node = new_node

        self.count_nodes += 1

        return new_node
        
    def delete_min(self) -> None:
        minimum_node = self.min_node

        self.roots.remove(minimum_node)
        self.count_nodes -= 1

        for child in minimum_node.children:
            child.flag = False
            child.parent = None
            self.roots.append(child)

        self.improve_forest_structure()

        self.min_node = self.roots[0]
        for index in range(1, len(self.roots)):
            if self.roots[index].val < self.min_node.val:
                self.min_node = self.roots[index]


    def find_min(self) -> FibNode:
        return self.min_node if self.min_node is not None else None

    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        node.val = new_val

        if node.val < self.min_node.val:
            self.min_node = node

        # If the node is not a root node, then we need to promote it
        if node not in self.roots:
            self.promote(node)

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define

    def promote(self, node: FibNode) -> None:
        if node not in self.roots:
            parent = node.parent

            parent.children.remove(node)

            node.parent = None
            self.roots.append(node)

            node.flag = False

            if parent.flag:
                self.promote(parent)
            elif parent not in self.roots:
                parent.flag = True

    def improve_forest_structure(self) -> None:
        C = (math.ceil(math.log(self.count_nodes) / math.log(self.PHI)) + 1) * [None]

        R = []

        for root in self.roots:
            R.append(root)

        while len(R) > 0:
            root = R.pop()

            if C[len(root.children)] is None:
                C[len(root.children)] = root
            else:
                node = C[len(root.children)]
                if root.val > node.val:
                    node.children.append(root)
                    root.parent = node
                    R.append(node)
                    self.roots.remove(root)
                else:
                    root.children.append(node)
                    node.parent = root
                    R.append(root)
                    self.roots.remove(node)

                index = -1
                for i, val in enumerate(C):
                    if val is None:
                        continue

                    if val == node:
                        index = i

                C[index] = None
