from os.path import commonprefix
from tree import Node
from typing import Iterable, Union

class SuffixTree(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self, strings: Iterable[str], method: str = "ukkonen"):
        if method.lower() == "ukkonen":
            print("Ukkonen's method.")
        elif method.lower() == "simple":
            print("Simple method.")
            for i, string in enumerate(strings):
                string = tuple(char.replace("$", "\\$") for char in string) + (f"${i}", )
                self.value = ()
                for j in range(len(string)):
                    self.append_suffix(string[j:], j)
        else:
            print("Invalid method.")
        return self

    def append_suffix(self, suffix: tuple, position: int):
        if suffix == ():
            return
        for child in self:
            common_prefix = commonprefix((suffix, child.value))
            if len(common_prefix) != 0:
                if len(common_prefix) < len(child.value):
                    child.set_children((
                        SuffixTree(child.value[len(common_prefix):], child.children),
                        SuffixTree(suffix[len(common_prefix):], (Node(position), ))
                    ))
                    child.value = common_prefix
                else:
                    child.append_suffix(suffix[len(child.value):], position)
                return
        self.append(SuffixTree(suffix, (Node(position), )))

    def match(self, pattern: Union[str, tuple]):
        if type(pattern) is str:
            pattern = tuple(char.replace("$", "\\$") for char in pattern)
        if pattern == ():
            return self.get_leaves()
        for child in self:
            if not child.is_leaf():
                child_raw_value = child.value[:-1] if child.value[-1][0] == "$" else child.value
                common_prefix = commonprefix((pattern, child_raw_value))
                if len(common_prefix) >= min(len(pattern), len(child_raw_value)):
                    return child.match(pattern[len(common_prefix):])
        return []

if __name__ == '__main__':
    suffix_tree = SuffixTree().build(("abab", "aab"), "simple").calculate_leaf_number()
    print(suffix_tree.__str__(True))
    print(suffix_tree.match("ba"))
    print(suffix_tree.match(""))
