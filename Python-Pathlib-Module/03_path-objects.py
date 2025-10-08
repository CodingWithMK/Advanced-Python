from pathlib import Path

# ============ Creating path objects from strings ============

file_path_str = "data/union_data.txt"

data_path = Path(file_path_str)



# ============ Creating path objects from other path objects ============

base_path = Path("/home/user")
data_dir = Path("data")

# Combining multiple paths
file_path = base_path / data_dir / "prices.csv"  
print(file_path)
