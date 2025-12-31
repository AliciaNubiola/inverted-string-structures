import os
import graphviz
from prefix_trie import PrefixTrie
from suffix_array import InvertedSuffixArray


# -------------------------------
# Prefix Trie GraphViz Visualizer
# -------------------------------
import graphviz
def visualize_prefix_trie_graphviz(trie_object, max_depth=None, filename="prefix_trie", highlight_prefix=None):

    dot = graphviz.Digraph(comment='Prefix Trie')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', fontsize='10')
    dot.attr('edge', fontsize='10')
    dot.attr(size='20,20!')
    dot.attr(dpi='300')
    dot.attr(ranksep='0.5')
    dot.attr(nodesep='0.3')

    node_count = [0]

    def _add_nodes(node, parent_id=None, edge_label="", prefix_so_far="", depth=0):
        if max_depth is not None and depth > max_depth:
            return

        current_id = f"node_{node_count[0]}"
        node_count[0] += 1

        # Determine node color
        fillcolor = 'lightblue'
        shape = 'circle'
        if node.is_end:
            fillcolor = 'lightgreen'
            shape = 'doublecircle'

        # Highlight node if it is part of a word containing highlight_prefix
        highlight = False
        if highlight_prefix:
            # If any suffix of current prefix_so_far contains highlight_prefix
            for i in range(len(prefix_so_far)):
                if prefix_so_far[i:].startswith(highlight_prefix):
                    highlight = True
                    break
        if highlight:
            fillcolor = 'yellow'

        dot.node(current_id, "", shape=shape, fillcolor=fillcolor)

        if parent_id is not None:
            dot.edge(parent_id, current_id, label=edge_label)

        for char, child in sorted(node.children.items()):
            _add_nodes(child, current_id, char, prefix_so_far + char, depth + 1)

    _add_nodes(trie_object.root)
    return dot

# -------------------------------
# Suffix Array Text File Export
# -------------------------------
def export_suffix_array_to_txt(sa_object, filename="suffix_array.txt", limit=None):
    """
    Exports the suffix array to a text file.

    Args:
        sa_object: instance of InvertedSuffixArray
        filename: output filename
        limit: maximum number of entries to export (None for all)
    """
    entries = sa_object.suffix_array if limit is None else sa_object.suffix_array[:limit]
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{'Index':<8} | {'Inverted Suffix':<30} | {'Original Word'}\n")
        f.write("-" * 80 + "\n")
        
        for i, idx in enumerate(entries):
            inv_suffix = sa_object.text[idx:idx+30]
            
            # Extract original word by splitting at delimiter
            end = len(inv_suffix)
            for j, ch in enumerate(inv_suffix):
                if ord(ch) >= 0xE000:
                    end = j
                    break
            original = inv_suffix[:end][::-1]  # reverse back
            
            f.write(f"{i:<8} | {inv_suffix:<30} | {original}\n")
        
        if limit and len(sa_object.suffix_array) > limit:
            f.write(f"\n... ({len(sa_object.suffix_array) - limit} more entries)\n")
        
        f.write(f"\nTotal suffixes: {len(sa_object.suffix_array)}\n")


