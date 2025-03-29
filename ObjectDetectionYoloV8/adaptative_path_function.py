from pathlib import Path
import os
def adapt_path(original_path="Data/CandyDataset/data23.yaml"):
    """Adapt the path depending on the user.

    Args:
        path: path inside /GitRepo.

    Returns:
        The path depending of the user.

    Example usage:
        adapt_path("Data/CandyDataset/data.yaml")
    """
    home_dir = str(Path.home())
    adapted_path = os.path.join(home_dir, "GitRepo", original_path)
    return adapted_path
def main():
    pass


if __name__ == "__main__":
    main()