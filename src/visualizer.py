# -------------------------------
# Suffix Array Visualizer
# -------------------------------
def visualize_suffix_array(sa_object, limit=20):
    """
    Visualizes the suffix array.

    Args:
        sa_object: instance of InvertedSuffixArray
        limit: maximum number of entries to display
    """
    print(f"{'Index':>5} | {'Inverted Suffix':<20} | {'Original Word'}")
    print("-" * 60)
    
    for i, idx in enumerate(sa_object.suffix_array[:limit]):
        inv_suffix = sa_object.text[idx:idx+20]
        
        # Extract original word by splitting at delimiter
        end = len(inv_suffix)
        for j, ch in enumerate(inv_suffix):
            if ord(ch) >= 0xE000:
                end = j
                break
        original = inv_suffix[:end][::-1]  # reverse back
        print(f"{i:5} | {inv_suffix:<20} | {original}")
    
    if len(sa_object.suffix_array) > limit:
        print(f"... ({len(sa_object.suffix_array) - limit} more entries)")
    print(f"Total suffixes: {len(sa_object.suffix_array)}\n")


# -------------------------------
# Prefix Trie Visualizer
# -------------------------------
def visualize_prefix_trie(trie_object, max_depth=5):
    """
    Visualizes the trie structure up to a given depth.

    Args:
        trie_object: instance of PrefixTrie
        max_depth: maximum depth to display
    """

    node_count = 0

    def _dfs(node, prefix="", depth=0):
        nonlocal node_count
        node_count += 1
        if depth > max_depth:
            return
        end_marker = "*" if node.is_end else ""
        print(f"{'  '*depth}{prefix}{end_marker}")
        for char, child in node.children.items():
            _dfs(child, char, depth+1)

    print("Trie Structure (up to depth", max_depth, "):")
    _dfs(trie_object.root)
    print(f"\nTotal nodes displayed (including truncated): {node_count}")
