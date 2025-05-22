from pathlib import Path
import os
def adapt_path(original_path):
    home_dir = str(Path.home())

    # Split the original path and extract the base structure
    parts = original_path.split("\\")
    # Find index of "home" to locate username
    if "home" in parts:
        home_index = parts.index("home") + 1  # Username should be right after "home"
        if home_index < len(parts):  
            parts[home_index] = os.path.basename(home_dir)  # Replace username
    # Reconstruct the path
    adapted_path = "\\".join(parts)
    
    return adapted_path
def main():
    original_path = "data.yaml"
    print(adapt_path(original_path))


if __name__ == "__main__":
    main()
