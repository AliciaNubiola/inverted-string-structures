import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from benchmarks import Benchmark
from prefix_trie import PrefixTrie
from suffix_array import InvertedSuffixArray

# -------------------------------
# Performance plotting
# -------------------------------
def plot_insert_comparison(results):
    """Plot insertion time and memory comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Extract data for both structures
    sizes = [r["size"] for r in results["prefix_trie"]["insert"]]
    
    pt_times = [r["time_sec"] for r in results["prefix_trie"]["insert"]]
    sa_times = [r["time_sec"] for r in results["suffix_array"]["insert"]]
    
    pt_memory = [r["peak_memory_bytes"] / (1024*1024) for r in results["prefix_trie"]["insert"]]
    sa_memory = [r["peak_memory_bytes"] / (1024*1024) for r in results["suffix_array"]["insert"]]
    
    # Time plot
    ax1.plot(sizes, pt_times, marker="o", label="Prefix Trie", linewidth=2, markersize=8)
    ax1.plot(sizes, sa_times, marker="s", label="Suffix Array", linewidth=2, markersize=8)
    ax1.set_title("Insert Time Comparison", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Dataset Size", fontsize=12)
    ax1.set_ylabel("Time (seconds)", fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Memory plot
    ax2.plot(sizes, pt_memory, marker="o", label="Prefix Trie", linewidth=2, markersize=8)
    ax2.plot(sizes, sa_memory, marker="s", label="Suffix Array", linewidth=2, markersize=8)
    ax2.set_title("Insert Peak Memory Comparison", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Dataset Size", fontsize=12)
    ax2.set_ylabel("Memory (MB)", fontsize=12)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("results/graphs/insert_comparison.png", dpi=300, bbox_inches='tight')
    print("Insert comparison plot saved to results/graphs/insert_comparison.png")
    plt.close()


def plot_search_comparison(results):
    """Plot search performance comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    structures = ["prefix_trie", "suffix_array"]
    labels = ["Prefix Trie", "Suffix Array"]
    colors = ['#2E86AB', '#A23B72']
    
    avg_times = []
    for struct in structures:
        if results[struct]["search"]:
            avg_time = results[struct]["search"][0]["avg_time_sec"] * 1000000  # Convert to microseconds
            avg_times.append(avg_time)
        else:
            avg_times.append(0)
    
    bars = ax.bar(labels, avg_times, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_title("Average Search Time Comparison", fontsize=14, fontweight='bold')
    ax.set_ylabel("Average Time (µs)", fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, avg_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} µs',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("results/graphs/search_comparison.png", dpi=300, bbox_inches='tight')
    print("Search comparison plot saved to results/graphs/search_comparison.png")
    plt.close()


def plot_range_search_comparison(results):
    """Plot range search performance comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    structures = ["prefix_trie", "suffix_array"]
    labels = ["Prefix Trie", "Suffix Array"]
    colors = ['#2E86AB', '#A23B72']
    
    avg_times = []
    for struct in structures:
        if results[struct]["range_search"]:
            avg_time = results[struct]["range_search"][0]["avg_time_sec"] * 1000000  # Convert to microseconds
            avg_times.append(avg_time)
        else:
            avg_times.append(0)
    
    bars = ax.bar(labels, avg_times, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_title("Average Range Search Time Comparison", fontsize=14, fontweight='bold')
    ax.set_ylabel("Average Time (µs)", fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, avg_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} µs',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("results/graphs/range_search_comparison.png", dpi=300, bbox_inches='tight')
    print("Range search comparison plot saved to results/graphs/range_search_comparison.png")
    plt.close()


def plot_delete_comparison(results):
    """Plot deletion performance comparison"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    structures = ["prefix_trie", "suffix_array"]
    labels = ["Prefix Trie", "Suffix Array"]
    colors = ['#2E86AB', '#A23B72']
    
    avg_times = []
    for struct in structures:
        if results[struct]["delete"]:
            avg_time = results[struct]["delete"][0]["avg_time_sec"] * 1000000  # Convert to microseconds
            avg_times.append(avg_time)
        else:
            avg_times.append(0)
    
    bars = ax.bar(labels, avg_times, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax.set_title("Average Deletion Time Comparison", fontsize=14, fontweight='bold')
    ax.set_ylabel("Average Time (µs)", fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, avg_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} µs',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("results/graphs/delete_comparison.png", dpi=300, bbox_inches='tight')
    print("Deletion comparison plot saved to results/graphs/delete_comparison.png")
    plt.close()


def plot_all_operations_comparison(results):
    """Plot all operations in one comprehensive figure"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Inverted String Structures: Performance Comparison', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # 1. Insert Time (top-left)
    ax = axes[0, 0]
    sizes = [r["size"] for r in results["prefix_trie"]["insert"]]
    pt_times = [r["time_sec"] for r in results["prefix_trie"]["insert"]]
    sa_times = [r["time_sec"] for r in results["suffix_array"]["insert"]]
    
    ax.plot(sizes, pt_times, marker="o", label="Prefix Trie", linewidth=2.5, markersize=10, color='#2E86AB')
    ax.plot(sizes, sa_times, marker="s", label="Suffix Array", linewidth=2.5, markersize=10, color='#A23B72')
    ax.set_title("Insert Time vs Dataset Size", fontsize=13, fontweight='bold')
    ax.set_xlabel("Dataset Size", fontsize=11)
    ax.set_ylabel("Time (seconds)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 2. Insert Memory (top-right)
    ax = axes[0, 1]
    pt_memory = [r["peak_memory_bytes"] / (1024*1024) for r in results["prefix_trie"]["insert"]]
    sa_memory = [r["peak_memory_bytes"] / (1024*1024) for r in results["suffix_array"]["insert"]]
    
    ax.plot(sizes, pt_memory, marker="o", label="Prefix Trie", linewidth=2.5, markersize=10, color='#2E86AB')
    ax.plot(sizes, sa_memory, marker="s", label="Suffix Array", linewidth=2.5, markersize=10, color='#A23B72')
    ax.set_title("Memory Usage vs Dataset Size", fontsize=13, fontweight='bold')
    ax.set_xlabel("Dataset Size", fontsize=11)
    ax.set_ylabel("Memory (MB)", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # 3. Search Time (bottom-left)
    ax = axes[1, 0]
    operations = ["Search", "Range Search", "Delete"]
    pt_values = []
    sa_values = []
    
    for op_key in ["search", "range_search", "delete"]:
        if results["prefix_trie"][op_key]:
            pt_values.append(results["prefix_trie"][op_key][0]["avg_time_sec"] * 1000000)
        else:
            pt_values.append(0)
        
        if results["suffix_array"][op_key]:
            sa_values.append(results["suffix_array"][op_key][0]["avg_time_sec"] * 1000000)
        else:
            sa_values.append(0)
    
    x = range(len(operations))
    width = 0.35
    ax.bar([i - width/2 for i in x], pt_values, width, label='Prefix Trie', color='#2E86AB', alpha=0.8, edgecolor='black')
    ax.bar([i + width/2 for i in x], sa_values, width, label='Suffix Array', color='#A23B72', alpha=0.8, edgecolor='black')
    ax.set_title("Operation Time Comparison", fontsize=13, fontweight='bold')
    ax.set_ylabel("Average Time (µs)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(operations)
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)
    
    # 4. Memory comparison table (bottom-right)
    ax = axes[1, 1]
    ax.axis('tight')
    ax.axis('off')
    
    table_data = []
    table_data.append(["Operation", "Prefix Trie", "Suffix Array"])
    
    for op_key, op_name in [("insert", "Insert"), ("search", "Search"), 
                             ("range_search", "Range Search"), ("delete", "Delete")]:
        if results["prefix_trie"][op_key]:
            pt_mem = results["prefix_trie"][op_key][-1 if op_key == "insert" else 0]["peak_memory_bytes"] / (1024*1024)
            sa_mem = results["suffix_array"][op_key][-1 if op_key == "insert" else 0]["peak_memory_bytes"] / (1024*1024)
            table_data.append([op_name, f"{pt_mem:.2f} MB", f"{sa_mem:.2f} MB"])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.35, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(3):
        table[(0, i)].set_facecolor('#4A90E2')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data)):
        for j in range(3):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F0F0F0')
    
    ax.set_title("Memory Usage Summary", fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig("results/graphs/comprehensive_comparison.png", dpi=300, bbox_inches='tight')
    print("Comprehensive comparison plot saved to results/graphs/comprehensive_comparison.png")
    plt.close()


# -------------------------------
# Main execution
# -------------------------------
if __name__ == "__main__":
    import os
    
    # Create results directories if they don't exist
    os.makedirs("results/graphs", exist_ok=True)
    os.makedirs("results/data", exist_ok=True)
    
    print("="*60)
    print("Running Benchmarks...")
    print("="*60)
    
    # Run all benchmarks using your existing Benchmark class
    benchmark = Benchmark()
    
    # Run benchmarks for PrefixTrie
    print("\n[1/2] Benchmarking Prefix Trie...")
    benchmark.run_all(PrefixTrie, "prefix_trie")
    
    # Run benchmarks for InvertedSuffixArray
    print("\n[2/2] Benchmarking Suffix Array...")
    benchmark.run_all(InvertedSuffixArray, "suffix_array")
    
    # Save results to JSON in results/data
    results_file = "results/data/benchmark_results.json"
    benchmark.save_results(results_file)
    print(f"\n✓ Results saved to {results_file}")
    
    # Load results for plotting
    with open(results_file, "r") as f:
        results = json.load(f)
    
    print("\n" + "="*60)
    print("Generating Plots...")
    print("="*60)
    
    # Generate all plots
    plot_insert_comparison(results)
    plot_search_comparison(results)
    plot_range_search_comparison(results)
    plot_delete_comparison(results)
    plot_all_operations_comparison(results)
    
    print("\n" + "="*60)
    print("✓ All benchmarks and plots complete!")
    print("="*60)
    print("\nResults:")
    print(f"  - Data: {results_file}")
    print(f"  - Graphs: results/graphs/")
    print("\nView plots:")
    print("  Invoke-Item results\\graphs\\comprehensive_comparison.png")