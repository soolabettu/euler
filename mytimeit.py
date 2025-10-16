import time


class MyTimer:
    """Simple context manager for timing code blocks."""
    def __init__(self, label="Elapsed time"):
        """Initialize the timer with an optional label."""
        self.label = label

    def __enter__(self):
        """Start the timer and return the context manager."""
        self.start = time.time()
        return self  # Optionally, return self to access timing info

    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the timer and print the elapsed time."""
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"{self.label}: {self.elapsed:.4f} seconds")
