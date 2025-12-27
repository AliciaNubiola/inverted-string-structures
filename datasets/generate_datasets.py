import random
import string
import os

# Set seed for reproducibility
random.seed(42)

def generate_unique_strings(count, min_len=5, max_len=20):
    """Generate a set of unique random strings, order preserved for reproducibility."""
    unique_strings = dict()
    while len(unique_strings) < count:
        length = random.randint(min_len, max_len)
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        unique_strings[s] = None
    return list(unique_strings.keys())

# Dataset specifications
datasets = {
    "small.txt": 100,
    "medium.txt": 1000,
    "large.txt": 10000,
    "xlarge.txt": 50000
}

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Generate datasets
for filename, count in datasets.items():
    print(f"Generating {filename} with {count} strings...")
    strings = generate_unique_strings(count)
    # Optional: shuffle reproducibly
    random.shuffle(strings)
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "w") as f:
        f.write("\n".join(strings))

print("Datasets generated successfully!")
