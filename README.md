# Inverted String Structures: Suffix Array vs Prefix Trie

Performance comparison of Suffix Array and Prefix Trie with inverted strings.

## Prerequisites

- Python 3.1 or higher
- GraphViz system library
- Git for Windows
- Windows 10/11
- PowerShell 5.1 or higher

## Installation (Windows PowerShell)

### 1. Clone Repository
``````powershell
git clone https://github.com/yourusername/inverted-string-structures.git
Set-Location inverted-string-structures
``````

### 2. Create Virtual Environment
``````powershell
python -m venv venv
``````

### 3. Enable Script Execution (if needed)
``````powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
``````

### 4. Activate Virtual Environment
``````powershell
.\venv\Scripts\Activate.ps1
``````
Your prompt should show `(venv)` at the beginning.

### 5. Install Python Dependencies
``````powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
``````

### 6. Install GraphViz System Library

1. Download from: https://graphviz.org/download/
2. Download the Windows installer (`.msi` file)
3. Run installer
4. **IMPORTANT**: Check "Add Graphviz to the system PATH" during installation
5. Restart PowerShell
6. Verify installation:
``````powershell
dot -V
``````

If `dot` is not recognized:
``````powershell
# Add GraphViz to PATH manually:
$env:Path += ";C:\Program Files\Graphviz\bin"

# To make it permanent:
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Graphviz\bin", "User")
``````

### 7. Verify Installation
``````powershell
python -c "import graphviz; print(graphviz.version())"
``````

## Usage

### Generate Datasets
``````powershell
python datasets\generate_datasets.py
``````

This creates:
- `datasets\small.txt` (100 strings)
- `datasets\medium.txt` (1,000 strings)
- `datasets\large.txt` (10,000 strings)
- `datasets\xlarge.txt` (50,000 strings)

### Run All Experiments
``````powershell
python src\experiments.py --all
``````

### Run Without Visualizations (faster)
``````powershell
python src\experiments.py --all --no-visualize
``````

## Output

Results are saved to:
- `results\data\benchmark_results.json` - Raw benchmark data
- `results\graphs\performance_comparison.png` - Performance graphs
- `results\graphs\suffix_array.png` - Suffix Array visualization
- `results\graphs\prefix_trie.png` - Prefix Trie visualization

## Viewing Results

Open images:
``````powershell
Invoke-Item results\graphs\performance_comparison.png
Invoke-Item results\graphs\suffix_array.png
Invoke-Item results\graphs\prefix_trie.png
``````

View JSON data:
``````powershell
notepad results\data\benchmark_results.json
# Or
code results\data\benchmark_results.json
``````

List files:
``````powershell
Get-ChildItem results\graphs
Get-ChildItem results\data
``````

## Reproducibility

All experiments are deterministic and reproducible. To reproduce:

1. Ensure same Python version:
``````powershell
   python --version
``````
2. Use same dependencies:
``````powershell
   pip install -r requirements.txt
``````
3. Generate datasets:
``````powershell
   python datasets\generate_datasets.py
``````
4. Run experiments:
``````powershell
   python src\experiments.py --all
``````

## Project Structure
``````
inverted-string-structures\
├── README.md
├── requirements.txt
├── .gitignore
├── src\
│   ├── __init__.py
│   ├── suffix_array.py       # Suffix Array implementation
│   ├── prefix_trie.py         # Prefix Trie implementation
│   ├── visualizer.py          # GraphViz visualizations
│   ├── benchmarks.py          # Performance benchmarking
│   └── experiments.py         # Experiment runner
├── datasets\
│   ├── generate_datasets.py   # Dataset generator
│   ├── small.txt
│   ├── medium.txt
│   ├── large.txt
│   └── xlarge.txt
├── results\
│   ├── graphs\                # Generated visualizations
│   └── data\                  # Benchmark results
└── docs\
    └── seminar.md             # Full seminar paper (3000+ words)
``````

## Deactivating Virtual Environment

When done working:
``````powershell
deactivate
``````

## Troubleshooting (PowerShell)

### Execution Policy Error
``````powershell
# If you get "cannot be loaded because running scripts is disabled"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
``````

### GraphViz not found
``````powershell
# Check if installed
dot -V

# If not found, add to PATH for current session:
$env:Path += ";C:\Program Files\Graphviz\bin"

# To add permanently:
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\Graphviz\bin", "User")

# Restart PowerShell and verify
dot -V
``````

### Python not found
``````powershell
# Check Python installation
python --version

# Check where Python is installed
Get-Command python | Select-Object Source

# If not found, download from python.org
# During installation, check "Add Python to PATH"
``````

### Module not found errors
``````powershell
# Verify virtual environment is active (should see (venv))
Get-Command python | Select-Object Source

# Should point to venv directory
# Reinstall dependencies:
pip install -r requirements.txt
``````

### Memory errors with large datasets
- Reduce dataset size in experiments.py
- Use `--no-visualize` flag
- Close other applications to free RAM

### Permission Errors
``````powershell
# Run PowerShell as Administrator if needed
Start-Process powershell -Verb RunAs
``````

## Citation

If you use this code, please cite:
[Your Name]. (2024). Inverted String Structures Performance Comparison.
GitHub: https://github.com/yourusername/inverted-string-structures