# -------------------------------
# Incremental Insert Visualizer
# -------------------------------
def visualize_incremental_inserts(words, output_dir="./visualizations/insert"):
    """
    Creates visualizations after each word insertion.
    
    Args:
        words: list of words to insert
        output_dir: directory to save output files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f'{output_dir}/trie', exist_ok=True)
    os.makedirs(f'{output_dir}/suffix_array', exist_ok=True)
    
    trie = PrefixTrie()
    sa = InvertedSuffixArray()

    print("\n=== INCREMENTAL INSERT VISUALIZATION ===")
    
    for idx, word in enumerate(words):
        print(f"\n[{idx + 1}/{len(words)}] Inserting: '{word}'")
        
        # Insert into both structures
        trie.insert(word)
        sa.insert(word)
        
        # Generate visualization filenames with zero-padded numbers
        step_num = str(idx + 1).zfill(3)
        
        # Generate Trie visualization
        trie_filename = f'{output_dir}/trie/step_{step_num}_trie_{word}'
        print(f"  → Generating trie visualization...")
        trie_graph = visualize_prefix_trie_graphviz(trie, max_depth=None)
        trie_graph.render(trie_filename, format='png', cleanup=True)
        print(f"  ✓ Saved: {trie_filename}.png")
        
        # Export Suffix Array to text file
        sa_filename = f'{output_dir}/suffix_array/step_{step_num}_suffix_array_{word}.txt'
        print(f"  → Exporting suffix array...")
        export_suffix_array_to_txt(sa, sa_filename)
        print(f"  ✓ Saved: {sa_filename}")
    
    print("\n=== COMPLETE ===")
    print(f"Generated {len(words)} visualization sets in '{output_dir}/' directory")
    print(f"Files are named: step_XXX_trie_WORD.png and step_XXX_suffix_array_WORD.txt")


# -------------------------------
# Combined Visualizer (Original)
# -------------------------------
def visualize_all_graphviz(words, visualize_delete, delete_word, output_dir="./visualizations",):
    """
    Creates visualizations for both trie and suffix array.
    
    Args:
        words: list of words to insert
        output_dir: directory to save output files
        visualize_delete: whether to visualize deletion operations
        delete_word: word to delete (if applicable)
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f'{output_dir}/complete', exist_ok=True)
    if visualize_delete:
        os.makedirs(f'{output_dir}/delete', exist_ok=True)

    trie = PrefixTrie()
    sa = InvertedSuffixArray()

    print("\n=== INSERT PHASE ===")
    for w in words:
        print(f"Inserting: {w}")
        trie.insert(w)
        sa.insert(w)

    print("\n=== GENERATING VISUALIZATIONS FOR INSERT ===")
    
    visualize_incremental_inserts(words)
    
    print("\n=== GENERATING VISUALIZATIONS FOR COMPLETE ===")

    # Generate Trie visualization
    print("Generating Prefix Trie...")
    trie_graph = visualize_prefix_trie_graphviz(trie, max_depth=None)
    trie_graph.render(f'{output_dir}/complete/prefix_trie', format='png', cleanup=True)
    print(f"Saved: {output_dir}/complete/prefix_trie.png")
    
    # Export Suffix Array to text file
    print("Exporting Suffix Array to text file...")
    export_suffix_array_to_txt(sa, f'{output_dir}/complete/suffix_array.txt')
    print(f"Saved: {output_dir}/complete/suffix_array.txt")

    if visualize_delete and delete_word:

        print("\n=== DELETE PHASE ===")
        print(f"Deleting: {words[0]}")
        trie.delete(words[0])
        sa.delete(words[0])

        print("\n=== GENERATING POST-DELETE VISUALIZATIONS ===")
        
        # Generate post-deletion visualizations
        print("Generating Prefix Trie (after deletion)...")
        trie_graph_after = visualize_prefix_trie_graphviz(trie, max_depth=None)
        trie_graph_after.render(f'{output_dir}/delete/prefix_trie_after_delete', format='png', cleanup=True)
        print(f"Saved: {output_dir}/delete/prefix_trie_after_delete.png")
        
        # Export Suffix Array after deletion to text file
        print("Exporting Suffix Array (after deletion) to text file...")
        export_suffix_array_to_txt(sa, f'{output_dir}/delete/suffix_array_after_delete.txt')
        print(f"Saved: {output_dir}/delete/suffix_array_after_delete.txt")

    print("\n=== COMPLETE ===")
    print("All visualizations generated successfully!")


if __name__ == "__main__":

    dataset_name = input("Enter the name of to the dataset file: (Ex. small.txt) ")
    delete_operation = input("Do you want to visualize a delete operation? (y/n): ")
    if delete_operation.lower() == 'y':
        visualize_delete = True
        delete_word = input("Enter the word to delete from the structures: ")
    else:
        visualize_delete = False
        delete_word = None
    # Read words from datasets/dataset_name
    with open(f'datasets/{dataset_name}', 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(words)} words from datasets/{dataset_name}")
    # Generate incremental visualizations
    visualize_all_graphviz(words, visualize_delete, delete_word)