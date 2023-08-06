from pathlib import Path

# Set __version__ attribute
# Reading VERSION file
version_file = Path(__file__).resolve().parent.parent.parent / Path('VERSION')

with open(version_file, 'r') as f:
    version = f.read().strip()

__version__: str = version
