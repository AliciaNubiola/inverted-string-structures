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
git clone https://github.com/AliciaNubiola/inverted-string-structures.git
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

### 7. Verify Installation
``````powershell
python -c "import graphviz; print(graphviz.version())"
``````

## Usage

### Generate Datasets (should already be generated)
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


## Reproducibility

All experiments are deterministic and reproducible. To reproduce delete datasets and results and follow the steps:

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


## Deactivating Virtual Environment

When done working:
``````powershell
deactivate
``````