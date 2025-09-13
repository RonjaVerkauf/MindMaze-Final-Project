"""Minimal inventory helper."""
class Inventory:
    def __init__(self):
        self._items = set()
    def add(self, item: str): self._items.add(item)
    def has(self, item: str) -> bool: return item in self._items
    def remove(self, item: str): self._items.discard(item)
    def list(self): return sorted(self._items)
