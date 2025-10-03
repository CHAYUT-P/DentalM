import os
import pickle

class Repository:
    """Base repository class for saving/loading objects using pickle."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.load()

    def save(self):
        """Save all current data to file."""
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        """Load data from file (if it exists)."""
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        return []