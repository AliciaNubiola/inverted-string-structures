#Create TrieNode class with __slots__ for memory efficiency
class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}
        self.is_end = False


class PrefixTrie:
    def __init__(self):
        self.root = TrieNode()
        self._node_id = 0
        self._node_map = {}

    # -------------------------------
    # String inversion
    # -------------------------------
    def invert_string(self, s: str) -> str:
        return s[::-1]

    # -------------------------------
    # Insert (O(m))
    # -------------------------------
    def insert(self, word: str) -> None:
        word = self.invert_string(word)
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end = True

    # -------------------------------
    # Search (O(m))
    # -------------------------------
    def search(self, pattern: str) -> bool:
        pattern = self.invert_string(pattern)
        node = self.root

        for char in pattern:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_end

    # -------------------------------
    # Range Search (suffix query)
    # -------------------------------
    def range_search(self, suffix: str):
        suffix = self.invert_string(suffix)
        node = self.root

        for char in suffix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        self._collect(node, list(suffix), results)
        return results

    def _collect(self, node, path, results):
        if node.is_end:
            results.append("".join(path)[::-1])

        for char, child in node.children.items():
            path.append(char)
            self._collect(child, path, results)
            path.pop()

    # -------------------------------
    # Delete (O(m))
    # -------------------------------
    def delete(self, word: str) -> None:
        word = self.invert_string(word)
        self._delete_recursive(self.root, word, 0)

    def _delete_recursive(self, node, word, depth):
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0

        char = word[depth]
        if char not in node.children:
            return False

        should_delete = self._delete_recursive(
            node.children[char], word, depth + 1
        )

        if should_delete:
            del node.children[char]
            return not node.is_end and len(node.children) == 0

        return False

    # -------------------------------
    # Memory usage (node count)
    # -------------------------------
    def memory_usage(self) -> int:
        return self._count_nodes(self.root)

    def _count_nodes(self, node) -> int:
        count = 1
        for child in node.children.values():
            count += self._count_nodes(child)
        return count

    # -------------------------------
    # GraphViz visualization
    # -------------------------------
    def to_graphviz(self, filename="trie.dot"):
        self._node_id = 0
        self._node_map = {}
        lines = ["digraph Trie {", "node [shape=circle];"]

        self._graphviz_dfs(self.root, lines)

        lines.append("}")
        with open(filename, "w") as f:
            f.write("\n".join(lines))

    def _graphviz_dfs(self, node, lines):
        current_id = self._node_id
        self._node_map[id(node)] = current_id
        self._node_id += 1

        if node.is_end:
            lines.append(f'{current_id} [shape=doublecircle];')

        for char, child in node.children.items():
            child_id = self._node_id
            self._graphviz_dfs(child, lines)
            lines.append(f'{current_id} -> {child_id} [label="{char}"];')

