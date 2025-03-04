import time


class MyTimer:
    def __init__(self, label="Elapsed time"):
        self.label = label

    def __enter__(self):
        self.start = time.time()
        return self  # Optionally, return self to access timing info

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"{self.label}: {self.elapsed:.4f} seconds")
