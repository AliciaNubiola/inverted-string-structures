Use cProfile for profiling
Use tracemalloc for memory tracking
Use time.perf_counter() for precise timing
Create benchmark functions for:

Insert: Incremental sizes (100, 500, 1K, 5K, 10K, 50K)
Search: Average time over 100 queries
Range search: Average time over 50 range queries
Delete: Average time over 100 deletions


Save results to JSON format