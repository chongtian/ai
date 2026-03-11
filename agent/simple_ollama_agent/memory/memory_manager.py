import time
class MemoryManager:
    def __init__(self):
        self.history = []

    def add(self, item: dict):
        # attach timestamp
        item_copy = dict(item)
        item_copy['_ts'] = time.time()
        self.history.append(item_copy)

    def last(self, n=5):
        return self.history[-n:]

    def all(self):
        return self.history
