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

input_path = r"\home\yassine\GitRepo\YassineXHedi\ObjectDetectionYoloV8\DatasetAnalysis"
output_path = adapt_path(input_path)

print("Adapted Path:", output_path)

