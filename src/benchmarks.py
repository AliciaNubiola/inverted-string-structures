import time
import tracemalloc
import cProfile
import json
import random
import string
from prefix_trie import PrefixTrie
from suffix_array import InvertedSuffixArray


def read_words_from_file(filename: str) -> list:
    with open(filename, "r") as f:
        words = [line.strip() for line in f if line.strip()]    
    return words

# -------------------------------
# Benchmarking class
# -------------------------------
class Benchmark:
    def __init__(self):
        self.results = {"prefix_trie": {}, "suffix_array": {}}
        self.dataset_sizes = ["small", "medium", "large", "xlarge"]

    # -------------------------------
    # Benchmark insert
    # -------------------------------
    def benchmark_insert(self, structure_class, name):
        self.results[name]["insert"] = []
        for size in self.dataset_sizes:
            words = read_words_from_file(f"datasets/{size}.txt")

            # Initialize structure
            structure = structure_class()

            # Memory tracking
            tracemalloc.start()
            start_time = time.perf_counter()

            for w in words:
                structure.insert(w)

            elapsed = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            self.results[name]["insert"].append({
                "size": size,
                "time_sec": elapsed,
                "peak_memory_bytes": peak
            })

    # -------------------------------
    # Benchmark search
    # -------------------------------
    def benchmark_search(self, structure_class, name, query_count=100):
        self.results[name]["search"] = []
        size = self.dataset_sizes[-1]
        words = read_words_from_file(f"datasets/{size}.txt")
        structure = structure_class()
        for w in words:
            structure.insert(w)

        # Select queries randomly (some may not exist)
        queries = words[:query_count]

        tracemalloc.start()
        start_time = time.perf_counter()

        for q in queries:
            structure.search(q)

        elapsed = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.results[name]["search"].append({
            "queries": query_count,
            "avg_time_sec": elapsed / query_count,
            "peak_memory_bytes": peak
        })

    # -------------------------------
    # Benchmark range search
    # -------------------------------
    def benchmark_range_search(self, structure_class, name, query_count=50):
        self.results[name]["range_search"] = []
        size = self.dataset_sizes[-1]
        words = read_words_from_file(f"datasets/{size}.txt")
        structure = structure_class()
        for w in words:
            structure.insert(w)

        queries = random.choices(words, k=query_count)

        tracemalloc.start()
        start_time = time.perf_counter()

        for q in queries:
            structure.range_search(q[:3])  # using first 3 chars as suffix/prefix

        elapsed = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.results[name]["range_search"].append({
            "queries": query_count,
            "avg_time_sec": elapsed / query_count,
            "peak_memory_bytes": peak
        })

    # -------------------------------
    # Benchmark delete
    # -------------------------------
    def benchmark_delete(self, structure_class, name, delete_count=100):
        self.results[name]["delete"] = []
        size = self.dataset_sizes[-1]
        words = read_words_from_file(f"datasets/{size}.txt")
        structure = structure_class()
        for w in words:
            structure.insert(w)

        # Pick words to delete
        deletions = random.choices(words, k=delete_count)

        tracemalloc.start()
        start_time = time.perf_counter()

        for w in deletions:
            structure.delete(w)

        elapsed = time.perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.results[name]["delete"].append({
            "deletions": delete_count,
            "avg_time_sec": elapsed / delete_count,
            "peak_memory_bytes": peak
        })

    # -------------------------------
    # Run all benchmarks for a structure
    # -------------------------------
    def run_all(self, structure_class, name):
        print(f"Running benchmarks for {name}...")
        profiler = cProfile.Profile()
        profiler.enable()

        self.benchmark_insert(structure_class, name)
        self.benchmark_search(structure_class, name)
        self.benchmark_range_search(structure_class, name)
        self.benchmark_delete(structure_class, name)

        profiler.disable()
        profiler.print_stats()

    # -------------------------------
    # Save results to JSON
    # -------------------------------
    def save_results(self, filename="benchmark_results.json"):
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=4)


# -------------------------------
# Main benchmarking execution
# -------------------------------
if __name__ == "__main__":
    benchmark = Benchmark()

    # Run benchmarks for PrefixTrie
    benchmark.run_all(PrefixTrie, "prefix_trie")

    # Run benchmarks for InvertedSuffixArray
    benchmark.run_all(InvertedSuffixArray, "suffix_array")

    # Save results to JSON
    benchmark.save_results()
    print("Benchmarking complete. Results saved to benchmark_results.json")
