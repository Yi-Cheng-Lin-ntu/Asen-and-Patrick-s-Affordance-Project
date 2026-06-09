import os
from pathlib import Path

base_dir = Path("D:/NTU_PSY/Documents/Patric_Asen_BrainHackProject")

# Search for any file matching dog_12s.jpg in the workspace
found = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if "dog_12s.jpg" in f:
            found.append(os.path.join(root, f))

print("Found files matching 'dog_12s.jpg':")
for p in found:
    print(p)
