import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from benchmarks import run_insert, run_search, run_range_search, run_delete

# -------------------------------
# Load dataset function
# -------------------------------
def read_words_from_file(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]

# -------------------------------
# Generate deterministic patterns
# -------------------------------
def generate_search_patterns(words, count):
    return words[:count]

def generate_range_patterns(words, count, length=3):
    return [w[:length] for w in words[:count]]

# -------------------------------
# Benchmark driver
# -------------------------------
def run_all_benchmarks(structure_class, name, dataset_sizes, dataset_folder="datasets"):
    results = {"insert": [], "search": [], "range_search": [], "delete": []}

    for size in dataset_sizes:
        words = read_words_from_file(f"{dataset_folder}/{size}.txt")

        # Insert benchmark
        insert_result = run_insert(structure_class, words)
        results["insert"].append({"size": size, **insert_result})

        # Search benchmark
        search_patterns = generate_search_patterns(words, 100)
        search_result = run_search(structure_class, words, search_patterns)
        results["search"].append({"size": size, **search_result})

        # Range search benchmark
        range_patterns = generate_range_patterns(words, 50)
        range_result = run_range_search(structure_class, words, range_patterns)
        results["range_search"].append({"size": size, **range_result})

        # Delete benchmark
        delete_result = run_delete(structure_class, words, delete_count=100)
        results["delete"].append({"size": size, **delete_result})

    # Save results to JSON
    json_file = f"{name}_benchmark_results.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"{name} benchmark results saved to {json_file}")

    return results

# -------------------------------
# Performance plotting
# -------------------------------
def plot_results(results, name):
    sizes = [r["size"] for r in results["insert"]]
    times = [r["time_sec"] for r in results["insert"]]
    memory = [r["peak_memory_bytes"] / (1024*1024) for r in results["insert"]]

    # Time plot
    plt.figure()
    plt.plot(dataset_sizes, times, marker="o")
    plt.title(f"{name} - Insert Time")
    plt.xlabel("Dataset size")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    plt.savefig(f"{name}_insert_time.png")


    # Memory plot
    plt.figure()
    plt.plot(sizes, memory, marker="o", color="orange")
    plt.title(f"{name} - Insert Peak Memory")
    plt.xlabel("Dataset size")
    plt.ylabel("Memory (MB)")
    plt.grid(True)
    plt.xscale("log")
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))
    plt.savefig(f"{name}_insert_memory.png")
    print(f"{name} performance plots saved.")


# -------------------------------
# Main execution
# -------------------------------
if __name__ == "__main__":
    dataset_sizes = ["small", "medium", "large", "xlarge"]
    dataset_folder = "datasets"

    # Run benchmarks for PrefixTrie
    prefix_trie_results = run_all_benchmarks(structure_class="PrefixTrie", name="prefix_trie", dataset_sizes=dataset_sizes)
    plot_results(prefix_trie_results, "prefix_trie")

    # Run benchmarks for InvertedSuffixArray
    sa_results = run_all_benchmarks(structure_class="InvertedSuffixArray", name="suffix_array", dataset_sizes=dataset_sizes)
    plot_results(sa_results, "suffix_array")
