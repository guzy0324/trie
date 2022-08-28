from __future__ import annotations
from typing import Any, Iterable, Optional

class Node:
    def __init__(self, value: Optional[Any] = None, children: Iterable[Node] = ()):
        self.value = value
        self.set_children(children)

    def append(self, child: Node):
        self.children.append(child)

    def extend(self, children: Iterable[Node]):
        self.children += children

    def get_leaves(self, leaves: Optional[list] = None):
        if leaves is None:
            leaves = []
        if self.is_leaf():
            leaves.append(self.value)
        for child in self:
            child.get_leaves(leaves)
        return leaves

    def set_children(self, children: Iterable[Node]):
        self.children = []
        self.extend(children)

    def calculate_leaf_number(self):
        if self.is_leaf():
            self.leaf_number = 1
            return self
        self.leaf_number = 0
        for child in self:
            self.leaf_number += child.calculate_leaf_number().leaf_number
        return self

    def is_leaf(self):
        return len(self.children) == 0

    def __eq__(self, other: Node):
        return self.value == other.value

    def __getitem__(self, key):
        return self.children[key]

    def __iter__(self):
        return iter(self.children)

    def __str__(self, leaf_number: Optional[bool] = False, depth: Optional[int] = 0) -> str:
        string = f"{depth * '  '}- {self.value}{f' : {self.leaf_number}' if leaf_number else ''}"
        for child in self:
            string += f"\n{child.__str__(leaf_number, depth + 1)}"
        return string

if __name__ == '__main__':
    root = Node(1)
    children = [Node(1, (Node(i) for i in range(3, 5))), Node(2)]
    root.extend(children)
    print(root)
    print(root != root[0])
    print(root.get_leaves())
